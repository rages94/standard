from fastapi import APIRouter

from src.api.routers.achievements import achievement_router
from src.api.routers.completed_standards import completed_standard_router
from src.api.routers.credits import credit_router
from src.api.routers.health import health_router
from src.api.routers.liabilities import liability_router
from src.api.routers.liability_templates import liability_template_router
from src.api.routers.standards import standard_router
from src.api.routers.tokens import token_router
from src.api.routers.users import user_router


def include_routers() -> APIRouter:
    main_router = APIRouter()
    main_router.include_router(token_router, prefix="/tokens", tags=["Tokens"])
    main_router.include_router(user_router, prefix="/users", tags=["Users"])
    main_router.include_router(
        liability_router, prefix="/liabilities", tags=["Liabilities"]
    )
    main_router.include_router(
        liability_template_router,
        prefix="/liability_templates",
        tags=["Liability templates"],
    )
    main_router.include_router(
        completed_standard_router,
        prefix="/completed_standards",
        tags=["Completed standards"],
    )
    main_router.include_router(standard_router, prefix="/standards", tags=["Standards"])
    main_router.include_router(credit_router, prefix="/credits", tags=["Credits"])
    main_router.include_router(
        achievement_router, prefix="/achievements", tags=["Achievements"]
    )
    main_router.include_router(health_router, prefix="/health", tags=["Health"])
    return main_router
