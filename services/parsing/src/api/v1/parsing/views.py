from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from aiohttp import ClientSession

from .models import SubmitRequestSchema, Response
from src.parsers.compile import Compile
from src.parsers.logger import Logger

router = APIRouter(prefix='/parsing')


@router.post("", response_model=Response)
async def start_parsing(payload: SubmitRequestSchema) -> JSONResponse:
    async with ClientSession('http://payment:9102/api/v1/') as resp:
        request_to_payment = {
            "summa": 1,
            "currency": 100,
            "id": payload.id,
            "surname": payload.fullname.split()[0],
            "name": payload.fullname.split()[1],
            "patronymic": payload.fullname.split()[2],
            "email": "ultramarinow@gmail.com",
            "testing": True
        }
        response = await resp.post('payment/', json=request_to_payment)
        if not (await response.json())["access"]:
            raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED)
    response = await Compile.compileData(payload)
    Logger().debug(response)
    response = Response(response_data_dict=response.__dict__)
    return JSONResponse(response.model_dump(), status.HTTP_200_OK)
