import datetime

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas

from mainDIR.bot.processes.classesForBot import RequesterData
from businessLogic.classForParsers import CompiledData


async def generatePDFReport():
    """
    Генерирует PDF отчёт для бота
    """

    fullname = RequesterData.fullname
    region = RequesterData.region
    birthdate = RequesterData.birthdate
    passport = RequesterData.passport
    passportDate = RequesterData.passportDate

    inn = CompiledData.inn
    fns = CompiledData.fns
    ter = CompiledData.ter
    civ = CompiledData.civ
    bank = CompiledData.bank
    iss = CompiledData.iss

    birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
    passportDate = datetime.datetime.strptime(passportDate, "%Y-%m-%d")
    birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
    passportDate = datetime.datetime.strftime(passportDate, "%d.%m.%Y")

    pdfmetrics.registerFont(TTFont('arialmt', 'arialmt.ttf'))
    c = canvas.Canvas("reportBOT.pdf", pagesize=letter)
    c.setFont("arialmt", 16)

    c.drawString(40, 760, f"ФИО: {fullname}")
    c.drawString(40, 740, f"Регион: {region}")
    c.drawString(40, 720, f"Дата рождения: {birthdate}")
    c.drawString(40, 700, f"Паспорт: {passport}")
    c.drawString(40, 680, f"Дата выдачи паспорта: {passportDate}")

    if inn and inn not in ('Информация об ИНН не найдена.', '', "Нет доступа к ресурсу"):
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ИНН: {inn}")
        c.drawString(40, 620, f"ФНС: {fns}")
        c.drawString(40, 600, f"База террористов: {ter}")
        c.drawString(40, 580, f"Госслужба: {civ}")
        c.drawString(40, 560, f"Банкротство: {bank}")
        c.drawString(40, 540, f"Исполнительные производства:")
        c.setFont("arialmt", 14)
        if iss not in ("Ничего не найдено", "Сервис недоступен"):
            await drawIssIp(c, 550)
        else:
            c.drawString(40, 510, iss)

    else:
        c.setFont("arialmt", 14)
        c.drawString(40, 640, f"ФНС: {fns}")
        c.drawString(40, 620, f"База террористов: {ter}")
        c.drawString(40, 600, f"Госслужба: {civ}")
        c.drawString(40, 580, "Исполнительные производства:")
        if iss not in ('Ничего не найдено', 'Сервис недоступен'):
            await drawIssIp(c, 590)
        else:
            c.drawString(40, 550, iss)
    c.save()


async def drawIssIp(canvasObject: Canvas, startPosition: int):
        c = canvasObject
        someSpace = 1
        for x, rowIterable in enumerate(range(0, len(CompiledData.iss))):
            if x % 3 == 0 and x != 0:
                c.showPage()
                c.setFont("arialmt", 14)
                someSpaceForY = 760
                someSpace = 1
            startPosition -= 10
            row = CompiledData.iss[rowIterable]
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
