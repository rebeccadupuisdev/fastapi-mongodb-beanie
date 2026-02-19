import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import find_category
from services.word_service import get_words_by_category

router = fastapi.APIRouter()


@router.get("/category/{category}", response_class=HTMLResponse)
async def get_category_page(request: Request, category: str):
    found = await find_category(category)
    if not found:
        return HTMLResponse(content="Category not found", status_code=404)

    words = await get_words_by_category(category)
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": found, "words": words}
    )
