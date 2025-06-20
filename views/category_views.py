import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import find_category_en
from services.word_service import get_words_by_category

router = fastapi.APIRouter()


@router.get("/category/{category_en}", response_class=HTMLResponse)
async def get_category_page(request: Request, category_en: str):
    category = await find_category_en(category_en)
    if not category:
        return HTMLResponse(content="Category not found", status_code=404)

    words = await get_words_by_category(category_en)
    return templates.TemplateResponse(
        "category.html", {"request": request, "category": category, "words": words}
    )
