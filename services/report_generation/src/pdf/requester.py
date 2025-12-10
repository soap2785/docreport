from reportlab.pdfgen.canvas import Canvas

from src.api.v1.generating.models import RequesterData
from .methods import Methods


class WriteRequesterData:
    def __init__(self, req: RequesterData, canvas: Canvas) -> None:
        self.fullname: str = req.fullname
        self.region: str = req.region
        self.birthdate: str = req.birthdate
        self.passport = None
        if req.passport_series and req.passport_number:
            self.passport: str = f'{req.passport_series} {req.passport_number}'
        self.passport_date: str = req.passport_date
        self.canvas = canvas

    def write(self, y: int = 760) -> None:
        self.canvas.setFont('tbold', 14)
        self.canvas.drawString(40, y, 'ФИО:')
        Methods.next(self.canvas)
        self.canvas.drawString(85, y, self.fullname)
        y = Methods.final(self.canvas, y)

        if self.region:
            self.canvas.drawString(40, y, 'Регион:')
            Methods.next(self.canvas)
            self.canvas.drawString(95, y, self.region)
            y = Methods.final(self.canvas, y)

        if self.birthdate:
            self.canvas.drawString(40, y, 'Дата рождения:')
            Methods.next(self.canvas)
            self.canvas.drawString(145, y, self.birthdate)
            y = Methods.final(self.canvas, y)

        if self.passport:
            self.canvas.drawString(40, y, 'Паспорт:')
            Methods.next(self.canvas)
            self.canvas.drawString(105, y, self.passport)
            y = Methods.final(self.canvas, y)

        if self.passport_date:
            self.canvas.drawString(40, y, 'Дата выдачи паспорта:')
            Methods.next(self.canvas)
            self.canvas.drawString(195, y, self.passport_date)
        return Methods.final(self.canvas, y)
