from typing import Optional

from beanie import Document
from pydantic import HttpUrl


class Word(Document):
    word: str
    word_fr: str
    pictogram: HttpUrl
    asl_video: HttpUrl
    category: Optional[str] = None

    class Settings:
        collection = "words"
