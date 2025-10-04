from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models.message import Message


class MessageFilterSet(BaseFilterSet):
    id = Filter(Message.id)
    user_id = Filter(Message.user_id)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(Message.created_at),
    )


class MessageRepository(
    Repository[
        Message,
        MessageFilterSet,
        AsyncSession,
    ]
):
    model = Message
    filter_set = MessageFilterSet
    query = select(Message).order_by(Message.created_at.desc())
