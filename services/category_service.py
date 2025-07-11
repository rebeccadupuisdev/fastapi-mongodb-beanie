from typing import Optional

from pydantic import HttpUrl

from models.category import Category


async def find_category_en(category_en: str) -> Optional[Category]:
    category = await Category.find_one(Category.en == category_en.strip().title())
    return category


async def create_category(
    en: str,
    fr: str,
    pictogram: HttpUrl,
):
    if existing_category := await find_category_en(en):
        print(f"Category {existing_category.en} already exists!")
        return existing_category

    en = en.strip().title()
    fr = fr.strip().title()

    category = Category(
        en=en,
        fr=fr,
        pictogram=pictogram,
    )

    await category.insert()

    print(f"New category created: {category.en}")

    return category


async def get_categories() -> list[Category]:
    categories = await Category.find_all().to_list()
    return categories
