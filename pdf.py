from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

pdfmetrics.registerFont(TTFont('arialmt', 'arialmt.ttf'))
c = canvas.Canvas('report.pdf', pagesize=letter)
c.setFont("arialmt", 16)

c.drawString(40, 760, f"1111")
c.drawString(40, 560, f"1111")
c.drawString(40, 360, f"1111")
c.drawString(40, 160, f"1111")
c.drawString(40, 60, f"1111")
c.save()