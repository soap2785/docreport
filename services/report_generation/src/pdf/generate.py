from random import randint as rnt

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from src.api.v1.generating.models import RequesterData, ResponseData
from .requester import WriteRequesterData
from .fns import WriteFNS
from .fedres import WriteFEDRES
from .other import WriteOther


class GeneratePDF:
    def __init__(self, req: RequesterData, resp: ResponseData) -> None:
        self.req = req
        self.resp = resp

    def generate(self):
        pdf_name = f"report{rnt(0, 1000)}.pdf"
        pdfmetrics.registerFont(TTFont('times', '/app/src/static/times.ttf'))
        pdfmetrics.registerFont(
            TTFont('tbold', '/app/src/static/timesbold.ttf')
        )
        canvas = Canvas(pdf_name, pagesize=letter)
        y = WriteRequesterData(self.req, canvas).write()
        y = WriteFNS(self.resp, canvas).write(y)
        y = WriteFEDRES(self.resp, canvas).write(y)
        WriteOther(self.resp, canvas).write(y)
        canvas.showPage()
        canvas.save()
        return pdf_name
