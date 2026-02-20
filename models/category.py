from beanie import Document, Link
from pydantic import BaseModel, Field, HttpUrl


class BaseCategory(BaseModel):
    text: str = Field(
        ..., title="Category name", json_schema_extra={"example": "Sweets"}
    )
    pictogram: HttpUrl = Field(
        ...,
        title="Link of the pictogram image",
        json_schema_extra={"example": "http://example.com/food.jpg"},
    )


class CategoryCreate(BaseCategory):
    parent_category: str | None = Field(
        None, title="Parent category", json_schema_extra={"example": "Food"}
    )


class Category(BaseCategory, Document):
    parent_category: Link["Category"] | None = None

    class Settings:
        name = "categories"
