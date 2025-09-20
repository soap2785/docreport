import datetime

from businessLogic.parsers.INN import suggestInnPOST
from businessLogic.parsers.FNS import suggestFNS
from businessLogic.parsers.bankrupts import bankrupt
from businessLogic.parsers.issIp import iss_ip
from businessLogic.parsers.terrorist import terroristCheck
from businessLogic.parsers.civilService import checkCivserv
from mainDIR.bot.processes.classesForBot import RequesterData
from businessLogic.classForParsers import CompiledData


async def compileData() -> dict | None:
    fullname: str = RequesterData.fullname
    region: str = RequesterData.region
    birthdate: datetime.date = RequesterData.birthdate
    passport: str = RequesterData.passport
    passportDate: datetime.date = RequesterData.passportDate

    try:
        await suggestInnPOST(fullname, birthdate, passport, passportDate)
        getINN = CompiledData.inn
        if getINN != 'Информация об ИНН не найдена.' and getINN != '' and getINN != "Нет доступа к ресурсу" and getINN != 0:
            await suggestFNS(getINN, fullname)
            await terroristCheck(fullname)
            await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            await bankrupt(getINN)
            await iss_ip(region, fullname, birthdate)
        else:
            await suggestFNS(None, fullname)
            await terroristCheck(fullname)
            await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            await iss_ip(region, fullname, birthdate)

    except Exception as e:
        print(e)
        return None