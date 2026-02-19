from datetime import datetime
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security
from fastapi.params import Query
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials, JwtRefreshBearer
from sqlalchemy.exc import NoResultFound

from src.config import Settings
from src.data.models import CompletedStandard
from src.data.models.completed_standard import (
    CompletedStandardCreate,
    CompletedStandardUpdate,
)
from src.data.uow import UnitOfWork
from src.domain.achievements.use_cases.check_and_update import (
    CheckAndUpdateAchievements,
)
from src.domain.completed_standards.dto.output import (
    CompletedStandardListResponse,
    GroupedCompletedStandard,
    RatingGroupedCompletedStandard,
)
from src.domain.math.services.normalization import ExerciseNormalizationService

settings = Settings()
completed_standard_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)


@completed_standard_router.post(
    "/",
    status_code=201,
)
@inject
async def create_completed_standard(  # TODO check weightlifting(write tests)
    body: CompletedStandardCreate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    exercise_normalization: ExerciseNormalizationService = Depends(
        Provide["services.exercise_normalization"]
    ),
    check_and_update_achievements: CheckAndUpdateAchievements = Depends(
        Provide["use_cases.check_and_update_achievements"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> CompletedStandard:
    user_id = credentials["id"]
    async with uow:  # TODO use_case
        standard = await uow.standard_repo.get_one(dict(id=body.standard_id))

        if body.weight:
            normalization = exercise_normalization.normalization(
                body.user_weight,
                body.weight,
                standard.name,
                # user.sex,  # TODO get user
            )
            total_norm = normalization * body.count
        else:
            total_norm = (
                body.count
                if not body.completed_type_is_count()
                else body.count / float(standard.count)
            )

        completed_standard = CompletedStandard(
            standard_id=standard.id,
            count=body.count,
            weight=body.weight,
            user_weight=body.user_weight,
            total_norm=total_norm,
            completed_type=body.completed_type,
            user_id=user_id,
        )

        uow.completed_standard_repo.add(completed_standard)

        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)
        try:
            await uow.credit_repo.update_completed_count(user_id, total_norm)
        except NoResultFound:
            pass
        await uow.commit()
        await uow.refresh(completed_standard)
        await uow.refresh(standard)

        # Проверяем и обновляем достижения
        await check_and_update_achievements(
            user_id=user_id,
            standard_id=standard.id,
            activity_date=datetime.now().date(),
        )
    return completed_standard


@completed_standard_router.get(
    "/",
)
@inject
async def list_completed_standards(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
    limit: int = Query(10),
    offset: int = Query(0),
) -> CompletedStandardListResponse:
    params = dict(user_id=credentials["id"], pagination=(limit, offset))
    async with uow:
        count = await uow.completed_standard_repo.count(params)
        completed_standards = await uow.completed_standard_repo.filter(params)
    return CompletedStandardListResponse(
        data=completed_standards, count=count, next_page=count > limit + offset
    )


@completed_standard_router.get(
    "/grouped/",
)
@inject
async def list_grouped_completed_standards(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
    as_standard: bool = Query(False),
) -> GroupedCompletedStandard:
    async with uow:
        return await uow.completed_standard_repo.grouped_list(
            UUID(credentials["id"]), as_standard
        )


@completed_standard_router.get(
    "/rating/",
)
@inject
async def completed_standards_rating_list(
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
    period_days: int | None = Query(None),
) -> list[RatingGroupedCompletedStandard]:
    async with uow:
        return await uow.completed_standard_repo.rating_list(period_days)


@completed_standard_router.patch(
    "/{completed_standard_id}",
)
@inject
async def update_completed_standard(
    completed_standard_id: UUID,
    body: CompletedStandardUpdate,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    check_and_update_achievements: CheckAndUpdateAchievements = Depends(
        Provide["use_cases.check_and_update_achievements"]
    ),
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

        # Проверяем и обновляем достижения
        await check_and_update_achievements(
            user_id=user_id,
            standard_id=completed_standard.standard_id,
            activity_date=datetime.now().date(),
        )
    return completed_standard


@completed_standard_router.delete(
    "/{completed_standard_id}",
    status_code=204,
)
@inject
async def delete_completed_standard(
    completed_standard_id: UUID,
    uow: UnitOfWork = Depends(Provide["repositories.uow"]),
    check_and_update_achievements: CheckAndUpdateAchievements = Depends(
        Provide["use_cases.check_and_update_achievements"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> None:
    user_id = credentials["id"]
    async with uow:
        completed_standard = await uow.completed_standard_repo.get_one(
            {"id": completed_standard_id, "user_id": user_id}
        )
        standard_id = completed_standard.standard_id
        await uow.completed_standard_repo.delete(completed_standard_id)
        await uow.flush()
        await uow.user_repo.update_total_liabilities(user_id)  # TODO events
        # TODO update credit
        await uow.commit()

        # Проверяем и обновляем достижения
        await check_and_update_achievements(
            user_id=user_id,
            standard_id=standard_id,
            activity_date=datetime.now().date(),
        )
