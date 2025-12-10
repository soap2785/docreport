from typing import Optional
from csv import reader

from src.api.v1.parsing.models import ResponseData
from ..logger import Logger


class MassFounders:
    __error_logger = Logger('error')

    @classmethod
    async def check(
        cls, classObject: ResponseData,
        fullname: Optional[str] = None, inn: Optional[int] = None
    ) -> None:
        try:
            with open(
                '/app/src/static/massfounders.csv', 'r', encoding='utf-8'
            ) as file:
                for line in reader(file):
                    if inn:
                        if line[0].split(';')[0] == str(inn):
                            classObject.mass = "Человек находится в базе"
                    if fullname:
                        if inn:
                            return
                        fullnamePr = [row.upper() for row in fullname.split()]
                        if fullnamePr == line[0].split(';')[1:4]:
                            classObject.mass = "Человек находится в базе"
        except Exception as error:
            cls.__error_logger.error(str(error) + ' MSFND')
