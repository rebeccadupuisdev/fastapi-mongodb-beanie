from pydantic import HttpUrl

from models.word import WordCreate


def test_word_create():
    w = WordCreate(
        text="Cheese",
        pictogram=HttpUrl("http://example.com/image.jpg"),
        asl_video=HttpUrl("http://example.com/video.mp4"),
        category=None,
    )
    assert w.text == "Cheese"
    assert w.pictogram == HttpUrl("http://example.com/image.jpg")
    assert w.asl_video == HttpUrl("http://example.com/video.mp4")
    assert w.category is None


def test_word_create_category():
    w = WordCreate(
        text="Cheese",
        pictogram=HttpUrl("http://example.com/image.jpg"),
        asl_video=HttpUrl("http://example.com/video.mp4"),
        category="Food",
    )
    assert w.text == "Cheese"
    assert w.pictogram == HttpUrl("http://example.com/image.jpg")
    assert w.asl_video == HttpUrl("http://example.com/video.mp4")
    assert w.category == "Food"
