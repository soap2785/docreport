from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple

from databases.postgresql.models import Request
from sqlalchemy import update, select


class PostgreSQLRequestRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add(self, payload: Tuple[int, str]):
        stmt = (
            update(Request)
            .where(Request.id == payload[0])
            .values(idempotence_key=payload[1])
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def get_by_id(self, id: int):
        stmt = (
            select(Request)
            .where(Request.id == id)
        )
        return await self._session.execute(stmt)
