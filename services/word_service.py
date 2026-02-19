from typing import Optional

from models.word import Word, WordPictogramView, WordShortView


async def find_word(word: str) -> Optional[Word]:
    return await Word.find_one(Word.text == word.strip().title())


async def create_word(
    text: str,
    pictogram: str,
    asl_video: str,
    category: str | None,
):
    if existing_word := await find_word(text):
        print(f"Word {existing_word.text} already exists!")
        return existing_word

    text = text.strip().title()
    category = category.strip().title() if category else None

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


async def get_words_by_category(category: str) -> list[Word]:
    words = await Word.find(Word.category == category.strip().title()).to_list()
    return words
