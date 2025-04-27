from datetime import datetime

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer

from src.config import Settings
from src.data.models import Credit
from src.data.uow import UnitOfWork

settings = Settings()
credit_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@credit_router.get(
    "/",
    responses={201: {"model": Credit}},
)
@inject
async def get_credit(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> Credit:
    user_id = credentials["id"]
    async with uow:
        return await uow.credit_repo.get_one(dict(user_id=user_id, deadline_date_ge=datetime.now()))
