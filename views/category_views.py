import fastapi
from fastapi import Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import (
    find_category,
    get_categories_by_parent_category,
    get_category_ancestors,
)
from services.word_service import get_words_by_category

router = fastapi.APIRouter()


@router.get("/category/{category}", response_class=HTMLResponse)
async def get_category_page(request: Request, category: str):
    category_found = await find_category(category)
    if not category_found:
        return HTMLResponse(content="Category not found", status_code=404)

    categories = await get_categories_by_parent_category(category_found)
    ancestors = await get_category_ancestors(category_found)
    words = await get_words_by_category(category_found)
    return templates.TemplateResponse(
        "category.html",
        {
            "request": request,
            "category": category_found,
            "categories": categories,
            "ancestors": ancestors,
            "words": words,
        },
    )
