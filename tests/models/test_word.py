from pydantic import HttpUrl

from models.word import WordCreate


def test_word_create():
    w = WordCreate(
        en="Cheese",
        fr="Fromage",
        pictogram="http://example.com/image.jpg",
        asl_video="http://example.com/video.mp4",
    )
    assert w.en == "Cheese"
    assert w.fr == "Fromage"
    assert w.pictogram == HttpUrl("http://example.com/image.jpg")
    assert w.asl_video == HttpUrl("http://example.com/video.mp4")
    assert w.category is None


def test_word_create_category():
    w = WordCreate(
        en="Cheese",
        fr="Fromage",
        pictogram="http://example.com/image.jpg",
        asl_video="http://example.com/video.mp4",
        category="Food",
    )
    assert w.en == "Cheese"
    assert w.fr == "Fromage"
    assert w.pictogram == HttpUrl("http://example.com/image.jpg")
    assert w.asl_video == HttpUrl("http://example.com/video.mp4")
    assert w.category == "Food"
