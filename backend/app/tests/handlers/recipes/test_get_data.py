import pytest
from unittest.mock import AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.handlers.recipes.handler import Recipe
from app.handlers.recipes.schemas import RecipeSchema
from app.db.db_connector import get_session


session: AsyncSession = Depends(get_session)


@pytest.mark.asyncio
async def test_get_data():
    recipe = Recipe(session)
    params = RecipeSchema(...)

    # Create a simulated async function and define the return data
    recipe.get_query = AsyncMock(return_value='query result')
    recipe.session.execute = AsyncMock(side_effect=[
        [('item1', 'item2')],
        1
    ])
    recipe.format_data = Mock(return_value=[{
        'title': 'value',
        'ingredients': 'value',
        'instructions': 'value',
        'time': 'value',
        'tags': 'value'
    }])

    result = await recipe.get_data(params)

    assert 'totalItems' in result
    assert 'items' in result
    assert isinstance(result['totalItems'], int)
    assert isinstance(result['items'], list)
