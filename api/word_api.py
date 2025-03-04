import fastapi

from models.word import Word
from services.word_service import find_word_en

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
