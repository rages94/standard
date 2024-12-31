import abc
import uuid
from datetime import datetime
from typing import Generic, MutableSequence, Type, TypeVar

from pydantic import BaseModel


EventSchema = TypeVar("EventSchema", bound=BaseModel)
KeyType = str | uuid.UUID | int | None


class AbstractEvent(abc.ABC, Generic[EventSchema]):
    event_schema: Type[EventSchema]

    def __init__(self) -> None:
        self._headers: dict[str, bytes] = {
            "EventId": str(uuid.uuid4()).encode(),
            "OccuredOn": datetime.utcnow().isoformat().encode(),
        }

    @abc.abstractmethod
    def get_serialized_event(self) -> EventSchema:
        ...  # pragma: no cover

    @abc.abstractmethod
    def get_key(self) -> KeyType:
        ...  # pragma: no cover

    def get_headers(self) -> dict[str, bytes]:
        return self._headers


class EventEntityMixin:
    _events: MutableSequence[AbstractEvent] | None = None

    @property
    def events(self) -> MutableSequence[AbstractEvent]:
        if self._events is None:
            self._events = list()
        return self._events

    @events.setter
    def events(self, value: MutableSequence[AbstractEvent]) -> None:
        self._events = value


class IEventRouter(abc.ABC):
    @abc.abstractmethod
    async def send_event(self, event: AbstractEvent) -> None:
        ...  # pragma: no cover
