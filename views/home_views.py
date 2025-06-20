from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from infrastructure.template_config import templates
from services.category_service import get_categories

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    categories = await get_categories()
    return templates.TemplateResponse(
        "index.html", {"request": request, "categories": categories}
    )
