import pytest
from pydantic import HttpUrl

from services.category_service import (
    create_category,
    delete_category,
    find_category,
    get_categories,
    get_categories_by_parent_category,
    get_category_ancestors,
)
from services.word_service import create_word, find_word

# ---------------------------------------------------------------------------
# create_category
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category():
    """Happy path: a new category is created and returned."""
    category = await create_category(
        text="Food",
        pictogram="http://example.com/food.jpg",
    )

    assert category is not None
    assert category.text == "Food"
    assert category.pictogram == HttpUrl("http://example.com/food.jpg")


@pytest.mark.asyncio(loop_scope="session")
async def test_create_duplicate_category_returns_existing():
    """Creating a category that already exists returns the original, unchanged."""
    first = await create_category(text="Food", pictogram="http://example.com/food.jpg")
    second = await create_category(
        text="Food", pictogram="http://example.com/other.jpg"
    )

    assert second.id == first.id
    assert second.pictogram == first.pictogram


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_with_parent():
    """When the parent exists the child is linked to it."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    child = await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )

    assert child is not None
    assert child.text == "Sweets"
    assert child.parent_category is not None


@pytest.mark.asyncio(loop_scope="session")
async def test_create_category_parent_not_found_returns_none():
    """When the requested parent does not exist the service returns None."""
    result = await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="NonExistent",
    )

    assert result is None


# ---------------------------------------------------------------------------
# find_category
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_returns_category_when_found():
    """A category that exists is returned by its exact name."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    category = await find_category("Food")

    assert category is not None
    assert category.text == "Food"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_normalises_whitespace_and_case():
    """find_category strips whitespace and title-cases the input before querying."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    category = await find_category("  fOoD  ")

    assert category is not None
    assert category.text == "Food"


@pytest.mark.asyncio(loop_scope="session")
async def test_find_category_returns_none_when_not_found():
    """Looking up a name that does not exist returns None, not an exception."""
    category = await find_category("NonExistent")

    assert category is None


# ---------------------------------------------------------------------------
# get_categories
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_returns_empty_list_when_no_categories_exist():
    """get_categories on an empty collection returns [] not None."""
    categories = await get_categories()

    assert categories == []


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_returns_all_categories():
    """Every inserted category is included in the result."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_category(text="Animals", pictogram="http://example.com/animals.jpg")

    categories = await get_categories()

    assert len(categories) == 2
    assert {c.text for c in categories} == {"Food", "Animals"}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_excludes_child_categories():
    """Child categories are not included in the top-level listing."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )

    categories = await get_categories()

    assert len(categories) == 1
    assert categories[0].text == "Food"


# ---------------------------------------------------------------------------
# delete_category
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_removes_it():
    """A category can no longer be found after deletion."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")

    await delete_category("Food")

    assert await find_category("Food") is None


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_not_found_does_not_raise():
    """Deleting a category that does not exist is a silent no-op."""
    await delete_category("NonExistent")


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_nullifies_words():
    """Words that belonged to the deleted category become uncategorized."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_word(
        text="Cheese",
        pictogram="http://example.com/cheese.jpg",
        asl_video="http://example.com/cheese.mp4",
        category="Food",
    )

    await delete_category("Food")

    cheese = await find_word("Cheese")
    assert cheese is not None
    assert cheese.category is None


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_category_nullifies_child_categories():
    """Sub-categories of the deleted category lose their parent link."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )

    await delete_category("Food")

    sweets = await find_category("Sweets")
    assert sweets is not None
    assert sweets.parent_category is None


# ---------------------------------------------------------------------------
# get_categories_by_parent_category
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_by_parent_category():
    """Only direct children of the given category are returned."""
    parent = await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )
    await create_category(
        text="Fruits",
        pictogram="http://example.com/fruits.jpg",
        parent_category="Food",
    )
    children = await get_categories_by_parent_category(parent)

    assert len(children) == 2
    assert {c.text for c in children} == {"Sweets", "Fruits"}


@pytest.mark.asyncio(loop_scope="session")
async def test_get_categories_by_parent_category_returns_empty_when_no_children():
    """A category with no children returns [] not None."""
    parent = await create_category(text="Food", pictogram="http://example.com/food.jpg")

    children = await get_categories_by_parent_category(parent)

    assert children == []


# ---------------------------------------------------------------------------
# get_category_ancestors
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_ancestors_returns_empty_for_root():
    """A root category (no parent) has no ancestors."""
    root = await create_category(text="Food", pictogram="http://example.com/food.jpg")

    ancestors = await get_category_ancestors(root)

    assert ancestors == []


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_ancestors_returns_parent():
    """A category one level deep returns a list containing only its parent."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    child = await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )

    ancestors = await get_category_ancestors(child)

    assert len(ancestors) == 1
    assert ancestors[0].text == "Food"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_category_ancestors_returns_ordered_chain():
    """Ancestors are returned root-first for a multi-level hierarchy."""
    await create_category(text="Food", pictogram="http://example.com/food.jpg")
    await create_category(
        text="Sweets",
        pictogram="http://example.com/sweets.jpg",
        parent_category="Food",
    )
    grandchild = await create_category(
        text="Chocolate",
        pictogram="http://example.com/chocolate.jpg",
        parent_category="Sweets",
    )

    ancestors = await get_category_ancestors(grandchild)

    assert len(ancestors) == 2
    assert ancestors[0].text == "Food"  # root comes first
    assert ancestors[1].text == "Sweets"  # then the immediate parent
