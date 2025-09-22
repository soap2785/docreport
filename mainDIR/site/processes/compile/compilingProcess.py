from businessLogic.parsers.INN import checkINN
from businessLogic.parsers.FNS import checkFNS
from businessLogic.parsers.bankrupts import checkBankrupt
from businessLogic.parsers.issIp import checkIssIp
from businessLogic.parsers.terrorist import checkTerrorist
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
        await checkINN(fullname, birthdate, passport, passportDate)
        getINN = CompiledData.inn
        if getINN and getINN not in ('Информация об ИНН не найдена.', '', "Нет доступа к ресурсу", 0):
            await checkFNS(getINN, fullname)
            await checkTerrorist(fullname)
            await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            await checkBankrupt(getINN)
            await checkIssIp(region, fullname, birthdate)
        else:
            await checkFNS(None, fullname)
            await checkTerrorist(fullname)
            await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            await checkIssIp(region, fullname, birthdate)

    except Exception as e:
        print(e)
        return None