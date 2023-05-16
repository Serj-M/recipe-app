from fastapi import APIRouter, Depends, Request

from api.handlers.mery.handler import Mery
from api.handlers.mery.schemas import SchemaMery

from app.db.redis_helper import ClientCache
import app.config as config
from app.handlers.recipes.headers import recipes_header

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
