from pydantic import HttpUrl

from models.word import Word


async def find_word_en(word_en: str) -> Word | None:

    word_en = word_en.strip().capitalize()
    return await Word.find_one(Word.en == word_en)


async def create_word(
    en: str,
    fr: str,
    pictogram: HttpUrl,
    asl_video: HttpUrl,
    category: str | None,
):
    if existing_word := await find_word_en(en):
        print(f"Word {existing_word.en} already exists!")
        return existing_word

    en = en.strip().capitalize()
    fr = fr.strip().capitalize()
    category = category.strip().capitalize() if category else None

    word = Word(
        en=en,
        fr=fr,
        pictogram=pictogram,
        asl_video=asl_video,
        category=category,
    )

    await word.save()

    print(f"New word created: {word.en}")

    return word
