from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, distinct, update, delete, desc, Column
from sqlalchemy.engine import row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, or_, and_

from app.handlers.recipes.exceptions import NotAvailableDB, AddConflict, UpdateConflict, DeleteConflict
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
        :params
            @params - query parameters. Filled on the frontend
        :return dictionary with amount of data and list of Recipes
        """
        query: select = self.get_query(params)
        rows_count: int = (await self.session.execute(
            select(func.count()).select_from(query)
        )).scalars().one()
        items: row = (await self.session.execute(query)).fetchall()
        result: dict = {'totalItems': rows_count, 'items': self.format_data(items)}
        return result

    @staticmethod
    def get_query(params: RecipeSchema) -> select:
        query: select = select(
            RecipesModel,
            func.array_agg(distinct(TagsModel.tag)).label('tags')
        ).join(
            RecipesTags, RecipesModel.id == RecipesTags.recipe_id
        ).join(
            TagsModel, TagsModel.id == RecipesTags.tag_id
        ).group_by(
            RecipesModel.id,
            RecipesModel.title,
            RecipesModel.ingredients,
            RecipesModel.instructions,
            RecipesModel.time
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
            column_id: Column = getattr(TagsModel, 'id')
            # Create a list of conditions for filtering by tags
            tag_filters: list = [column_id == tag_id for tag_id in params.search['tags']]
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

    @staticmethod
    def format_data(items: row) -> list:
        def prep_recipes(item: row) -> dict:
            recipe = item.RecipesModel
            tags = item.tags
            d = {
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'time': recipe.time,
                'tags': tags
            }
            return d

        items: list = list(map(prep_recipes, items))
        return items

    async def add_recipe(self, params: AddRecipeSchema) -> int:
        """
        :params:
            @params - from UI
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
        params:
            @recipe_id - Recipe ID
            @tags - tag list
        :return: None
        """
        for tag_id in tags:
            new_recipes_tags: RecipesTags = RecipesTags(recipe_id=recipe_id, tag_id=tag_id)
            self.session.add(new_recipes_tags)
            await self.session.flush()

    async def del_recipe(self, recipe_id: int) -> None:
        """
        :params:
            @recipe_id - ID of the recipe to be removed
        :return: None
        """
        query: delete = delete(RecipesModel).where(RecipesModel.id == recipe_id)
        try:
            await self.delete_in_association_table(recipe_id=recipe_id)
            await self.session.flush()
            await self.session.execute(query)
            await self.session.commit()
            return None
        except IntegrityError as e:
            print(e)
            await self.session.rollback()
            raise DeleteConflict

    async def delete_in_association_table(self, recipe_id: int) -> None:
        """
        params:
            @recipe_id - ID of the recipe to be del
        :return: None
        """
        await self.session.execute(
            RecipesTags.__table__.delete().where(RecipesTags.recipe_id == recipe_id)
        )
        await self.session.flush()

    async def edit_recipe(self, recipe_id: int, params: EditRecipeSchema) -> int:
        """
        :params:
            @recipe_id - ID of the recipe to be edited
            @params - from UI
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
