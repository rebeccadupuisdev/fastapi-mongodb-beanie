import pytest
from pydantic import HttpUrl, ValidationError

from models.category import CategoryCreate


def test_category_create():
    """Test creating a valid category"""
    category = CategoryCreate(
        text="Food", pictogram=HttpUrl("http://example.com/food.jpg")
    )

    assert category.text == "Food"
    assert category.pictogram == HttpUrl("http://example.com/food.jpg")


def test_category_create_missing_fields():
    """Test creating a category with missing fields fails"""
    with pytest.raises(ValidationError):
        CategoryCreate(text="Food")  # type: ignore
