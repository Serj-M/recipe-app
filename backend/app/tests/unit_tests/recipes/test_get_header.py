import pytest
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
