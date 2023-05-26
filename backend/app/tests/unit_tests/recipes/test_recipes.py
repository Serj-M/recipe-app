import pytest
from unittest.mock import Mock
from sqlalchemy import Select

from app.handlers.recipes.routes import get_header


@pytest.mark.asyncio
async def test_get_header():
    mock_header = [
        {'title': 'Title', 'align': 'start', 'sortable': False, 'key': 'title', 'width': '10%'},
        {'title': 'Ingredients', 'key': 'ingredients', 'align': 'end', 'sortable': False, 'width': '20%'},
        {'title': 'Instructions for preparation', 'key': 'instructions', 'align': 'end', 'sortable': False, 'width': '40%'},
        {'title': 'Cook time', 'key': 'time', 'align': 'end', 'width': '10%'},
        {'title': 'Tags', 'key': 'tags', 'align': 'end', 'sortable': False, 'width': '15%'},
        {'title': 'Actions', 'key': 'actions', 'sortable': False, 'width': '5%'},
    ]

    response = await get_header()

    assert isinstance(response, dict)
    assert response['headers'] == mock_header
    for item in response['headers']:
        assert 'title' in item and 'key' in item


@pytest.mark.asyncio
async def test_get_query(recipes_instance, params_get_recipes, sample_query):
    recipes_instance.modification_query = Mock(return_value=sample_query)
    query = recipes_instance.get_query(params_get_recipes)
    assert isinstance(query, Select)


@pytest.mark.asyncio
async def test_modification_query(recipes_instance, params_get_recipes, sample_query):
    query = recipes_instance.modification_query(params_get_recipes, sample_query)
    assert isinstance(query, Select)
