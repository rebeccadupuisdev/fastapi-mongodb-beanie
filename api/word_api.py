import fastapi

from models.word import Word, WordCreate
from services.word_service import (
    create_word,
    delete_word_en,
    find_word_en,
    get_pictograms,
    get_words,
)

router = fastapi.APIRouter()


@router.get(
    "/api/words/en/{word_en}", name="Find Word EN", response_model=Word, tags=["Word"]
)
async def api_find_word_en(word_en: str):
    word = await find_word_en(word_en)
    if not word:
        return fastapi.responses.JSONResponse(
            {"error": f"Word {word_en.title()} not found"}, status_code=404
        )
    return word


@router.delete("/api/words/en/{word_en}", name="Delete Word EN", tags=["Word"])
async def api_delete_word(word_en: str):
    await delete_word_en(word_en)


@router.post("/api/words", name="Create Word", response_model=Word, tags=["Word"])
async def api_create_word(word: WordCreate):
    new_word = await create_word(**word.model_dump())
    return new_word


@router.get("/api/pictograms", name="Get Pictograms", tags=["Word"])
async def api_get_pictograms():
    pictograms = await get_pictograms()
    return pictograms


@router.get("/api/words", name="Get Words", tags=["Word"])
async def api_get_words():
    words = await get_words()
    return words
