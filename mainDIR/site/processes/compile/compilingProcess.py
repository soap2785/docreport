from businessLogic.parsers.INN import suggestInnPOST
from businessLogic.parsers.FNS import suggestFNS
from businessLogic.parsers.bankrupts import bankrupt
from businessLogic.parsers.issIp import iss_ip
from businessLogic.parsers.terrorist import terroristCheck
from businessLogic.parsers.civilService import checkCivserv
from mainDIR.site.processes.misc.classesForSite import RequesterData
from businessLogic.classForParsers import CompiledData


async def compileData() -> dict | None:
    name: str = RequesterData.name
    surname: str = RequesterData.surname
    patronymic = RequesterData.patronymic
    region: str = RequesterData.region
    birthdate: str = RequesterData.birthdate
    passport: str = RequesterData.passport
    passportDate: str = RequesterData.passportDate
    fullname = surname + ' ' + name + ' ' + patronymic

    try:
        await suggestInnPOST(fullname, birthdate, passport, passportDate)
        getINN = CompiledData.inn
        if getINN and getINN not in ('Информация об ИНН не найдена.', '', "Нет доступа к ресурсу", 0):
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