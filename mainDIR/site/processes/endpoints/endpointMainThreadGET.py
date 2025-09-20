from datetime import datetime, date

from flask import render_template


async def handlerGET():
    return render_template(
        'request.html',
        id_document="",
        name="",
        surname="",
        patronymic="",
        region="Москва",
        birthdate="",
        docnumber="",
        docdate="",
        email="",
        pasdatamax=str(date.today()),
        dobdatamin=str(datetime.now().year - 100)
    )