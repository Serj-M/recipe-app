import pytest


@pytest.mark.asyncio
async def test_get_recipes(client):
    response = client.post("/recipes/v1/items", json={
        "page": 1,
        "itemsPerPage": 10,
        "sortBy": [],
        "search": {}
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_recipes_validation_error(client):
    response = client.post("/recipes/v1/items", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_recipes(client):
    response = client.post("/recipes/v1/add", json={
        "title": "Title ...",
        "ingredients": "Ingredients ...",
        "instructions": "Instructions...",
        "time": 1,
        "tags": [1]
    })
    assert response.status_code == 201 or response.status_code == 409


@pytest.mark.asyncio
async def test_add_recipes_validation_error(client):
    response = client.post("/recipes/v1/add", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_edit_recipes(client):
    response = client.put("/recipes/v1/edit/1", json={
        "title": "Edited title",
        "ingredients": "Edited ingredients",
        "instructions": "Edited instructions",
        "time": 1,
        "tags": [1]
    })
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_edit_recipes_validation_error(client):
    response = client.put("/recipes/v1/edit/12759", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_del_recipes_validation_error(client):
    response = client.delete("/recipes/v1/del/95714")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_tags(client):
    response = client.get("/recipes/v1/tags")
    assert response.status_code == 200
