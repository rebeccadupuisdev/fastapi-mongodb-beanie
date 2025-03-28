from beanie import Document
from pydantic import BaseModel, Field, HttpUrl


class WordCreate(BaseModel):
    en: str = Field(..., title="Word in english", example="Cheese")
    fr: str = Field(..., title="Word in french", example="Fromage")
    pictogram: HttpUrl = Field(
        ...,
        title="Link of the pictogram image",
        example="http://example.com/cheese.jpg",
    )
    asl_video: HttpUrl = Field(
        ..., title="Link of the ASL video", example="http://example.com/cheese.mp4"
    )
    category: str | None = Field(None, title="Category for the word", example="Food")


class Word(WordCreate, Document):

    class Settings:
        name = "words"
