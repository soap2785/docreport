from typing import Optional, Union

from aiohttp import ClientSession
from asyncio import sleep as asleep
from time import time

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger

URL = "https://egrul.nalog.ru"


class FNS:
    __error_logger = Logger(type='error')
    __info_logger = Logger()

    @staticmethod
    async def __check(query: Union[int, str]) -> bool:
        async with ClientSession() as client:
            async with client.post(
                URL, data={'query': query, 'nameEq': 'on'}
            ) as resp:
                magic: str = (await resp.json()).get('t')
                if not magic:
                    return False

                while True:
                    currentTime = int(round(time() * 1000))

                    async with client.get(
                        f'{URL}/search-result/{magic}'
                        f'?r={currentTime}&_={currentTime}'
                    ) as resp:
                        _response = await resp.json()
                        if _response.get('status') == 'wait':
                            continue
                        if _response.get('rows'):
                            return True
                        return False
                    await asleep(.1)

    @classmethod
    async def check(
        cls, classObject: ResponseData,
        inn: Optional[int] = None, fullname: Optional[str] = None
    ) -> None:
        cls.__info_logger.info('FNS', 1)
        query = fullname or inn

        try:
            if await cls.__check(query):
                classObject.fns = 'Человек есть в базе данных'
            cls.__info_logger.info('FNS', 2)
        except Exception as err:
            cls.__error_logger.error(f'FNS -- {err}')
