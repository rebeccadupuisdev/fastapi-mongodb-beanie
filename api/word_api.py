import fastapi

from models.word import Word, WordCreate
from services.word_service import (
    create_word,
    delete_word,
    find_word,
    get_pictograms,
    get_words,
)

router = fastapi.APIRouter()


@router.get(
    "/api/words/{word}", name="Find Word", response_model=Word, tags=["Word"]
)
async def api_find_word(word: str):
    found = await find_word(word)
    if not found:
        return fastapi.responses.JSONResponse(
            {"error": f"Word {word.title()} not found"}, status_code=404
        )
    return found


@router.delete("/api/words/{word}", name="Delete Word", tags=["Word"])
async def api_delete_word(word: str):
    await delete_word(word)


@router.post("/api/words", name="Create Word", response_model=Word, tags=["Word"])
async def api_create_word(word: WordCreate):
    new_word = await create_word(**word.model_dump(mode="json"))
    return new_word


@router.get("/api/pictograms", name="Get Pictograms", tags=["Word"])
async def api_get_pictograms():
    pictograms = await get_pictograms()
    return pictograms


@router.get("/api/words", name="Get Words", tags=["Word"])
async def api_get_words():
    words = await get_words()
    return words
