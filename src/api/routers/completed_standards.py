from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends
from fastapi.params import Query
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer
from sqlalchemy.exc import NoResultFound

from src.config import Settings
from src.data.models import CompletedStandard
from src.data.models.completed_standard import CompletedStandardCreate, CompletedStandardUpdate
from src.data.uow import UnitOfWork
from src.domain.completed_standards.dto.output import GroupedCompletedStandard

settings = Settings()
completed_standard_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@completed_standard_router.post(
    "/",
    responses={201: {"model": CompletedStandard}},
)
@inject
async def create_completed_standard(
    body: CompletedStandardCreate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> CompletedStandard:
    user_id = credentials["id"]
    async with uow:
        standard = await uow.standard_repo.get_one(dict(id=body.standard_id))
        standard_count = body.count if not body.completed_type_is_count() else body.count // standard.count
        count = body.count if body.completed_type_is_count() else body.count * standard.count
        completed_standard = CompletedStandard(
            standard_id=body.standard_id,
            count=count,
            user_id=user_id,
        )
        uow.completed_standard_repo.add(completed_standard)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        try:
            await uow.credit_repo.update_completed_count(user_id, standard_count)
        except NoResultFound:
            pass
        await uow.commit()
        await uow.refresh(completed_standard)
    return completed_standard


@completed_standard_router.get(
    "/",
    responses={200: {"model": list[CompletedStandard]}},
)
@inject
async def list_completed_standards(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[CompletedStandard]:
    async with uow:
        return await uow.completed_standard_repo.filter({"user_id": credentials["id"]})


@completed_standard_router.get(
    "/grouped/",
    responses={200: {"model": GroupedCompletedStandard}},
)
@inject
async def list_grouped_completed_standards(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
    as_standard: bool = Query(False),
) -> GroupedCompletedStandard:
    async with uow:
        return await uow.completed_standard_repo.grouped_list(UUID(credentials["id"]), as_standard)


@completed_standard_router.patch(
    "/{completed_standard_id}",
    responses={200: {"model": CompletedStandard}},
)
@inject
async def update_completed_standard(
    completed_standard_id: UUID,
    body: CompletedStandardUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> CompletedStandard:
    user_id = credentials["id"]
    async with uow:
        completed_standard = await uow.completed_standard_repo.get_one(
            {"id": completed_standard_id, "user_id": user_id}
        )
        for k, v in body.model_dump(exclude_none=True).items():
            setattr(completed_standard, k, v)
        uow.completed_standard_repo.add(completed_standard)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)  # TODO events
        # TODO update credit
        await uow.commit()
        await uow.refresh(completed_standard)
    return completed_standard


@completed_standard_router.delete(
    "/{completed_standard_id}",
    status_code=204,
)
@inject
async def delete_completed_standard(
    completed_standard_id: UUID,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> None:
    user_id = credentials["id"]
    async with uow:
        await uow.completed_standard_repo.get_one(
            {"id": completed_standard_id, "user_id": user_id}
        )
        await uow.completed_standard_repo.delete(completed_standard_id)
        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)  # TODO events
        # TODO update credit
        await uow.commit()
