from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Security, Depends
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer

from src.config import Settings
from src.data.models.liability_template import LiabilityTemplateCreate, LiabilityTemplate, LiabilityTemplateUpdate
from src.data.uow import UnitOfWork

settings = Settings()
liability_template_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@liability_template_router.post(
    "/",
    responses={201: {"model": LiabilityTemplate}},
)
@inject
async def create_liability_template(
    body: LiabilityTemplateCreate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> LiabilityTemplate:
    async with uow:
        liability_template = LiabilityTemplate(
            name=body.name,
            count=body.count,
            user_id=credentials["id"]
        )
        uow.liability_template_repo.add(liability_template)
        await uow.commit()
        await uow.refresh(liability_template)
    return liability_template


@liability_template_router.get(
    "/",
    responses={200: {"model": list[LiabilityTemplate]}},
)
@inject
async def list_liability_templates(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[LiabilityTemplate]:
    async with uow:
        return await uow.liability_template_repo.filter(dict(user_id=credentials["id"]))


@liability_template_router.patch(
    "/{liability_template_id}",
    responses={200: {"model": LiabilityTemplate}},
)
@inject
async def update_liability_template(
    liability_template_id: UUID,
    body: LiabilityTemplateUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> LiabilityTemplate:
    user_id = credentials["id"]
    async with uow:
        liability_template = await uow.liability_template_repo.get_one(
            {"id": liability_template_id, "user_id": user_id}
        )
        for k, v in body.model_dump(exclude_none=True).items():
            setattr(liability_template, k, v)
        uow.liability_template_repo.add(liability_template)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        await uow.commit()
        await uow.refresh(liability_template)
    return liability_template


@liability_template_router.delete(
    "/{liability_template_id}",
    status_code=204,
)
@inject
async def delete_liability_template(
    liability_template_id: UUID,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> None:
    async with uow:
        liability_template = await uow.liability_template_repo.get_one(
            {"id": liability_template_id, "user_id": credentials["id"]}
        )
        liability_template.is_deleted = True
        uow.liability_template_repo.add(liability_template)
        await uow.commit()
