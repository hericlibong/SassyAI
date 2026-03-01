from fastapi import APIRouter


router = APIRouter()


@router.get("/api/health")
async def get_health() -> dict[str, str]:
    return {"status": "ok"}
