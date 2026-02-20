import pytest

from services.category_service import create_category
from services.word_service import create_word


# ---------------------------------------------------------------------------
# GET /api/words/{word}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_find_word_returns_200(client):
    # Arrange
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category=None,
    )

    # Act
    response = await client.get("/api/words/Cheese")

    # Assert
    assert response.status_code == 200
    assert response.json()["text"] == "Cheese"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_word_returns_404_when_not_found(client):
    response = await client.get("/api/words/NonExistent")

    assert response.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/words
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word_returns_200(client):
    # Arrange: valid payload, no category
    payload = {
        "text": "Cheese",
        "pictogram": "http://example.com/cheese.jpg",
        "asl_video": "http://example.com/cheese.mp4",
        "category": None,
    }

    # Act
    response = await client.post("/api/words", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["text"] == "Cheese"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word_with_existing_category_returns_200(client):
    # Arrange: the category must exist before the word can reference it
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    payload = {
        "text": "Cheese",
        "pictogram": "http://example.com/cheese.jpg",
        "asl_video": "http://example.com/cheese.mp4",
        "category": "Food",
    }

    # Act
    response = await client.post("/api/words", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["text"] == "Cheese"


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word_returns_400_when_category_not_found(client):
    # Arrange: payload references a category that does not exist
    payload = {
        "text": "Cheese",
        "pictogram": "http://example.com/cheese.jpg",
        "asl_video": "http://example.com/cheese.mp4",
        "category": "NonExistent",
    }

    # Act
    response = await client.post("/api/words", json=payload)

    # Assert: the API handler raises HTTPException(400)
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /api/words/{word}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_word_returns_204(client):
    # Arrange
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category=None,
    )

    # Act
    response = await client.delete("/api/words/Cheese")

    # Assert: 204 No Content — there is no body to check, only the status code
    assert response.status_code == 204


# ---------------------------------------------------------------------------
# GET /api/words
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_words_returns_200(client):
    # Arrange
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category=None,
    )

    # Act
    response = await client.get("/api/words")

    # Assert: endpoint is reachable and returns the inserted word
    assert response.status_code == 200
    texts = {w["text"] for w in response.json()}
    assert "Cheese" in texts


# ---------------------------------------------------------------------------
# GET /api/pictograms
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_pictograms_returns_200(client):
    # Arrange
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category=None,
    )

    # Act
    response = await client.get("/api/pictograms")

    # Assert: each item has both text and pictogram fields
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["text"] == "Cheese"
    assert "pictogram" in data[0]
