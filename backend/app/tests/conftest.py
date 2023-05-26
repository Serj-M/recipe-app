import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.handlers.recipes.handler import Recipe
from app.handlers.recipes.schemas import RecipeSchema
from app.db.db_connector import get_session

session: AsyncSession = Depends(get_session)

app = FastAPI()


@pytest.fixture(autouse=True)
def disable_logging():
    logger.disable('app.db.redis_helper')


@pytest.fixture(scope='module')
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def recipes_instance():
    recipe = Recipe(session)
    return recipe


@pytest.fixture
def sample_query():
    return select()


@pytest.fixture
def params_get_recipes():
    data = {
        'page': 1,
        'itemsPerPage': 10,
        'sortBy': [{
            "key": "time",
            "order": "asc"
        }],
        'search': {"tags": [1],
                   "ingredients": "f"}
    }
    params = RecipeSchema(**data)
    return params
