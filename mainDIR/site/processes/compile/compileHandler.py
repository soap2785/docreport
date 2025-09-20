import datetime
from aiogram.types import Message
from sqlite3 import connect

from mainDIR.site.processes.misc.classesForSite import RequesterData
from mainDIR.bot.processes.compile.compilingProcess import compileData
from mainDIR.bot.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.bot.processes.generating.generatePDFReportFile import generatePDFReport


async def compilation(tgID: int, message: Message) -> None:

    with connect('database.db') as conn:
        cur = conn.cursor()
        curTime = datetime.datetime.now()
        cur.execute(
            "INSERT INTO orders "
            "(name, surname, patronymic, region, birthdate, passport, passportDate, curTime, messageChatId) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (RequesterData.name, RequesterData.surname, RequesterData.patronymic, RequesterData.region,
             RequesterData.birthdate, RequesterData.passport, RequesterData.passportDate, curTime, message.chat.id))
        conn.commit()

    await compileData()
    await generatePDFReport()
    await generateDOCXReport()


