import abc
from types import TracebackType
from typing import Type

from src.common.events.interfaces import AbstractEvent



class BaseAbstractUnitOfWork(abc.ABC):
    async def commit(self) -> None:
        await self._commit()
        await self.publish_events()

    async def flush(self) -> None:
        await self._flush()

    @abc.abstractmethod
    async def rollback(self) -> None:
        ...

    @abc.abstractmethod
    async def expunge_all(self) -> None:
        """Remove all objects from uow"""
        ...

    @abc.abstractmethod
    async def add_event(self, event: AbstractEvent) -> None:
        ...

    @abc.abstractmethod
    async def publish_events(self) -> None:
        ...

    @abc.abstractmethod
    async def _commit(self) -> None:
        ...

    @abc.abstractmethod
    async def _flush(self) -> None:
        ...

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(
        self,
        exc_t: Type[BaseException] | None,
        exc_v: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.rollback()
