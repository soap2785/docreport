import datetime
from aiogram.types import Message
from sqlite3 import connect

from mainDIR.processes.bot.classes import RequesterData
from mainDIR.processes.compile.compilingProcess import compileData
from mainDIR.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.processes.generating.generatePDFReportFile import generatePDFReport
from mainDIR.processes.generating.generateTGReportMessage import generateMessage


async def compilation(tgID: int, message: Message) -> tuple:

    with connect('database.db') as conn:
        cur = conn.cursor()
        curTime = datetime.datetime.now()
        cur.execute(
            "INSERT INTO orders (fullname, region, birthdate, passport, passportDate, curTime, messageChatId) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (RequesterData.fullname, RequesterData.region, RequesterData.birthdate,
             RequesterData.passport, RequesterData.passportDate, curTime, message.chat.id))
        conn.commit()
        cur.execute("SELECT id FROM orders WHERE curTime = ?", (curTime,))
        result = cur.fetchall()

    compiledData = await compileData()
    returnedTG = await generateMessage(message, compiledData)
    returnedPDF = await generatePDFReport(result[0], compiledData)
    returnedDOCX = await generateDOCXReport(result[0], compiledData)
    return returnedTG, returnedPDF, returnedDOCX


