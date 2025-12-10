from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.parsing.models import SubmitRequestSchema, RequestSchema
from databases.postgresql.models import Request


class PostgreSQLRequestRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: SubmitRequestSchema):
        request = Request(
            id=payload.id,
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
        schema = RequestSchema(
            id=request.id,
            fullname=request.fullname,
            region=request.region,
            birthdate=request.birthdate,
            passport_date=request.passport_date,
            passport_series=request.passport_series,
            passport_number=request.passport_number,
            state=request.state
        )
        return schema
