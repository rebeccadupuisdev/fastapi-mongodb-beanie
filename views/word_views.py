import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import find_category_en
from services.word_service import find_word_en

router = fastapi.APIRouter()


@router.get("/word/{word_en}", response_class=HTMLResponse)
async def get_word_page(request: Request, word_en: str):
    word = await find_word_en(word_en)
    if not word:
        return HTMLResponse(content="Word not found", status_code=404)

    category = None
    if word.category:
        category = await find_category_en(word.category)

    return templates.TemplateResponse(
        "word.html", {"request": request, "word": word, "category": category}
    )
