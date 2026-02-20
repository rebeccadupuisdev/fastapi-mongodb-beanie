from beanie import Document, Link
from pydantic import BaseModel, Field, HttpUrl

from models.category import Category


class BaseWord(BaseModel):
    text: str = Field(
        ..., title="Word in english", json_schema_extra={"example": "Cheese"}
    )
    pictogram: HttpUrl = Field(
        ...,
        title="Link of the pictogram image",
        json_schema_extra={"example": "http://example.com/cheese.jpg"},
    )
    asl_video: HttpUrl = Field(
        ...,
        title="Link of the ASL video",
        json_schema_extra={"example": "http://example.com/cheese.mp4"},
    )


class WordCreate(BaseWord):
    category: str | None = Field(
        None, title="Category for the word", json_schema_extra={"example": "Food"}
    )


class Word(BaseWord, Document):
    category: Link["Category"] | None = None

    class Settings:
        name = "words"


class WordShortView(BaseModel):
    text: str


class WordPictogramView(BaseModel):
    text: str
    pictogram: HttpUrl
