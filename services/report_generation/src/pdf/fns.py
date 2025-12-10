from reportlab.pdfgen.canvas import Canvas

from src.api.v1.generating.models import ResponseData
from .methods import Methods


class WriteFNS:
    def __init__(self, resp: ResponseData, canvas: Canvas) -> None:
        self.inn = resp.inn
        self.fns = resp.fns
        self.disq = resp.disq
        self.semp = resp.semp
        self.mass = resp.mass
        self.warnip = resp.warnip
        self.warnorg = resp.warnorg
        self.warnuchr1 = resp.warnuchr1
        self.warnuchr2 = resp.warnuchr2
        self.canvas = canvas

    def write(self, y: int) -> int:
        self.canvas.drawString(40, y, 'ИНН:')
        y = Methods.next(self.canvas, y)
        if self.inn:
            self.canvas.drawString(40, y, self.inn)
            y = Methods.final(self.canvas, y)
        else:
            self.canvas.drawString(40, y, 'Данные не обнаружены')
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'ФНС:')
        y = Methods.next(self.canvas, y)
        self.canvas.drawString(40, y, self.fns)
        y = Methods.final(self.canvas, y)
        print(self.mass)
        self.canvas.drawString(40, y, 'Массовые учредители:')
        y = Methods.next(self.canvas, y)
        self.canvas.drawString(40, y, self.mass)
        y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Самозанятые:')
        y = Methods.next(self.canvas, y)
        self.canvas.drawString(40, y, self.semp)
        y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр дисквалифицированных:')
        y = Methods.final(self.canvas, y + 10)
        if isinstance(self.disq, dict):
            for line in self.disq:
                self.canvas.drawString(45, y, f'{line}:')
                y = Methods.next(self.canvas, y)
                self.canvas.drawString(45, y, str(self.disq[line]))
                y = Methods.final(self.canvas, y + 10)
        elif isinstance(self.disq, str):
            Methods.next(self.canvas)
            self.canvas.drawString(40, y, self.disq)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр организаций:')
        y = Methods.next(self.canvas, y)
        if isinstance(self.warnorg, list):
            for line in self.warnorg:
                self.canvas.drawString(45, y, f'{line[0]} {line[1]} {line[2]}')
                y = Methods.next(self.canvas, y)
            y = Methods.final(self.canvas, y + 20)
        elif isinstance(self.warnorg, str):
            self.canvas.drawString(40, y, self.warnorg)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(40, y, 'Реестр ИП:')
        y = Methods.next(self.canvas, y)
        if isinstance(self.warnip, list):
            for line in self.warnip:
                self.canvas.drawString(45, y, f'{line[0]} {line[1]}')
                y = Methods.next(self.canvas, y)
            y = Methods.final(self.canvas, y + 20)
        elif isinstance(self.warnip, str):
            self.canvas.drawString(40, y, self.warnip)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(
            40, y,
            'Сведения о лице, имеющем право без доверенности действовать '
        )
        y = Methods.final(self.canvas, y + 15)
        self.canvas.drawString(40, y, 'от имени юридического лица:')
        y = Methods.next(self.canvas, y)
        if isinstance(self.warnuchr1, list):
            for line in self.warnuchr1:
                self.canvas.drawString(45, y, f'{line[0]} {line[1]} {line[2]}')
                y = Methods.next(self.canvas, y)
            y = Methods.final(self.canvas, y + 20)
        elif isinstance(self.warnuchr1, str):
            self.canvas.drawString(40, y, self.warnuchr1)
            y = Methods.final(self.canvas, y)

        self.canvas.drawString(
            40, y,
            'Сведения об учредителях (участниках, единственном акционере)'
        )
        y = Methods.final(self.canvas, y + 15)
        self.canvas.drawString(40, y, 'юридического лица:')
        y = Methods.next(self.canvas, y)
        if isinstance(self.warnuchr2, list):
            for line in self.warnuchr2:
                self.canvas.drawString(45, y, f'{line[0]} {line[1]} {line[2]}')
                y = Methods.next(self.canvas, y)
            y = Methods.final(self.canvas, y + 20)
        elif isinstance(self.warnuchr2, str):
            self.canvas.drawString(40, y, self.warnuchr2)
            y = Methods.final(self.canvas, y)
        return y
