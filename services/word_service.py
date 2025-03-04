from models.word import Word


async def find_word_en(word_en: str) -> Word | None:

    word_en = word_en.strip().lower().capitalize()
    return await Word.find_one(Word.en == word_en)
