from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_connector import get_session
from app.db.redis_helper import ClientCache
import app.config as config
from app.handlers.recipes.handler import Recipe
from app.handlers.recipes.headers import recipes_header
from app.handlers.recipes.schemas import RecipeSchema

recipes_router = APIRouter()
redis = ClientCache(config.REDIS_PARAMS)


@recipes_router.get('/header')
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def get_header() -> dict:
    """
    Router to get a description of the recipe table columns
    :return header in dict
    """
    header: dict = recipes_header
    return {'headers': header}


@recipes_router.post('/recipes')
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def get_recipes(
        q: Request,
        params: RecipeSchema,
        session: AsyncSession = Depends(get_session)
) -> dict:
    """
    Router to retrieve a list of recipes.
    :return: Dictionary with number and list of activities
    """
    recipe: Recipe = Recipe(session)
    data: dict = await recipe.get_data(params=params)
    return {'totalItems': data['totalItems'], 'items': data['items']}
