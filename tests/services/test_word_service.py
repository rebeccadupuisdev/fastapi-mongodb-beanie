import pytest
from pydantic import HttpUrl

from models.word import WordCreate
from services.word_service import create_word


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
