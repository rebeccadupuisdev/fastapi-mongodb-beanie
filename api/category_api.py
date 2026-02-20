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
        raise fastapi.HTTPException(
            status_code=404, detail=f"Category {category.title()} not found"
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
    if not new_category:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"Category {category.text} not created, parent category not found",
        )
    return new_category
