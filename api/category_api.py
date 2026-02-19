import fastapi

from models.category import Category, CategoryCreate
from services.category_service import create_category, find_category

router = fastapi.APIRouter()


@router.get(
    "/api/categories/{category}",
    name="Find Category",
    response_model=Category,
    tags=["Category"],
)
async def api_find_category(category: str):
    found = await find_category(category)
    if not found:
        return fastapi.responses.JSONResponse(
            {"error": f"Category {category.title()} not found"}, status_code=404
        )
    return found


@router.post(
    "/api/categories",
    name="Create Category",
    response_model=Category,
    tags=["Category"],
)
async def api_create_category(category: CategoryCreate):
    new_category = await create_category(**category.model_dump(mode="json"))
    return new_category
