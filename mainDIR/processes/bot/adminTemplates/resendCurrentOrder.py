import os
from sqlite3 import connect

from aiogram.types import Message, FSInputFile

from mainDIR.bot.config import bot
from mainDIR.processes.bot.classes import TempStorageForAdmin
from mainDIR.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.processes.generating.generatePDFReportFile import generatePDFReport


async def resend(message: Message) -> None:
    await bot.delete_message(message.chat.id, message.message_id)
    with connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE id = ?", (TempStorageForAdmin.absID,))
        result = cur.fetchall()
        result = result[0]
    returnedPDF = await generatePDFReport(result[1], result[2], result[3], result[4], result[5], TempStorageForAdmin.absID)
    returnedDOCX = await generateDOCXReport(returnedPDF[1], result[0], result[1], result[2], result[3], result[4], result[5])
    await bot.send_document(result[8], FSInputFile(returnedPDF[0]))
    await bot.send_document(result[8], FSInputFile(returnedDOCX))
    os.remove(returnedPDF[0])
    os.remove(returnedDOCX)