import asyncio
import sys

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel

from src.api.main import app
from src.config import Settings
from src.containers.container import container
from src.data.models import User
from tests.utils.db import FakeDatabase, create_database, drop_database

settings = Settings()

pytest_plugins = [
    "tests.fixtures.standards",
    "tests.fixtures.completed_standards",
    "tests.fixtures.users",
    "tests.fixtures.liability_templates",
    "tests.fixtures.liabilities",
]

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="session")
def database_url(worker_id: str) -> str:
    return settings.database.dsn + f"_test_{worker_id}"


@pytest.fixture(scope="function")
async def database(database_url):
    await create_database(database_url)

    try:
        yield database_url
    finally:
        await drop_database(database_url)


@pytest.fixture
async def sqla_engine(database, init_database):
    engine = create_async_engine(database)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="function")
def init_database(database):
    engine = create_engine(database.replace("+asyncpg", ""))
    return SQLModel.metadata.create_all(engine)


@pytest.fixture
async def db_session(sqla_engine):
    async with AsyncSession(sqla_engine, expire_on_commit=False) as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture(scope="function")
def _container(db_session):
    container.gateways.db.override(FakeDatabase(db_session))
    return container


@pytest.fixture(scope="function")
async def client(_container):
    app.container = _container
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
def auth_headers(default_user: User) -> dict:
    from fastapi_jwt import JwtAccessBearer
    access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)
    token = access_bearer.create_access_token(subject={"id": str(default_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def auth_client(_container, auth_headers: dict):
    app.container = _container
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", headers=auth_headers
    ) as client:
        yield client


@pytest.fixture(scope="function")
def refresh_headers(default_user: User) -> dict:
    from fastapi_jwt import JwtRefreshBearer
    refresh_bearer = JwtRefreshBearer(secret_key=settings.jwt.refresh_secret_key)
    token = refresh_bearer.create_refresh_token(subject={"id": str(default_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
async def refresh_client(_container, refresh_headers: dict):
    app.container = _container
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", headers=refresh_headers
    ) as client:
        yield client
