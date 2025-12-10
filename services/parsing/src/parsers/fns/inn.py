from aiohttp import ClientSession

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger

URL = 'https://service.nalog.ru/'


class INN:
    __error_logger = Logger('error')

    @staticmethod
    async def __check(
        data: dict[str, str], classObject: ResponseData
    ) -> None:
        async with ClientSession(URL) as client:
            async with client.post('inn-proc.do', data=data) as resp:
                if resp.status in range(1, 200):
                    classObject.inn = resp['inn']

    @classmethod
    async def check(
        cls, fullname: str, birthdate: str,
        passport: str, passportDate: str,
        classObject: ResponseData
    ) -> None:
        classObject.inn = None
        if fullname == 'test':
            return

        fullname = fullname.split()
        surname = fullname[0]
        name = fullname[1]
        patronymic = fullname[2]

        data = {
            "fam": surname, "nam": name, "otch": patronymic,
            "bdate": birthdate, "bplace": "", "doctype": "21",
            "docno": passport, "docdt": passportDate, "c": "innMy",
            "captcha": "", "captchaToken": "",
        }

        try:
            await cls.__check(data, classObject)
        except Exception as error:
            cls.__error_logger.error(f'INN -- {error}')
