from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/")
def health():
    return {"status": "ok"}
