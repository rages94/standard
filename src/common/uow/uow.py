from types import TracebackType
from typing import Type

from sqlmodel import SQLModel

from src.common.db import Database
from src.common.events.interfaces import AbstractEvent, EventEntityMixin
from src.common.uow.interfaces import BaseAbstractUnitOfWork


class BaseUnitOfWork(BaseAbstractUnitOfWork):
    def __init__(
            self,
            db: Database,
            # event_router: IEventRouter
    ):
        self.db = db
        # self.event_router = event_router
        self.events: list[AbstractEvent] = []

    async def __aenter__(self) -> None:
        await super().__aenter__()
        self.session = self.db.session_factory()

    async def __aexit__(
            self,
            exc_t: Type[BaseException] | None,
            exc_v: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        self.session.expunge_all()
        await super().__aexit__(exc_t, exc_v, exc_tb)
        await self.session.close()

    async def add_event(self, event: AbstractEvent) -> None:
        self.events.append(event)

    async def _commit(self) -> None:
        await self.session.commit()

    async def _flush(self) -> None:
        await self.session.flush()

    async def add(self) -> None:
        await self.session.add()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def expunge_all(self) -> None:
        self.session.expunge_all()

    async def refresh(self, entity: SQLModel) -> None:
        await self.session.refresh(entity)

    async def publish_events(self) -> None:
        for entity in self.session.identity_map.values():  # type: ignore
            if not isinstance(entity, EventEntityMixin):
                continue
            # while entity.events:
            #     event = entity.events.pop(0)
            #     self.events.append(event)

        # while self.events:
        #     event = self.events.pop(0)
        #     await self.event_router.send_event(event)
