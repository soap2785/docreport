from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.request.models import CreateUpdateRequestSchema, RequestSchema
from databases.postgresql.models import Request
from sqlalchemy import select


class PostgreSQLRequestRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUpdateRequestSchema):
        request = Request(
            fullname=payload.fullname,
            region=payload.region,
            birthdate=payload.birthdate,
            passport_date=payload.passport_date,
            passport_series=payload.passport_series,
            passport_number=payload.passport_number,
            state=payload.state
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
            state=request.state
        )
        return schema
