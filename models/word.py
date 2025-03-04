from beanie import Document
from pydantic import BaseModel, HttpUrl


class WordCreate(BaseModel):
    en: str
    fr: str
    pictogram: HttpUrl
    asl_video: HttpUrl
    category: str | None = None


class Word(WordCreate, Document):

    class Settings:
        name = "words"
