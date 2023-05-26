from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, distinct, update, delete, desc, Column, CursorResult
from sqlalchemy.engine import row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_

from app.handlers.recipes.exceptions import AddConflict, UpdateConflict, DeleteConflict
from app.handlers.recipes.models import RecipesModel, TagsModel, RecipesTags
from app.handlers.recipes.schemas import RecipeSchema, AddRecipeSchema, EditRecipeSchema


@dataclass
class Recipe:
    """
    Class for recipes data processing
    """
    session: AsyncSession

    async def get_data(self, params: RecipeSchema) -> dict:
        """
        :param params: query parameters. Filled on the frontend
        :return dictionary with amount of data and list of Recipes
        """
        query: select = self.get_query(params)
        rows_count: int = (await self.session.execute(
            select(func.count()).select_from(query)
        )).scalars().one()
        items: row = (await self.session.execute(query)).fetchall()
        result: dict = {'totalItems': rows_count, 'items': await self.format_data(items, params)}
        return result

    @staticmethod
    def get_query(params: RecipeSchema) -> select:
        """
        :param params: from UI
        :return: query
        """
        query: select = (
            select(
                RecipesModel,
                func.array_agg(distinct(TagsModel.tag)).label('tags'))
            .join(RecipesTags, RecipesModel.id == RecipesTags.recipe_id)
            .join(TagsModel, TagsModel.id == RecipesTags.tag_id)
            .group_by(RecipesModel.id)
        )
        query = Recipe.modification_query(params, query)
        return query

    @staticmethod
    def modification_query(params: RecipeSchema, query: select) -> select:
        """
        :param params: from UI
        :param query: sql-query for get recipes
        :return: query
        """
        if getattr(params, 'search', None) and len(params.search['tags']):
            # Create a list of conditions for filtering by tags
            tag_filters: list = [TagsModel.id == tag_id for tag_id in params.search['tags']]
            # Combine conditions with the OR operator
            query = query.filter(or_(*tag_filters))
        if getattr(params, 'search', None) and params.search['ingredients']:
            column_ingredients: Column = getattr(RecipesModel, 'ingredients')
            query = query.filter(column_ingredients.ilike(f'%{params.search["ingredients"]}%'))
        if getattr(params, 'sortBy', None) and len(params.sortBy):
            for sort in params.sortBy:
                key: str = sort['key']
                order: str = sort["order"]
                table_column = getattr(RecipesModel, key)
                if order == 'asc':
                    query = query.order_by(table_column)
                else:
                    query = query.order_by(desc(table_column))
        return query

    async def format_data(self, items: row, params: RecipeSchema) -> list:
        """
        :param items: data from DB
        :param params: params from UI
        :return: list of prepared data
        """
        async def prep_recipes(item: row) -> dict:
            recipe: RecipesModel = item.RecipesModel
            if getattr(params, 'search', None) and len(params.search['tags']):
                tags: list = await self.getAssociativeTags(recipe)
            else:
                tags: list = item.tags
            d = {
                'id': recipe.id,
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'time': recipe.time,
                'tags': tags
            }
            return d

        result: list = [await prep_recipes(item) for item in items]
        return result

    async def getAssociativeTags(self, recipe) -> list:
        """
        Query for tag addition after filtering
        :param recipe: one entry from a table
        :return: list of tags
        """
        query: select = (
            select(func.array_agg(TagsModel.tag).label('tags'))
            .select_from(RecipesTags)
            .join(TagsModel, RecipesTags.tag_id == TagsModel.id)
            .where(RecipesTags.recipe_id == recipe.id)
            .group_by(RecipesTags.recipe_id)
        )
        result: list = (await self.session.execute(query)).scalar()
        return result

    async def add_recipe(self, params: AddRecipeSchema) -> int:
        """
        :param params: from UI
        :return: ID
        """
        params_dict: dict = params.dict()
        tags: list[int] = params_dict.pop('tags')
        new_recipe: RecipesModel = RecipesModel(**params_dict)
        try:
            self.session.add(new_recipe)
            await self.session.flush()
            recipe_id: int = new_recipe.id
            await self.add_in_association_table(recipe_id=recipe_id, tags=tags)
            await self.session.commit()
            return recipe_id
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            raise AddConflict

    async def add_in_association_table(
            self,
            recipe_id: int,
            tags: list[int]
    ) -> None:
        """
        :param recipe_id: Recipe ID
        :param tags: tag list
        :return: None
        """
        for tag_id in tags:
            new_recipes_tags: RecipesTags = RecipesTags(recipe_id=recipe_id, tag_id=tag_id)
            self.session.add(new_recipes_tags)
            await self.session.flush()

    async def del_recipe(self, recipe_id: int) -> CursorResult:
        """
        :param recipe_id: ID of the recipe to be removed
        :return: CursorResult
        """
        query: delete = delete(RecipesModel).where(RecipesModel.id == recipe_id)
        try:
            await self.delete_in_association_table(recipe_id=recipe_id)
            await self.session.flush()
            response: CursorResult = await self.session.execute(query)
            await self.session.commit()
            return response
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            raise DeleteConflict

    async def delete_in_association_table(self, recipe_id: int) -> None:
        """
        :param recipe_id: - ID of the recipe to be del
        :return: None
        """
        await self.session.execute(
            RecipesTags.__table__.delete().where(RecipesTags.recipe_id == recipe_id)
        )
        await self.session.flush()

    async def edit_recipe(self, recipe_id: int, params: EditRecipeSchema) -> int:
        """
        :param recipe_id: ID of the recipe to be edited
        :param params: from UI
        :return: ID
        """
        params_dict: dict = params.dict()
        tags: list[int] | list = params_dict.pop('tags', [])
        params_dict.pop('_sa_instance_state', None)
        query: update = (update(RecipesModel).values(**params_dict).where(RecipesModel.id == recipe_id))
        try:
            await self.session.execute(query)
            await self.session.flush()
            await self.delete_in_association_table(recipe_id)
            await self.add_in_association_table(recipe_id, tags)
            await self.session.commit()
            return recipe_id
        except IntegrityError as e:
            print('ERROR: ', e)
            await self.session.rollback()
            raise UpdateConflict
