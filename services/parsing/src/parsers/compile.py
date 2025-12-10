from asyncio import gather

from .fns.inn import INN
from .fns.disqualified import Disqualified
from .fns.fns import FNS
from .fns.massFounders import MassFounders
from .fns.selfEmployed import SelfEmployed
from .fns.warningList.warningListIP import WarningListIP
from .fns.warningList.warningListUCHR1 import WarningListUCHR1
from .fns.warningList.warningListUCHR2 import WarningListUCHR2
# from .fns.warningList.warningListUL import WarningListUl
from .fedres.arbitration import Arbitration
from .fedres.bankrupt import Bankrupt
from .fedres.organizer import Organizer
from .other.civilService import CivilService
from .other.interpol import Interpol
from .other.terrorist import Terrorist
from .other.ok import OK
from .other.lawyer import Lawyer

from .logger import Logger
from src.api.v1.parsing.models import (
    SubmitRequestSchema, BotPayload, ResponseData
)


class Compile:
    __info_logger = Logger()

    @classmethod
    async def compileData(cls, data: SubmitRequestSchema) -> ResponseData:
        cls.__info_logger.info('COMPILER', 1)
        resp = ResponseData()
        await INN.check(
            data.fullname, data.birthdate,
            f"{data.passport_series} {data.passport_number}",
            data.passport_date, resp
        )
        await gather(
            Disqualified.check(data.fullname, resp),
            FNS.check(resp, resp.inn, data.fullname),
            MassFounders.check(resp, data.fullname, resp.inn),
            SelfEmployed.check(resp.inn, resp),
            WarningListIP().check(resp, data.fullname, resp.inn),
            # WarningListUl().check(resp, data.fullname, resp.inn),
            WarningListUCHR1().check(resp, data.fullname or resp.inn),
            WarningListUCHR2().check(resp, data.fullname, resp.inn),
            Arbitration().check(resp, data.fullname, resp.inn),
            Bankrupt().check(resp, data.fullname, resp.inn),
            Organizer().check(resp, data.fullname, resp.inn),
            CivilService.check(data.fullname, resp),
            # Interpol().check(data.fullname, resp),
            # Terrorist().check(data.fullname, resp),
            # OK().check(data.fullname, resp),
            # Lawyer().check(data.fullname, resp),
        )
        cls.__info_logger.info('COMPILER', 2)
        return resp

    @classmethod
    async def compileDataTest(cls) -> ResponseData:
        cls.__info_logger.info('COMPILER', 1)
        resp = ResponseData()
        await INN.check(
            'Кудинов Игорь Артурович', '16.08.1998',
            '44 18 347118', '05.09.2018', resp
        )
        print(resp.inn)
        await gather(
            Disqualified.check('Ёлшина Лидия Дмитриевна', resp),
            FNS.check(resp, '490914102042', 'Кудинов Игорь Артурович'),
            MassFounders.check(resp, 'Варнавский Петр Владимирович', '550300914931'),
            SelfEmployed.check('490914102042', resp),
            # WarningListIP().check(resp, 'Белова Татьяна Александровна', 'None'),
            # WarningListUl().check(resp, data.fullname, resp.inn),
            WarningListUCHR1().check(resp, 'Белова Татьяна Александровна'),
            # WarningListUCHR2().check(resp, 'Белова Татьяна Александровна', None),
            Arbitration().check(resp, 'Аброськин Александр Витальевич', None),
            Bankrupt().check(resp, 'Неклюдов Алексей Владимирович', None),
            Organizer().check(resp, 'Аброськин Александр Витальевич', None),
            CivilService.check('Худаев Егор Александрович', resp),
            # Interpol().check(data.fullname, resp),
            # Terrorist().check(data.fullname, resp),
            # OK().check(data.fullname, resp),
            # Lawyer().check(data.fullname, resp),
        )
        cls.__info_logger.info('COMPILER', 2)
        return resp
