import fastapi

from models.category import Category, CategoryCreate
from services.category_service import create_category, find_category_en

router = fastapi.APIRouter()


@router.get(
    "/api/categories/en/{category_en}",
    name="Find Category EN",
    response_model=Category,
    tags=["Category"],
)
async def api_find_category_en(category_en: str):
    category = await find_category_en(category_en)
    if not category:
        return fastapi.responses.JSONResponse(
            {"error": f"Category {category_en.title()} not found"}, status_code=404
        )
    return category


@router.post(
    "/api/categories",
    name="Create Category",
    response_model=Category,
    tags=["Category"],
)
async def api_create_category(category: CategoryCreate):
    new_category = await create_category(**category.model_dump())
    return new_category
