from asyncio import gather, to_thread
from datetime import date

from businessLogic.parsers.INN import checkINN
from businessLogic.parsers.FNS import checkFNS
from businessLogic.parsers.bankrupts import checkBankrupt
from businessLogic.parsers.issIp import checkIssIp
from businessLogic.parsers.terrorist import checkTerrorist
from businessLogic.parsers.civilService import checkCivserv
from mainDIR.bot.processes.classesForBot import RequesterData
from businessLogic.classForParsers import CompiledData


async def compileData():
    fullname: str = RequesterData.fullname
    region: str = RequesterData.region
    birthdate: date = RequesterData.birthdate
    passport: str = RequesterData.passport
    passportDate: date = RequesterData.passportDate

    try:
        checkINN(fullname, birthdate, passport, passportDate)
        getINN = CompiledData.inn
        if getINN and getINN not in ('Информация об ИНН не найдена.', '', "Нет доступа к ресурсу", 0):
            await gather(
                to_thread(checkFNS, getINN, fullname),
                to_thread(checkTerrorist, fullname),
                to_thread(checkCivserv, fullname),
                to_thread(checkBankrupt, getINN),
                to_thread(checkIssIp, region, fullname, birthdate)
            )
        else:
            await gather(
                to_thread(checkFNS, None, fullname),
                to_thread(checkTerrorist, fullname),
                to_thread(checkCivserv, fullname),
                to_thread(checkIssIp, region, fullname, birthdate)
            )


    except Exception as e:
        print(e)
        return None
