from typing import Optional

from models.category import Category


async def find_category(category: str) -> Optional[Category]:
    return await Category.find_one(Category.text == category.strip().title())


async def create_category(
    text: str,
    pictogram: str,
    parent_category: str | None = None,
):
    if existing_category := await find_category(text):
        print(f"Category {existing_category.text} already exists!")
        return existing_category

    if parent_category:
        existing_parent_category = await find_category(parent_category)
        if not existing_parent_category:
            print(f"Parent category {parent_category} not found!")
            return None
        parent_category = existing_parent_category

    text = text.strip().title()

    category = Category(
        text=text,
        pictogram=pictogram,
        parent_category=parent_category,
    )

    await category.insert()

    print(f"New category created: {category.text}")

    return category


async def get_categories() -> list[Category]:
    categories = await Category.find(
        Category.parent_category == None  # noqa: E711
    ).to_list()
    return categories


async def get_categories_by_parent_category(category: Category) -> list[Category]:
    return await Category.find(Category.parent_category.id == category.id).to_list()


async def get_category_ancestors(category: Category) -> list[Category]:
    ancestors = []
    current = category
    while current.parent_category is not None:
        if isinstance(current.parent_category, Category):
            parent = await Category.get(current.parent_category.id)
        else:
            parent = await Category.get(current.parent_category.ref.id)
        ancestors.insert(0, parent)  # prepend so root comes first
        current = parent
    return ancestors


async def delete_category(category: str):
    found = await find_category(category)
    if found:
        await found.delete()
