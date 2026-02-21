from typing import Optional

from models.category import Category
from models.word import Word, WordPictogramView, WordShortView
from services.category_service import find_category


async def find_word(word: str) -> Optional[Word]:
    word_found = await Word.find_one(Word.text == word.strip().title())
    if word_found and word_found.category:
        word_found.category = await Category.get(word_found.category.ref.id)
    return word_found


async def create_word(
    text: str,
    pictogram: str,
    asl_video: str,
    category: str | None,
):
    if existing_word := await Word.find_one(Word.text == text.strip().title()):
        print(f"Word {existing_word.text} already exists!")
        return existing_word

    if category:
        existing_category = await find_category(category)
        if not existing_category:
            print(f"Category {category} not found!")
            return None
        category = existing_category

    text = text.strip().title()

    word = Word(
        text=text,
        pictogram=pictogram,
        asl_video=asl_video,
        category=category,
    )

    await word.save()

    print(f"New word created: {word.text}")

    return word


async def get_words():
    return await Word.find().project(WordShortView).to_list()


async def get_pictograms():
    return await Word.find().project(WordPictogramView).to_list()


async def delete_word(word: str):
    found = await find_word(word)
    if found:
        await found.delete()


async def get_words_by_category(category: Category) -> list[Word]:
    words = await Word.find(Word.category.id == category.id).to_list()
    return words
