import pytest

from services.category_service import create_category

# ---------------------------------------------------------------------------
# GET /api/categories/{category}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_returns_200(client):
    # Arrange: category exists in the database
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    # Act: request it through the API
    response = await client.get("/api/categories/Food")

    # Assert: correct status and the response body contains the category data
    assert response.status_code == 200
    assert response.json()["text"] == "Food"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_returns_404_when_not_found(client):
    # Arrange: nothing in the database

    # Act
    response = await client.get("/api/categories/NonExistent")

    # Assert: the API handler raises HTTPException(404)
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/categories
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_returns_200(client):
    # Arrange: valid payload, no parent
    payload = {
        "text": "Food",
        "pictogram": "http://example.com/food.jpg",
        "parent_category": None,
    }

    # Act
    response = await client.post("/api/categories", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["text"] == "Food"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_with_existing_parent_returns_200(client):
    # Arrange: parent must exist before the child can reference it
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    payload = {
        "text": "Sweets",
        "pictogram": "http://example.com/sweets.jpg",
        "parent_category": "Food",
    }

    # Act
    response = await client.post("/api/categories", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["text"] == "Sweets"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_returns_400_when_parent_not_found(client):
    # Arrange: payload references a parent that does not exist
    payload = {
        "text": "Sweets",
        "pictogram": "http://example.com/sweets.jpg",
        "parent_category": "NonExistent",
    }

    # Act
    response = await client.post("/api/categories", json=payload)

    # Assert: the API handler raises HTTPException(400)
    assert response.status_code == 400
