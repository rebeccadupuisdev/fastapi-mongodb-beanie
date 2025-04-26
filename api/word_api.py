import fastapi

from models.word import Word, WordCreate
from services.word_service import create_word, find_word_en, get_words

router = fastapi.APIRouter()


@router.get("/api")
def api():
    return {"message": "Hello API!"}


@router.get("/api/words/en/{word_en}", response_model=Word)
async def word(word_en: str):
    word = await find_word_en(word_en)
    if not word:
        return fastapi.responses.JSONResponse(
            {"error": f"Word {word_en.capitalize()} not found"}, status_code=404
        )
    return word


@router.post("/api/words", response_model=Word)
async def word(word: WordCreate):
    new_word = await create_word(**word.model_dump())
    return new_word


@router.get("/api/words")
async def word():
    words = await get_words()
    return words
