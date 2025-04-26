import pytest
import pytest_asyncio
from pydantic import HttpUrl

from models.word import WordCreate
from services.word_service import (
    create_word,
    delete_word_en,
    find_word_en,
    get_pictograms,
    get_words,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_word():
    """Test inserting an item into the database"""
    w = WordCreate(
        en="Cheese",
        fr="Fromage",
        pictogram="http://example.com/image.jpg",
        asl_video="http://example.com/video.mp4",
    )

    new_word = await create_word(**w.model_dump())

    assert new_word is not None
    assert new_word.en == "Cheese"
    assert new_word.fr == "Fromage"
    assert new_word.pictogram == HttpUrl("http://example.com/image.jpg")
    assert new_word.asl_video == HttpUrl("http://example.com/video.mp4")
    assert new_word.category is None


@pytest_asyncio.fixture
async def base_data():

    data = [
        {
            "en": "Cheese",
            "fr": "Fromage",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
        {
            "en": "Ice Cream",
            "fr": "Crème Glacée",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
        {
            "en": "Water",
            "fr": "Eau",
            "pictogram": "http://example.com/image.jpg",
            "asl_video": "http://example.com/video.mp4",
        },
    ]

    for item in data:

        w = WordCreate(
            en=item.get("en"),
            fr=item.get("fr"),
            pictogram=item.get("pictogram"),
            asl_video=item.get("asl_video"),
        )

        await create_word(**w.model_dump())

    return data


@pytest.mark.asyncio(loop_scope="session")
async def test_get_words(base_data):
    """Test getting all items from the database"""

    words = await get_words()

    for i, word in enumerate(words):
        assert word.en == base_data[i].get("en")
        assert word.fr == base_data[i].get("fr")

    assert len(words) == len(base_data)


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_word_en(base_data):
    await delete_word_en(base_data[0].get("en"))

    word = await find_word_en(base_data[0].get("en"))
    words = await get_words()

    assert word is None
    assert len(words) == len(base_data) - 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_pictograms(base_data):
    """Test getting all pictograms from the database"""

    words = await get_pictograms()

    for i, word in enumerate(words):
        assert word.en == base_data[i].get("en")
        assert word.pictogram == HttpUrl(base_data[i].get("pictogram"))

    assert len(words) == len(base_data)
