import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import get_category_ancestors
from services.word_service import find_word

router = fastapi.APIRouter()


@router.get("/word/{word}", response_class=HTMLResponse)
async def get_word_page(request: Request, word: str):
    word_found = await find_word(word)
    if not word_found:
        return HTMLResponse(content="Word not found", status_code=404)

    ancestors = await get_category_ancestors(word_found.category)

    return templates.TemplateResponse(
        "word.html",
        {
            "request": request,
            "word": word_found,
            "category": word_found.category,
            "ancestors": ancestors,
        },
    )
