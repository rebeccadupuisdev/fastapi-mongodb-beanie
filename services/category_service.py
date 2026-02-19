from typing import Optional

from models.category import Category


async def find_category(category: str) -> Optional[Category]:
    return await Category.find_one(Category.text == category.strip().title())


async def create_category(
    text: str,
    pictogram: str,
):
    if existing_category := await find_category(text):
        print(f"Category {existing_category.text} already exists!")
        return existing_category

    text = text.strip().title()

    category = Category(
        text=text,
        pictogram=pictogram,
    )

    await category.insert()

    print(f"New category created: {category.text}")

    return category


async def get_categories() -> list[Category]:
    categories = await Category.find_all().to_list()
    return categories
