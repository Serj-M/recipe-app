from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.db.db_connector import get_session
from app.db.redis_helper import ClientCache
import app.config as config
from app.handlers.recipes.exceptions import NotFoundId
from app.handlers.recipes.handler import Recipe
from app.handlers.recipes.headers import recipes_header
from app.handlers.recipes.schemas import RecipeSchema, AddRecipeSchema, EditRecipeSchema

recipes_router = APIRouter()
redis = ClientCache(config.REDIS_PARAMS)


@recipes_router.get('/header')
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def get_header() -> dict:
    """
    Router to get a description of the recipe table columns
    :return: Header in dict
    """
    header: dict = recipes_header
    return {'headers': header}


@recipes_router.post('/items')
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


@recipes_router.post('/add', status_code=201)
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def add_recipe(
        params: AddRecipeSchema,
        session: AsyncSession = Depends(get_session)
) -> int:
    """
    Router for adding a recipe.
    :return: ID added
    """
    recipe: Recipe = Recipe(session)
    _id: int = await recipe.add_recipe(params=params)
    return _id


@recipes_router.delete('/del/{recipe_id}')
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def del_recipe(
        recipe_id: int,
        session: AsyncSession = Depends(get_session)
) -> JSONResponse:
    """
    Router for deleting a recipe.
    :return: ID added
    """
    try:
        recipe: Recipe = Recipe(session)
        await recipe.del_recipe(recipe_id=recipe_id)
        response = JSONResponse(
            content="Successfully removed",
            status_code=status.HTTP_200_OK
        )
        return response
    except Exception as e:
        print('ERROR: ', e)
        if e.args[0] == 'No row was found when one was required':
            raise NotFoundId
        raise HTTPException(
            status_code=500,
            detail=f'Server error while deleting record'
        )


@recipes_router.put('/edit/{recipe_id}')
@redis.cache(ex=config.REDIS_CACHE_EX.default)
async def edit_recipe(
        recipe_id: int,
        params: EditRecipeSchema,
        session: AsyncSession = Depends(get_session)
) -> int:
    """
    Router for editing a recipe.
    :return: ID added
    """
    recipe: Recipe = Recipe(session)
    _id: int = await recipe.edit_recipe(recipe_id=recipe_id, params=params)
    return 0
