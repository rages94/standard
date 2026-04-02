from httpx import AsyncClient

from src.common.models.mixins import moscow_now
from src.data.models import Standard
from src.domain.user_records.use_cases.get_records import GetRecords
from tests.factories.completed_standards import CompletedStandardFactory
from tests.factories.user_records import UserRecordFactory


async def test_create_completed_standard_creates_daily_record(
    auth_client: AsyncClient,
    default_user,
    _container,
    standard: Standard,
) -> None:
    """Тест: создание completed_standard создает дневной рекорд"""
    count = 100
    data = {
        "standard_id": str(standard.id),
        "count": count,
        "user_weight": 70,
        "weight": None,
    }
    response = await auth_client.post("/completed_standards/", json=data)
    assert response.status_code == 201
    get_records = _container.use_cases.get_records()
    records = await get_records(default_user.id)
    assert records.get("daily", 0) == count / float(standard.count)


# async def test_delete_completed_standard_rolls_back_record(
#     auth_client: AsyncClient,
#     default_user,
#     _container,
#     standard: Standard,
# ) -> None:
#     """Тест: удаление completed_standard откатывает рекорд к предыдущему"""
#     await UserRecordFactory.create_async(
#         user_id=default_user.id, type="daily", count=100, created_at=moscow_now()
#     )
#     await UserRecordFactory.create_async(
#         user_id=default_user.id, type="weakly", count=200, created_at=moscow_now()
#     )
#     completed = await CompletedStandardFactory.create_async(
#         user_id=default_user.id,
#         standard_id=standard.id,
#         count=100,
#         total_norm=100,
#     )
#     response = await auth_client.delete(f"/completed_standards/{completed.id}")
#     assert response.status_code == 204
#     get_records = _container.use_cases.get_records()
#     records = await get_records(default_user.id)
#     assert records.get("daily", 0) == 100
#
#
# async def test_patch_completed_standard_updates_record(
#     auth_client: AsyncClient,
#     default_user,
#     _container,
#     standard: Standard,
# ) -> None:
#     """Тест: изменение completed_standard обновляет рекорд"""
#     completed = await CompletedStandardFactory.create_async(
#         user_id=default_user.id,
#         standard_id=standard.id,
#         count=50,
#         total_norm=50,
#     )
#     data = {"count": 150}
#     response = await auth_client.patch(
#         f"/completed_standards/{completed.id}", json=data
#     )
#     assert response.status_code == 200
#     get_records = GetRecords(uow=_container.repositories.uow())
#     records = await get_records(default_user.id)
#     assert records.get("daily", 0) == 150
#
#
# async def test_multiple_completed_standards_same_day(
#     auth_client: AsyncClient,
#     default_user,
#     _container,
#     standard: Standard,
# ) -> None:
#     """Тест: несколько completed_standards за день - рекорд максимальный"""
#     data1 = {
#         "standard_id": str(standard.id),
#         "count": 50,
#         "user_weight": 70,
#         "weight": None,
#     }
#     response1 = await auth_client.post("/completed_standards/", json=data1)
#     assert response1.status_code == 201
#     data2 = {
#         "standard_id": str(standard.id),
#         "count": 100,
#         "user_weight": 70,
#         "weight": None,
#     }
#     response2 = await auth_client.post("/completed_standards/", json=data2)
#     assert response2.status_code == 201
#     get_records = GetRecords(uow=_container.repositories.uow())
#     records = await get_records(default_user.id)
#     assert records.get("daily", 0) == 100
