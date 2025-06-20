import pytest
from pydantic import HttpUrl, ValidationError

from models.category import CategoryCreate


def test_category_create():
    """Test creating a valid category"""
    category = CategoryCreate(
        en="Food", fr="Nourriture", pictogram=HttpUrl("http://example.com/food.jpg")
    )

    assert category.en == "Food"
    assert category.fr == "Nourriture"
    assert category.pictogram == HttpUrl("http://example.com/food.jpg")


def test_category_create_missing_fields():
    """Test creating a category with missing fields fails"""
    with pytest.raises(ValidationError):
        CategoryCreate(en="Food")  # type: ignore

    with pytest.raises(ValidationError):
        CategoryCreate(en="Food", fr="Nourriture")  # type: ignore
