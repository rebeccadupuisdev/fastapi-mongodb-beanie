from beanie import Document
from pydantic import BaseModel, Field, HttpUrl


class CategoryCreate(BaseModel):
    en: str = Field(
        ..., title="Category in english", json_schema_extra={"example": "Food"}
    )
    fr: str = Field(
        ..., title="Category in french", json_schema_extra={"example": "Nourriture"}
    )
    pictogram: HttpUrl = Field(
        ...,
        title="Link of the pictogram image",
        json_schema_extra={"example": "http://example.com/food.jpg"},
    )


class Category(CategoryCreate, Document):

    class Settings:
        name = "categories"
