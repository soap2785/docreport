import asyncio
import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from mainDIR.processes.bot.classes import RequesterData


async def generatePDFReport(
        ID: int | tuple,
        CompiledData: dict
) -> str:
    if type(ID) is tuple:
        ID = ID[0]

    fullnameForFilename = RequesterData.fullname.replace(' ', '-')
    filename = f"Report-{ID}-{fullnameForFilename}.pdf"

    fullname = RequesterData.fullname
    region = RequesterData.region
    birthdate = RequesterData.birthdate
    passport = RequesterData.passport
    passportDate = RequesterData.passportDate

    birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
    passportDate = datetime.datetime.strftime(passportDate, "%d.%m.%Y")

    pdfmetrics.registerFont(TTFont('arialmt', '../arialmt.ttf'))
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("arialmt", 16)

    c.drawString(40, 760, f"ФИО: {fullname}")
    c.drawString(40, 740, f"Регион: {region}")
    c.drawString(40, 720, f"Дата рождения: {birthdate}")
    c.drawString(40, 700, f"Паспорт: {passport}")
    c.drawString(40, 680, f"Дата выдачи паспорта: {passportDate}")

    if CompiledData.get('inn') != 'Информация об ИНН не найдена.' and CompiledData.get('inn') != '' and CompiledData.get('inn') != "Нет доступа к ресурсу" and CompiledData.get('inn'):
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ИНН: {CompiledData.get('inn').get('inn')}")
        c.drawString(40, 620, f"ФНС: {CompiledData.get('fns')}")
        c.drawString(40, 600, f"База террористов: {CompiledData.get('ter')}")
        c.drawString(40, 580, f"Госслужба: {CompiledData.get('civ')}")
        c.drawString(40, 560, f"Банкротство: {CompiledData.get('bank')}")
        c.drawString(40, 540, f"Исполнительные производства:")
        c.setFont("arialmt", 14)
        if CompiledData.get('iss') != "Ничего не найдено":
            await drawIssIp(CompiledData, c, 550)
        else:
            c.drawString(40, 560, "Ничего не найдено")

    else:
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ФНС: {CompiledData.get('fns')}")
        c.drawString(40, 620, f"База террористов: {CompiledData.get('ter')}")
        c.drawString(40, 600, f"Госслужба: {CompiledData.get('civ')}")
        c.drawString(40, 580, "Исполнительные производства:")
        if CompiledData.get('iss') != "Ничего не найдено":
            await drawIssIp(CompiledData, c, 590)
        else:
            c.drawString(40, 560, "Ничего не найдено")
    c.save()
    await asyncio.sleep(1)
    return filename


async def drawIssIp(result: dict, canvasObject: Canvas, startPosition: int):
        c = canvasObject
        someSpace = 1
        for x, rowIterable in enumerate(range(0, len(result.get('iss')))):
            if x % 3 == 0 and x != 0:
                c.showPage()
                c.setFont("arialmt", 14)
                someSpaceForY = 760
                someSpace = 1
            startPosition -= 10
            row = result.get('iss')[rowIterable]
            if row:
                for line in row:
                    if len(line) >= 60:
                        text = line.split("\n")
                        for specifiedLine in text:
                            someSpace += 1
                            c.drawString(40, startPosition - (20 * someSpace), line)
                    else:
                        someSpace += 1
                        c.drawString(40, startPosition - (20 * someSpace), line)
