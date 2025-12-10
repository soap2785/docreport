from reportlab.pdfgen.canvas import Canvas

from src.api.v1.generating.models import ResponseData
from .methods import Methods


class WriteFEDRES:
    def __init__(self, resp: ResponseData, canvas: Canvas) -> None:
        self.arb = resp.arb
        self.bank = resp.bank
        self.org = resp.org
        self.canvas = canvas

    def write(self, y: int) -> int:
        self.canvas.drawString(40, y, 'Реестр арбитражных управляющих:')
        if isinstance(self.arb, list):
            y = Methods.final(self.canvas, y + 10)
            for line in self.arb:
                self.canvas.drawString(45, y, 'Регистрация в Росреестре:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[0])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'СРО:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[1])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'ИНН:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[2])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'ОГРН:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[3])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Активных дел:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[4])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Всего дел:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[5])
                y = Methods.final(self.canvas, y)
        elif isinstance(self.arb, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.arb)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр должников:')
        if isinstance(self.bank, list):
            y = Methods.final(self.canvas, y + 10)
            for line in self.bank:
                self.canvas.drawString(45, y, 'Номер судебного дела:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[0])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Адрес:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[1])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Дата начала процедуры:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[2])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(
                    45, y, 'Текущая процедура или итоговый статус дела'
                )
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[3])
                y = Methods.final(self.canvas, y)
        elif isinstance(self.bank, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.bank)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр орагнизаторов торгов:')
        if isinstance(self.org, list):
            y = Methods.final(self.canvas, y + 10)
            for line in self.org:
                self.canvas.drawString(45, y, 'Статус лица из ЕГРИП:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[0])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Всего торгов:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[1])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Текущих торгов:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[2])
                y = Methods.final(self.canvas, y)
        elif isinstance(self.org, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.org)
            y = Methods.final(self.canvas, y)
        return y
