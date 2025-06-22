import operator as op

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter

from src.common.repository.base import Repository
from src.data.models.auth_link import AuthLink


class AuthLinkFilterSet(BaseFilterSet):
    id = Filter(AuthLink.id)
    user_id = Filter(AuthLink.user_id)
    expire_datetime_gt = Filter(AuthLink.expire_datetime, lookup_expr=op.gt)


class AuthLinkRepository(
    Repository[
        AuthLink,
        AuthLinkFilterSet,
        AsyncSession,
    ]
):
    model = AuthLink
    filter_set = AuthLinkFilterSet
    query = select(AuthLink)
