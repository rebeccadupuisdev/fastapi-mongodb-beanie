from beanie import Document, Link
from pydantic import BaseModel, Field, HttpUrl


class CategoryCreate(BaseModel):
    text: str = Field(..., title="Category name", json_schema_extra={"example": "Food"})
    pictogram: HttpUrl = Field(
        ...,
        title="Link of the pictogram image",
        json_schema_extra={"example": "http://example.com/food.jpg"},
    )


class Category(CategoryCreate, Document):
    parent_category: Link["Category"] | None = None

    class Settings:
        name = "categories"
