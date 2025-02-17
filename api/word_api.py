import fastapi

router = fastapi.APIRouter()


@router.get("/api")
def api():
    return {"Hello API!"}
