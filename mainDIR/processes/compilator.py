from sqlite3 import connect

from business_logic.parsers.INN import suggestInn
from business_logic.parsers.FNS import suggestFNS
from business_logic.parsers.bankrupts import bankrupt
from business_logic.parsers.issIp import iss_ip
from business_logic.parsers.terrorist import terroristCheck
from business_logic.parsers.civil_service import checkCivserv
from business_logic.parsers.criminal import criminal
from mainDIR.config import bot


async def compilation(dt: dict, tgID: int):
    fullname = dt.get(tgID).get('fullname')
    region = dt.get(tgID).get('region')
    birthdate = dt.get(tgID).get('birthdate')
    passport = dt.get(tgID).get('passport')
    passportDate = dt.get(tgID).get('passportDate')

    with connect('database.db') as conn:
        conn.cursor().execute(
            "INSERT INTO orders (fullname, region, birthdate, passport, passportDate) VALUES (?, ?, ?, ?, ?)",
            (fullname, region, birthdate, passport, passportDate))
        conn.commit()




async def compilate(fullname, region, birthdate, passport, passportDate) -> dict:
    getINN = suggestInn(fullname, birthdate, passport, passportDate)
    getFNS = suggestFNS(getINN, fullname)
    getTerrorist = terroristCheck(fullname)
    getCivServ = checkCivserv(fullname)
    getCriminal = criminal(region, fullname)
    getBankrupts = bankrupt(getINN, fullname)
    getIssIp = iss_ip(region, fullname, birthdate)
    compilatedDict = {
        'https://service.nalog.ru/inn-proc.do': getINN,
        'https://egrul.nalog.ru/index.html': getFNS,
        'https://fedsfm.ru/documents/terrorists-catalog-portal-add': getTerrorist,
        'https://gossluzhba.gov.ru/reestr?filters=%7B"fullName":null%7D&page=1': getCivServ,
        'https://fsin.gov.ru/criminal/': getCriminal,
        'https://bankrot.fedresurs.ru/bankrupts': getBankrupts,
        'https://fssp.gov.ru/iss/ip': getIssIp
    }
    return compilatedDict
