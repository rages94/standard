from datetime import datetime, timedelta, timezone

from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Standard, User
from tests.factories.completed_standards import CompletedStandardFactory
from tests.factories.standards import StandardFactory


async def test_grouped_list_empty(default_user: User, _container: DeclarativeContainer):
    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.grouped_list(default_user.id)

    assert result.labels == []
    assert result.datasets == []


async def test_grouped_list_single_standard_multiple_records(
    user: User,
    standard: Standard,
    db_session: AsyncSession,
    _container: DeclarativeContainer,
):
    today = datetime.now(timezone.utc)
    await CompletedStandardFactory.create_async(
        user_id=user.id,
        standard_id=standard.id,
        total_norm=10.0,
        created_at=today,
    )
    await CompletedStandardFactory.create_async(
        user_id=user.id,
        standard_id=standard.id,
        total_norm=20.0,
        created_at=today,
    )
    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.grouped_list(user.id)

    assert len(result.labels) == 1
    assert len(result.datasets) == 1
    assert result.datasets[0].label == standard.name
    assert result.datasets[0].data == [30.0]


async def test_grouped_list_multiple_standards(
    default_user: User,
    db_session: AsyncSession,
    _container: DeclarativeContainer,
):
    standard1 = await StandardFactory.create_async(is_deleted=False)
    standard2 = await StandardFactory.create_async(is_deleted=False)

    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard1.id,
        total_norm=10.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard2.id,
        total_norm=20.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.grouped_list(default_user.id)

    assert len(result.datasets) == 2
    labels = {ds.label for ds in result.datasets}
    assert labels == {standard1.name, standard2.name}


async def test_grouped_list_multiple_days(
    default_user: User,
    standard: Standard,
    db_session: AsyncSession,
    _container: DeclarativeContainer,
):
    today = datetime.now(timezone.utc).replace(
        hour=12, minute=0, second=0, microsecond=0
    )
    yesterday = today - timedelta(days=1)

    cs1 = await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=10.0,
    )
    cs1.created_at = yesterday

    cs2 = await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=20.0,
    )
    cs2.created_at = today

    await db_session.flush()

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.grouped_list(default_user.id)

    assert len(result.labels) == 2
    assert len(result.datasets) == 1
    assert len(result.datasets[0].data) == 2


async def test_grouped_list_excludes_other_users(
    default_user: User,
    user: User,
    standard: Standard,
    db_session: AsyncSession,
    _container: DeclarativeContainer,
):
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=10.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=user.id,
        standard_id=standard.id,
        total_norm=20.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.grouped_list(default_user.id)

    assert len(result.datasets) == 1
    assert result.datasets[0].data == [10.0]


async def test_rating_list_empty(_container: DeclarativeContainer):
    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    assert len(result) == 1
    assert result[0].standard_name == "Все упражнения"
    assert result[0].user_ratings == []


async def test_rating_list_single_user(
    default_user: User,
    standard: Standard,
    _container: DeclarativeContainer,
):
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        count=5.0,
        total_norm=15.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    assert len(result) == 2

    all_exercises = next(r for r in result if r.standard_name == "Все упражнения")
    assert len(all_exercises.user_ratings) == 1
    assert all_exercises.user_ratings[0].username == default_user.username
    assert all_exercises.user_ratings[0].standards == 15.0

    standard_rating = next(r for r in result if r.standard_name == standard.name)
    assert len(standard_rating.user_ratings) == 1
    assert standard_rating.user_ratings[0].count == 5.0


async def test_rating_list_sorted_by_total_norm_desc(
    default_user: User,
    user: User,
    standard: Standard,
    _container: DeclarativeContainer,
):
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=50.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=user.id,
        standard_id=standard.id,
        total_norm=100.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    all_exercises = next(r for r in result if r.standard_name == "Все упражнения")
    assert all_exercises.user_ratings[0].username == user.username
    assert all_exercises.user_ratings[1].username == default_user.username


async def test_rating_list_with_days_filter(
    default_user: User,
    standard: Standard,
    db_session: AsyncSession,
    _container: DeclarativeContainer,
):
    now = datetime.now(timezone.utc)
    old_date = now - timedelta(days=10)

    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=10.0,
        created_at=old_date,
    )

    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        total_norm=20.0,
        created_at=now,
    )

    await db_session.flush()

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list(days=5)

    all_exercises = next(r for r in result if r.standard_name == "Все упражнения")
    assert len(all_exercises.user_ratings) == 1
    assert all_exercises.user_ratings[0].standards == 20.0


async def test_rating_list_excludes_deleted_standards(
    default_user: User,
    _container: DeclarativeContainer,
):
    deleted_standard = await StandardFactory.create_async(is_deleted=True)
    active_standard = await StandardFactory.create_async(is_deleted=False)

    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=deleted_standard.id,
        total_norm=10.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=active_standard.id,
        total_norm=20.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    standard_names = {r.standard_name for r in result}
    assert deleted_standard.name not in standard_names
    assert active_standard.name in standard_names


async def test_rating_list_aggregates_all_standards(
    default_user: User,
    _container: DeclarativeContainer,
):
    standard1 = await StandardFactory.create_async(is_deleted=False)
    standard2 = await StandardFactory.create_async(is_deleted=False)

    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard1.id,
        total_norm=30.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard2.id,
        total_norm=70.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    all_exercises = next(r for r in result if r.standard_name == "Все упражнения")
    assert len(all_exercises.user_ratings) == 1
    assert all_exercises.user_ratings[0].standards == 100.0


async def test_rating_list_multiple_users_aggregation(
    default_user: User,
    user: User,
    standard: Standard,
    _container: DeclarativeContainer,
):
    await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
        count=5.0,
        total_norm=15.0,
    )
    await CompletedStandardFactory.create_async(
        user_id=user.id,
        standard_id=standard.id,
        count=10.0,
        total_norm=30.0,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.completed_standard_repo.rating_list()

    all_exercises = next(r for r in result if r.standard_name == "Все упражнения")
    assert len(all_exercises.user_ratings) == 2

    standards_rating = next(r for r in result if r.standard_name == standard.name)
    assert len(standards_rating.user_ratings) == 2
    assert sum(ur.count for ur in standards_rating.user_ratings) == 15.0
