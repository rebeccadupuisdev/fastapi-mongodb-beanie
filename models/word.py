from typing import Optional

from beanie import Document
from pydantic import HttpUrl


class Word(Document):
    en: str
    fr: str
    pictogram: HttpUrl
    asl_video: HttpUrl
    category: Optional[str] = None

    class Settings:
        name = "words"
