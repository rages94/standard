from dependency_injector import containers, providers
from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer

from src.common.db import Database


class GatewaysContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(Database, dsn=config.database.dsn, echo=config.database.echo)
