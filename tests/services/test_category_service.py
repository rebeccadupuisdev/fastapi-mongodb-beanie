import pytest
import pytest_asyncio
from pydantic import HttpUrl

from services.category_service import create_category, find_category


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category():
    """Test creating a new category"""
    category = await create_category(
        text="Food",
        pictogram="http://example.com/food.jpg",
    )

    assert category is not None
    assert category.text == "Food"
    assert category.pictogram == HttpUrl("http://example.com/food.jpg")


@pytest.mark.asyncio(loop_scope="session")
async def test_create_duplicate_category():
    """Test creating a duplicate category returns existing one"""
    first_category = await create_category(
        text="Food",
        pictogram="http://example.com/food.jpg",
    )

    second_category = await create_category(
        text="Food",
        pictogram="http://example.com/different.jpg",
    )

    assert second_category.id == first_category.id
    assert second_category.pictogram == first_category.pictogram


@pytest_asyncio.fixture
async def base_categories():
    """Create some base categories for testing"""
    categories_data = [
        {
            "text": "Food",
            "pictogram": "http://example.com/food.jpg",
        },
        {
            "text": "Animals",
            "pictogram": "http://example.com/animals.jpg",
        },
        {
            "text": "Colors",
            "pictogram": "http://example.com/colors.jpg",
        },
    ]

    created_categories = []
    for cat in categories_data:
        category = await create_category(
            text=cat["text"],
            pictogram=cat["pictogram"],
        )
        created_categories.append(category)

    return created_categories


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category(base_categories):
    """Test finding a category by name"""
    category = await find_category("Food")
    assert category is not None
    assert category.text == "Food"

    category = await find_category("  fOoD  ")
    assert category is not None
    assert category.text == "Food"

    category = await find_category("NonExistent")
    assert category is None
