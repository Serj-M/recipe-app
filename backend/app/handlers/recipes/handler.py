from dataclasses import dataclass

import row as row
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select, or_, and_

from app.handlers.recipes.exceptions import NotAvailableDB, AddConflict, UpdateConflict, DeleteConflict
from app.handlers.recipes.models import RecipesModel, TagsModel, RecipesTags
from app.handlers.recipes.schemas import RecipeSchema


@dataclass
class Recipe:
    """
    Class for recipes data processing
    """
    session: AsyncSession

    async def get_data(self, params: RecipeSchema) -> dict:
        """
        Retrieving prescription data
        :params
            @params - query parameters. Filled on the frontend
        :return dictionary with amount of data and list of Recipes
        """
        # items: list = [{
        #     'title': 'Pancakes',
        #     'ingredients': 'Flour, Eggs, Milk, Salt, Sugar, Oil',
        #     'instructions': 'Mix flour, eggs, milk, salt, and sugar in a bowl until smooth. Heat and grease a '
        #                     'skillet. Pour the batter onto the skillet and cook until golden brown on both sides. '
        #                     'Repeat with the remaining batter. Serve the pancakes with your favorite fillings or '
        #                     'toppings.',
        #     'time': 1,
        #     'tags': 'Breakfast, Desserts'
        # }]
        query: Select = select(
            RecipesModel, TagsModel
        ).join(
            RecipesTags, RecipesModel.id == RecipesTags.recipe_id
        ).join(
            TagsModel, TagsModel.id == RecipesTags.tag_id
        )
        items: list = (await self.session.execute(query)).fetchall()

        def prep_recipes(item: row) -> dict:
            # recipe_dict: dict = dict(recipe)
            recipe = item.RecipesModel
            tag = item.TagsModel
            d = {
                'title': recipe.title,
                'ingredients': recipe.ingredients,
                'instructions': recipe.instructions,
                'time': recipe.time,
                'tags': tag.tag
            }
            return d
        recipes: list = list(map(prep_recipes, items))

        result: dict = {'totalItems': 10, 'items': recipes}
        return result
