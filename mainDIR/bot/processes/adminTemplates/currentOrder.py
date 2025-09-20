import os
from aiosqlite import connect

from aiogram.types import Message, FSInputFile

from mainDIR.bot.src.config import bot
from mainDIR.bot.processes.classesForBot import TempStorageForAdmin
from mainDIR.bot.processes.compile. compilingProcess import compileData
from mainDIR.bot.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.bot.processes.generating.generatePDFReportFile import generatePDFReport
from mainDIR.bot.processes.generating.generateTGReportMessage import generateMessage
from mainDIR.bot.processes.classesForBot import RequesterData


async def resendCurrentOrder(message: Message) -> None:
    await bot.delete_message(message.chat.id, message.message_id)

    async with connect('database.db') as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM orders WHERE id = ?", (TempStorageForAdmin.absID,))
            result = await cur.fetchone()

    RequesterData.fullname = result[1]
    RequesterData.region = result[2]
    RequesterData.birthdate = result[3]
    RequesterData.passport = result[4]
    RequesterData.passportDate = result[5]

    await compileData()
    returnedTG = await generateMessage()
    await generatePDFReport()
    await generateDOCXReport()

    await bot.send_message(result[8], returnedTG)
    await bot.send_document(result[8], FSInputFile("reportBOT.pdf"))
    await bot.send_document(result[8], FSInputFile("reportBOT.docx"))

    os.remove("reportBOT.pdf")
    os.remove("reportBOT.docx")