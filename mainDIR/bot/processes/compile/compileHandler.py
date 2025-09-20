import datetime
from aiogram.types import Message
from sqlite3 import connect

from mainDIR.bot.processes.classesForBot import RequesterData
from mainDIR.bot.processes.compile.compilingProcess import compileData
from mainDIR.bot.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.bot.processes.generating.generatePDFReportFile import generatePDFReport
from mainDIR.bot.processes.generating.generateTGReportMessage import generateMessage


async def compilation(tgID: int, message: Message) -> str:
    async with connect('database.db') as conn:
        cur = conn.cursor()
        curTime = datetime.datetime.now()
        cur.execute(
            "INSERT INTO orders (fullname, region, birthdate, passport, passportDate, curTime, messageChatId) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (RequesterData.fullname, RequesterData.region, RequesterData.birthdate,
             RequesterData.passport, RequesterData.passportDate, curTime, message.chat.id))
        conn.commit()

    await compileData()
    returnedTG = await generateMessage()
    await generatePDFReport()
    await generateDOCXReport()
    return returnedTG


