import asyncio
import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from mainDIR.processes.compiling import compileData


async def generatePDFReport(
        fullname: str,
        region: str,
        birthdate: datetime.date,
        passport: str,
        passportDate: datetime.date,
        ID: int | tuple) -> tuple:
    if type(ID) is tuple:
        ID = ID[0]
    fullnameForFilename = fullname.replace(' ', '-')
    filename = f"Report-{ID}-{fullnameForFilename}.pdf"
    result = await compileData(fullname, region, birthdate, passport, passportDate)
    pdfmetrics.registerFont(TTFont('arialmt', '../arialmt.ttf'))
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("arialmt", 16)

    c.drawString(40, 760, f"ФИО: {fullname}")
    c.drawString(40, 740, f"Регион: {region}")
    c.drawString(40, 720, f"Дата рождения: {birthdate}")
    c.drawString(40, 700, f"Паспорт: {passport}")
    c.drawString(40, 680, f"Дата выдачи паспорта: {passportDate}")

    if result.get('inn') != 'Информация об ИНН не найдена.' and result.get('inn') != '' and result.get('inn') != "Нет доступа к ресурсу" and result.get('inn'):
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ИНН: {result.get('inn').get('inn')}")
        c.drawString(40, 620, f"ФНС: {result.get('fns')}")
        c.drawString(40, 600, f"База террористов: {result.get('ter')}")
        c.drawString(40, 580, f"Госслужба: {result.get('civ')}")
        c.drawString(40, 560, f"Банкротство: {result.get('bank')}")
        c.drawString(40, 540, f"Исполнительные производства:")
        c.setFont("arialmt", 14)
        if result.get('iss') != "Ничего не найдено":
            await drawIssIp(result, c, 550)
        else:
            c.drawString(40, 560, "Ничего не найдено")

    else:
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ФНС: {result.get('fns')}")
        c.drawString(40, 620, f"База террористов: {result.get('ter')}")
        c.drawString(40, 600, f"Госслужба: {result.get('civ')}")
        c.drawString(40, 580, "Исполнительные производства:")
        if result.get('iss') != "Ничего не найдено":
            await drawIssIp(result, c, 590)
        else:
            c.drawString(40, 560, "Ничего не найдено")
    c.save()
    await asyncio.sleep(1)
    return filename, result


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
                for x, line in enumerate(row):
                    if len(line) >= 60:
                        text = line.split("\n")
                        for line in text:
                            someSpace += 1
                            c.drawString(40, startPosition - (20 * someSpace), line)
                    else:
                        someSpace += 1
                        c.drawString(40, startPosition - (20 * someSpace), line)
