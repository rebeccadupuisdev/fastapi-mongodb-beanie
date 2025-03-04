from pydantic import HttpUrl

from models.word import Word


async def find_word_en(word_en: str) -> Word | None:

    word_en = word_en.strip().lower().capitalize()
    return await Word.find_one(Word.en == word_en)


async def create_word(
    word_en: str,
    word_fr: str,
    pictogram: HttpUrl,
    asl_video: HttpUrl,
    category: str | None,
):
    if existing_word := await find_word_en(word_en):
        print(f"Word {existing_word.en} already exists!")
        return existing_word

    word_en = word_en.strip().lower().capitalize()
    word_fr = word_fr.strip().lower().capitalize()
    category = category.strip().lower().capitalize() if category else None

    word = Word(
        en=word_en,
        fr=word_fr,
        pictogram=pictogram,
        asl_video=asl_video,
        category=category,
    )

    await word.save()

    print(f"New word created: {word.en}")

    return word
