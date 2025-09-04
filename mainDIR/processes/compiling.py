from business_logic.parsers.INN import suggestInnPOST
from business_logic.parsers.FNS import suggestFNS
from business_logic.parsers.bankrupts import bankrupt
from business_logic.parsers.issIp import iss_ip
from business_logic.parsers.terrorist import terroristCheck
from business_logic.parsers.civil_service import checkCivserv


async def compileData(fullname, region, birthdate, passport, passportDate) -> dict | None:
    try:
        getINN = suggestInnPOST(fullname, birthdate, passport, passportDate)
        if getINN != 'Информация об ИНН не найдена.' and getINN != '' and getINN != "Нет доступа к ресурсу" and getINN.get('code') != 0:
            getFNS = await suggestFNS(getINN, fullname)
            getTerrorist = await terroristCheck(fullname)
            getCivServ = await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            getBankrupts = await bankrupt(getINN, fullname)
            getIssIp = await iss_ip(region, fullname, birthdate)
            compiledDict = {
                'inn': getINN,
                'fns': getFNS,
                'ter': getTerrorist,
                'civ': getCivServ,
                # 'crim': getCriminal,
                'bank': getBankrupts,
                'iss': getIssIp
            }
            return compiledDict
        else:
            getFNS = await suggestFNS(None, fullname)
            getTerrorist = await terroristCheck(fullname)
            getCivServ = await checkCivserv(fullname)
            #getCriminal = criminal(region, fullname)
            getIssIp = await iss_ip(region, fullname, birthdate)
            compiledDict = {
                'fns': getFNS,
                'ter': getTerrorist,
                'civ': getCivServ,
                # 'crim': getCriminal,
                'iss': getIssIp
            }
            return compiledDict

    except Exception as e:
        print(e)
        return None