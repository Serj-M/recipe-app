import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import select, NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from loguru import logger
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.config import DATABASE_URL
from app.handlers.recipes.handler import Recipe
from app.handlers.recipes.models import Recipes_Base
from app.handlers.recipes.schemas import RecipeSchema
from app.db.db_connector import get_session
from app.main import app


# There should be a connection to the test database here. But in my pet project I am using a generic DB.
DATABASE_URL_TEST = DATABASE_URL

sess: AsyncSession = Depends(get_session)
engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
metadata = Recipes_Base.metadata


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_session] = override_get_async_session


@pytest.fixture()
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(autouse=True)
def disable_logging():
    logger.disable('app.db.redis_helper')


@pytest.fixture(scope='module')
def client():
    tc = TestClient(app)
    yield tc


@pytest.fixture
def recipes_instance():
    recipe = Recipe(sess)
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
