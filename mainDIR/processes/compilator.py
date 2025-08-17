from business_logic.parsers.INN import suggestInn
from business_logic.parsers.FNS import suggestFNS
from business_logic.parsers.terrorist import terroristCheck
from business_logic.parsers.civil_service import checkCivserv


async def compilation(dt: dict, tgID: int):
    fullname = dt.get('fullname')
    region = dt.get('region')
    birthdate = dt.get('birthdate')
    passport = dt.get('passport')
    passportDate = dt.get('passportDate')

    INN = suggestInn(fullname, birthdate, passport, passportDate)
    FNS = suggestFNS(INN, fullname)
    terrorist = terroristCheck(fullname)
    civserv = checkCivserv(fullname)

