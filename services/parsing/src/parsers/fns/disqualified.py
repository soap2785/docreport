from aiohttp import ClientSession

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


URL = "https://service.nalog.ru/disqualified-proc.json"


class DisqualifiedResp:
    ROW_NUM: int
    ДатаФорм: str
    КолЗап: int
    НомЗап: str
    ФИО: str
    ДатаРожд: str
    МестоРожд: str
    НаимОрг: str
    Должность: str
    КвалификацияТекст: str
    НаимОргПрот: str
    ФИОСуд: str
    ДолжностьСуд: str
    ДисквСрок: str
    ДатаНачДискв: str
    ДатаКонДискв: str
    row_cnt: int

    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __bool__(self) -> bool:
        return self.__dict__.get('ROW_NUM') is not None


class Disqualified:
    __error_logger = Logger('error')
    __info_logger = Logger()

    @classmethod
    async def check(cls, fullname: str, classObject: ResponseData) -> None:
        cls.__info_logger.info('DISQ', 1)
        async with ClientSession() as client:
            try:
                async with client.get(f'{URL}?query={fullname}') as resp:
                    response = (await resp.json()).get('data')
                    response = [DisqualifiedResp(**row) for row in response]
                if response:
                    response = response[0]
                    classObject.disq = {
                        'Номер записи': response.ROW_NUM,
                        'Место рождения': response.МестоРожд,
                        'Организация': response.НаимОрг,
                        'Должность': response.Должность,
                        'Статья': response.КвалификацияТекст,
                        'Наименование органа': response.НаимОргПрот,
                        'Судья': response.ДолжностьСуд,
                        'Должность судьи': response.ДолжностьСуд,
                        'Срок дисквалификации': response.ДисквСрок,
                        'Дата начала': response.ДатаНачДискв,
                        'Дата конца': response.ДатаКонДискв
                    }
                cls.__info_logger.info('DISQ', 2)
            except Exception as error:
                cls.__error_logger.error(str(error) + ' DISQ')
