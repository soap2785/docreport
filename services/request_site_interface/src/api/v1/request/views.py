from fastapi import status, APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.request import (
    PostgreSQLRequestRepository
)

from .models import CreateUpdateRequestSchema
from aiohttp import ClientSession
from .logger import Logger

router = APIRouter(prefix='/request')


@router.post("")  # response_model=RequestSchema
async def create_request(
    payload: CreateUpdateRequestSchema,
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    repo = PostgreSQLRequestRepository(session)
    request = await repo.create(payload)
    async with ClientSession('http://parsing:9101/api/v1/') as resp:
        request_to_parsing = {
            "id": request.id,
            "fullname": request.fullname,
            "region": request.region,
            "birthdate": request.birthdate,
            "passport_series": request.passport_series,
            "passport_number": request.passport_number,
            "passport_date": request.passport_date
        }
        response = await resp.post(
            'parsing/', json=request_to_parsing, timeout=100000000
        )
        Logger().debug(response)
        return JSONResponse(await response.json(), status.HTTP_201_CREATED)
