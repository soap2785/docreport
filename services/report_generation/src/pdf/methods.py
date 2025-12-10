from typing import Optional

from reportlab.pdfgen.canvas import Canvas


class Methods:
    @classmethod
    def next(cls, canvas: Canvas, y: Optional[int] = None) -> Optional[int]:
        canvas.setFont("times", 14)
        if y:
            y -= 20
            y = cls.check_y(canvas, y)
            return y

    @classmethod
    def final(cls, canvas: Canvas, y: Optional[int] = None) -> Optional[int]:
        canvas.setFont('tbold', 14)
        if y:
            y -= 30
            y = cls.check_y(canvas, y)
            return y

    @staticmethod
    def check_y(canvas: Canvas, y: int) -> int:
        if y < 200:
            canvas.showPage()
            canvas.setFont('tbold', 14)
            return 760
        return y
