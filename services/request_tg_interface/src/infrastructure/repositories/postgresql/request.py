from typing import Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request_schema import RequestSchema
from app.bot.states import RequesterData
from databases.postgresql.models import Request
from sqlalchemy import select, update


class PostgreSQLRequestRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: RequesterData):
        request = Request(
            fullname=payload.fullname,
            region=payload.region,
            birthdate=payload.birthdate,
            passport_date=payload.passport_date,
            passport_series=payload.passport_series,
            passport_number=payload.passport_number,
            state=False
        )
        self._session.add(request)
        await self._session.commit()
        stmt = select(Request).order_by(Request.id.desc()).limit(1)
        repsonse = await self._session.execute(stmt)
        schema = RequestSchema(
            id=repsonse.scalar_one().id,
            fullname=request.fullname,
            region=request.region,
            birthdate=request.birthdate,
            passport_date=request.passport_date,
            passport_series=request.passport_series,
            passport_number=request.passport_number,
            state=False
        )
        return schema

    async def get_by_id(self, id: int):
        stmt = select(Request).where(Request.id == id)
        return (await self._session.execute(stmt)).one_or_none()

    async def commit(self):
        await self._session.commit()

    async def get_last_order(self) -> Optional[Request]:
        stmt = select(Request).order_by(Request.id.desc())
        result = await self._session.execute(stmt)
        last_order: Optional[Request] = result.scalar_one_or_none()
        return last_order

    async def update(self, key: str, value: Any, id: int):
        stmt = (
            update(Request)
            .where(Request.id == id)
            .values({key: value})
        )
        await self._session.execute(stmt)
