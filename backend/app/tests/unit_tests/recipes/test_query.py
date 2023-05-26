import pytest
from unittest.mock import Mock
from sqlalchemy import Select


@pytest.mark.asyncio
async def test_get_query(recipes_instance, params_get_recipes, sample_query):
    recipes_instance.modification_query = Mock(return_value=sample_query)
    query = recipes_instance.get_query(params_get_recipes)
    assert isinstance(query, Select)


@pytest.mark.asyncio
async def test_modification_query(recipes_instance, params_get_recipes, sample_query):
    query = recipes_instance.modification_query(params_get_recipes, sample_query)
    assert isinstance(query, Select)
