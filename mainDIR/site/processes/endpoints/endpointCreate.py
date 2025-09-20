import re
from datetime import datetime, date
from sqlite3 import connect

from flask import request, render_template

from mainDIR.site.processes.misc.addYooPay import addYooPay


async def create():
    id_document = request.form.get('id_document')
    action = request.form.get('action')
    if action == 'РЕДАКТИРОВАТЬ':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        region = request.form.get('region')
        birthdate = request.form.get('birthdate')
        passport = request.form.get('passport')
        passport = re.sub('\D', '', passport)
        passportDate = request.form.get('passportDate')
        email = request.form.get('email')
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM orders WHERE id = ?", (id_document,))
        return render_template('request.html', id_document=id_document,
                               name=name,
                               surname=surname,
                               patronymic=patronymic,
                               region=region,
                               birthdate=birthdate,
                               docnumber=passport,
                               docdate=passportDate,
                               email=email,
                               pasdatamax=str(date.today()),
                               dobdatamin=str(datetime.now().year - 100)
                               )
    if action == 'ОПЛАТИТЬ QIWI':
        id_document = request.form.get('id_document')
        # Отправка оповещение о нажатии на кнопку оплаты id_document
        # text = "Нажали кнопку оплатить по документу id_document"
        # send_message(text)
        return render_template('payPage.html', id_document=id_document, email=request.form.get('email'))

    if action == 'ОПЛАТИТЬ':
        id_document = request.form.get('id_document')
        cashRegister = addYooPay(100, 'RUB', id_document, request.form)
        # Отправка оповещение о нажатии на кнопку оплаты id_document
        # text = "Нажали кнопку оплатить по документу id_document"
        # send_message(text)
        return render_template('payPageYoo.html', id_document=id_document, email=request.form.get('email'),
                               form=request.form, url=cashRegister)

    return 'Ошибка при формировании отчёта', 400