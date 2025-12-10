from reportlab.pdfgen.canvas import Canvas

from src.api.v1.generating.models import ResponseData
from .methods import Methods


class WriteOther:
    def __init__(self, resp: ResponseData, canvas: Canvas) -> None:
        self.civ = resp.civ
        self.inter = resp.inter
        self.iss = resp.iss
        self.law = resp.law
        self.ok = resp.ok
        self.ter = resp.ter
        self.vk = resp.vk
        self.canvas = canvas

    def write(self, y) -> int:
        self.canvas.drawString(40, y, 'Реестр уволенных с госслужбы:')
        if isinstance(self.civ, list):
            for line in self.civ:
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Наименование органа:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[0])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Должность:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[1])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Причина увольнения:')
                y = Methods.next(self.canvas, y)
                name = ""
                for index, text in enumerate(line[2].split()):
                    if index % 6 == 5:
                        name = name + '!'
                    name = name + text + ' '
                for text in name.split('!'):
                    self.canvas.drawString(45, y, text)
                    y = Methods.next(self.canvas, y)
                y = Methods.final(self.canvas, y + 30)
                self.canvas.drawString(45, y, 'Дата увольнения:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[3])
                y = Methods.final(self.canvas, y)
        elif isinstance(self.civ, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.civ)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр интерпола:')
        y = Methods.next(self.canvas, y)
        self.canvas.drawString(40, y, self.inter)
        y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр адвокатов:')
        if isinstance(self.law, list):
            for line in self.law:
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Регистрационный номер:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[1])
                y = Methods.final(self.canvas, y + 10)
                self.canvas.drawString(45, y, 'Статус:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, line[3])
                y = Methods.final(self.canvas, y)
        elif isinstance(self.law, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.law)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр террористов:')
        y = Methods.next(self.canvas, y)
        self.canvas.drawString(40, y, self.ter)
        y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Ссылки на подходящие профили ВК:')
        if isinstance(self.vk, list):
            for link in self.vk:
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, link)
            y = Methods.final(self.canvas, y)
        elif isinstance(self.vk, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.vk)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Ссылки на подходящие профили ОК:')
        if isinstance(self.ok, list):
            for link in self.ok:
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, link)
            y = Methods.final(self.canvas, y)
        elif isinstance(self.ok, str):
            y = Methods.next(self.canvas, y)
            self.canvas.drawString(40, y, self.ok)
            y = Methods.final(self.canvas, y)
