from beanie import Document
from pydantic import BaseModel, Field, HttpUrl


class WordCreate(BaseModel):
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
    category: str | None = Field(
        None, title="Category for the word", json_schema_extra={"example": "Food"}
    )


class Word(WordCreate, Document):
    class Settings:
        name = "words"


class WordShortView(BaseModel):
    text: str


class WordPictogramView(BaseModel):
    text: str
    pictogram: HttpUrl
