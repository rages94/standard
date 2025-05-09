from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer

from src.config import Settings
from src.data.models import Standard
from src.data.models.standard import StandardUpdate, StandardCreate
from src.data.uow import UnitOfWork

settings = Settings()
standard_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@standard_router.post(
    "/",
    responses={201: {"model": Standard}},
)
@inject
async def create_standard(
    body: StandardCreate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> Standard:
    async with uow:
        standard = Standard(
            name=body.name,
            count=body.count,
        )
        uow.standard_repo.add(standard)
        await uow.commit()
        await uow.refresh(standard)
    return standard


@standard_router.get(
    "/",
    responses={200: {"model": list[Standard]}},
)
@inject
async def list_standards(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[Standard]:
    async with uow:
        return await uow.standard_repo.filter(dict(order={"created_at"}))


@standard_router.patch(
    "/{standard_id}",
    responses={200: {"model": Standard}},
)
@inject
async def update_standard(
    standard_id: UUID,
    body: StandardUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> Standard:
    async with uow:
        standard = await uow.standard_repo.get_one(
            {"id": standard_id}
        )
        for k, v in body.model_dump(exclude_none=True).items():
            setattr(standard, k, v)
        uow.standard_repo.add(standard)
        await uow.commit()
        await uow.refresh(standard)
    return standard


@standard_router.delete(
    "/{standard_id}",
    status_code=204,
)
@inject
async def delete_standard(
    standard_id: UUID,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> None:
    async with uow:
        standard = await uow.standard_repo.get_one(
            {"id": standard_id}
        )
        standard.is_deleted = True
        uow.standard_repo.add(standard)
        await uow.commit()
