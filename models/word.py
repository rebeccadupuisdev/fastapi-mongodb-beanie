from beanie import Document
from pydantic import HttpUrl


class Word(Document):
    en: str
    fr: str
    pictogram: HttpUrl
    asl_video: HttpUrl
    category: str | None = None

    class Settings:
        name = "words"
