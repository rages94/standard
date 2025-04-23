from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer

from src.config import Settings
from src.data.models import Liability
from src.data.models.liability import LiabilityCreate, LiabilityUpdate
from src.data.uow import UnitOfWork

settings = Settings()
liability_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@liability_router.post(
    "/",
    responses={201: {"model": Liability}},
)
@inject
async def create_liability(
    body: LiabilityCreate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> Liability:
    user_id = credentials["id"]
    async with uow:
        liability = Liability(
            liability_template_id=body.liability_template_id,
            count=body.count,
            user_id=user_id
        )
        uow.liability_repo.add(liability)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        await uow.commit()
        await uow.refresh(liability)
    return liability


@liability_router.get(
    "/",
    responses={200: {"model": list[Liability]}},
)
@inject
async def list_liabilities(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[Liability]:
    async with uow:
        liabilities = await uow.liability_repo.filter({"user_id": credentials["id"]})
    return liabilities


@liability_router.patch(
    "/{liability_id}",
    responses={200: {"model": Liability}},
)
@inject
async def update_liability(
    liability_id: UUID,
    body: LiabilityUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> Liability:
    user_id = credentials["id"]
    async with uow:
        liability = await uow.liability_repo.get_one(
            {"id": liability_id, "user_id": user_id}
        )
        for k, v in body.model_dump(exclude_none=True).items():
            setattr(liability, k, v)
        uow.liability_repo.add(liability)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        await uow.commit()
        await uow.refresh(liability)
    return liability


@liability_router.delete(
    "/{liability_id}",
    status_code=204,
)
@inject
async def delete_liability(
    liability_id: UUID,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> None:
    user_id = credentials["id"]
    async with uow:
        await uow.liability_repo.get_one(
            {"id": liability_id, "user_id": user_id}
        )
        await uow.liability_repo.delete(liability_id)
        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        await uow.commit()
