import pytest
import pytest_asyncio
from pydantic import HttpUrl

from services.category_service import create_category, find_category_en


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category():
    """Test creating a new category"""
    category = await create_category(
        en="Food",
        fr="Nourriture",
        pictogram=HttpUrl("http://example.com/food.jpg"),
    )

    assert category is not None
    assert category.en == "Food"
    assert category.fr == "Nourriture"
    assert category.pictogram == HttpUrl("http://example.com/food.jpg")


@pytest.mark.asyncio(loop_scope="session")
async def test_create_duplicate_category():
    """Test creating a duplicate category returns existing one"""
    # Create first category
    first_category = await create_category(
        en="Food",
        fr="Nourriture",
        pictogram=HttpUrl("http://example.com/food.jpg"),
    )

    # Try to create duplicate
    second_category = await create_category(
        en="Food",
        fr="Different French",  # Even with different fr/pictogram, should return existing
        pictogram=HttpUrl("http://example.com/different.jpg"),
    )

    assert second_category.id == first_category.id
    assert second_category.fr == first_category.fr  # Should keep original French name
    assert (
        second_category.pictogram == first_category.pictogram
    )  # Should keep original pictogram


@pytest_asyncio.fixture
async def base_categories():
    """Create some base categories for testing"""
    categories_data = [
        {
            "en": "Food",
            "fr": "Nourriture",
            "pictogram": "http://example.com/food.jpg",
        },
        {
            "en": "Animals",
            "fr": "Animaux",
            "pictogram": "http://example.com/animals.jpg",
        },
        {
            "en": "Colors",
            "fr": "Couleurs",
            "pictogram": "http://example.com/colors.jpg",
        },
    ]

    created_categories = []
    for cat in categories_data:
        category = await create_category(
            en=cat["en"],
            fr=cat["fr"],
            pictogram=HttpUrl(cat["pictogram"]),
        )
        created_categories.append(category)

    return created_categories


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_en(base_categories):
    """Test finding a category by English name"""
    # Test finding existing category
    category = await find_category_en("Food")
    assert category is not None
    assert category.en == "Food"
    assert category.fr == "Nourriture"

    # Test with different case/spacing
    category = await find_category_en("  fOoD  ")
    assert category is not None
    assert category.en == "Food"

    # Test non-existent category
    category = await find_category_en("NonExistent")
    assert category is None
