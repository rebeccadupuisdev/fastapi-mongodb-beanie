import pytest
import pytest_asyncio
from pydantic import HttpUrl

from services.word_service import (
    create_word,
    delete_word,
    find_word,
    get_pictograms,
    get_words,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word():
    """Test inserting an item into the database"""
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
    """Test getting all items from the database"""

    words = await get_words()

    for i, word in enumerate(words):
        assert word.text == base_data[i].get("text")

    assert len(words) == len(base_data)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_word(base_data):
    await delete_word(base_data[0].get("text"))

    word = await find_word(base_data[0].get("text"))
    words = await get_words()

    assert word is None
    assert len(words) == len(base_data) - 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_pictograms(base_data):
    """Test getting all pictograms from the database"""

    words = await get_pictograms()

    for i, word in enumerate(words):
        assert word.text == base_data[i].get("text")
        assert str(word.pictogram) == base_data[i].get("pictogram")

    assert len(words) == len(base_data)
