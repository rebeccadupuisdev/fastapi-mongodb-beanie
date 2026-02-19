import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import find_category
from services.word_service import find_word

router = fastapi.APIRouter()


@router.get("/word/{word}", response_class=HTMLResponse)
async def get_word_page(request: Request, word: str):
    found = await find_word(word)
    if not found:
        return HTMLResponse(content="Word not found", status_code=404)

    category = None
    if found.category:
        category = await find_category(found.category)

    return templates.TemplateResponse(
        "word.html", {"request": request, "word": found, "category": category}
    )
