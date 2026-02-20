import pytest
import pytest_asyncio
from pydantic import HttpUrl

from services.category_service import create_category
from services.word_service import (
    create_word,
    delete_word,
    find_word,
    get_pictograms,
    get_words,
    get_words_by_category,
)

# ---------------------------------------------------------------------------
# create_word
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word():
    """Happy path: a new word is created and returned."""
    new_word = await create_word(
        text="Cheese",
        pictogram="http://example.com/image.jpg",
        asl_video="http://example.com/video.mp4",
        category=None,
    )

    assert new_word is not None
    assert new_word.text == "Cheese"
    assert new_word.pictogram == HttpUrl("http://example.com/image.jpg")
    assert new_word.asl_video == HttpUrl("http://example.com/video.mp4")
    assert new_word.category is None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word_with_category():
    """When the category exists the word is linked to it."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    word = await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category="Food",
    )

    assert word is not None
    assert word.text == "Cheese"
    assert word.category is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word_category_not_found_returns_none():
    """When the requested category does not exist the service returns None."""
    result = await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category="NonExistent",
    )

    assert result is None


# ---------------------------------------------------------------------------
# find_word
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_find_word_returns_none_when_not_found():
    """Looking up a word that does not exist returns None, not an exception."""
    result = await find_word("NonExistent")

    assert result is None


@pytest.mark.asyncio(loop_scope="session")
async def test_find_word_with_category_resolves_category_link():
    """
    find_word fetches and populates the linked Category document.
    This tests the branch in word_service.py that calls Category.get().
    """
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category="Food",
    )

    # Arrange: word exists in DB with a category reference
    # Act: find_word must resolve that reference into a full Category object
    word = await find_word("Cheese")

    # Assert: the category is not a raw reference — it is a populated document
    assert word is not None
    assert word.category is not None
    assert word.category.text == "Food"


# ---------------------------------------------------------------------------
# get_words / get_pictograms
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def base_data():
    data = [
        {
            "text": "Cheese",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
        {
            "text": "Ice Cream",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
        {
            "text": "Water",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
    ]

    for item in data:
        await create_word(
            text=item["text"],
            pictogram=item["pictogram"],
            asl_video=item["asl_video"],
            category=None,
        )

    return data


@pytest.mark.asyncio(loop_scope="session")
async def test_get_words(base_data):
    """get_words returns one entry per word; order is not asserted."""
    words = await get_words()

    assert len(words) == len(base_data)
    # Use a set so the assertion does not depend on MongoDB return order
    assert {w.text for w in words} == {item["text"] for item in base_data}


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_word(base_data):
    first_text = base_data[0]["text"]
    await delete_word(first_text)

    assert await find_word(first_text) is None
    assert len(await get_words()) == len(base_data) - 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_pictograms(base_data):
    """get_pictograms returns text + pictogram for each word; order is not asserted."""
    words = await get_pictograms()

    assert len(words) == len(base_data)
    expected = {(item["text"], item["pictogram"]) for item in base_data}
    actual = {(w.text, str(w.pictogram)) for w in words}
    assert actual == expected


# ---------------------------------------------------------------------------
# get_words_by_category
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_words_by_category():
    """Only words linked to the given category are returned."""
    food = await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category="Food",
    )
    await create_word(
        text="Bread",
        pictogram="http://example.com/bread.jpg",
        asl_video="http://example.com/bread.mp4",
        category="Food",
    )

    words = await get_words_by_category(food)

    assert len(words) == 2
    assert {w.text for w in words} == {"Cheese", "Bread"}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_words_by_category_returns_empty_list_when_no_words():
    """A category with no words returns [] not None."""
    food = await create_category(text="Food", pictogram="http://example.com/food.jpg")

    words = await get_words_by_category(food)

    assert words == []
