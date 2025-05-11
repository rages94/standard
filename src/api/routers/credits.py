from datetime import datetime

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends, Query
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer

from src.config import Settings
from src.data.models import Credit
from src.data.uow import UnitOfWork
from src.domain.credits.dto.output import CreditListResponse

settings = Settings()
credit_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@credit_router.get(
    "/current/",
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


@credit_router.get(
    "/",
    responses={201: {"model": CreditListResponse}},
)
@inject
async def list_credits(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
    limit: int = Query(10),
    offset: int = Query(0),
) -> CreditListResponse:
    params = dict(
        user_id=credentials["id"],
        pagination=(limit, offset)
    )
    async with uow:
        count = await uow.credit_repo.count(params)
        credits = await uow.credit_repo.filter(params)
    return CreditListResponse(
        data=credits,
        count=count,
        next_page=count > limit + offset
    )
