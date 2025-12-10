from aiohttp import ClientSession

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger

URL = 'https://gossluzhba.gov.ru/api/anti-corruption/trust-loss-dismissal/list'


class CivilServiceResp:
    organizationName: str
    positionName: str
    regulatoryAct: str
    dismissActDate: str

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)


class CivilService:
    __error_logger = Logger('error')
    __info_logger = Logger()

    @classmethod
    async def check(cls, fullname: str, classObject: ResponseData):
        cls.__info_logger.info('CIV', 1)
        async with ClientSession() as client:
            try:
                query = {
                    'filter': {'fullName': fullname},
                    'paging': {'page': 1, 'pageSize': 20},
                    'order': []
                }
                async with client.post(URL, json=query) as resp:
                    response = (await resp.json())['items']
                    del (
                        response[0]['id'], response[0]['rowNumber'],
                        response[0]['fullName'], response[0]['publishDate'],
                        response[0]['status']
                    )
                    response = [CivilServiceResp(**response[0])]
                if response:
                    response = response[0]
                    classObject.civ = {
                        'Наименование организации': response.organizationName,
                        'Наименование должности': response.positionName,
                        'Статья': response.regulatoryAct,
                        'Дата увольнения': response.dismissActDate
                    }
                cls.__info_logger.info('CIV', 2)
            except IndexError:
                pass
            except Exception as err:
                cls.__error_logger.error(f'CIV: {err}')
