from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker


class Database:
    def __init__(self, dsn: str, echo: bool) -> None:
        self.engine: AsyncEngine = create_async_engine(dsn)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
        )
