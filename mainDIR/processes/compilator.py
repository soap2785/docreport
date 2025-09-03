import datetime
from sqlite3 import connect

from mainDIR.processes.generateDOCXReportFile import generateDOCXReport
from mainDIR.processes.generatePDFReportFile import generatePDFReport


async def compilation(dt: dict, tgID: int, messageChatId: int) -> tuple:
    fullname: str = dt.get(tgID).get('fullname')
    region: str = dt.get(tgID).get('region')
    birthdate: datetime.date = dt.get(tgID).get('birthdate')
    passport: str = dt.get(tgID).get('passport')
    passportDate: datetime.date = dt.get(tgID).get('passportDate')

    with connect('database.db') as conn:
        curTime = datetime.datetime.now()
        conn.cursor().execute(
            "INSERT INTO orders (fullname, region, birthdate, passport, passportDate, curTime, messageChatId) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (fullname, region, birthdate, passport, passportDate, curTime, messageChatId))
        conn.commit()

    with connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM orders WHERE curTime = ?", (curTime,))
        result = cur.fetchall()

    returnedPDF = await generatePDFReport(fullname, region, birthdate, passport, passportDate, result[0])
    returnedDOCX = await generateDOCXReport(returnedPDF[1], result[0], fullname, region, birthdate, passport, passportDate)
    return returnedPDF, returnedDOCX


