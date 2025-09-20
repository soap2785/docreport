from sqlite3 import connect

from flask import render_template, request

from mainDIR.site.processes.misc.classesForSite import RequesterData
from mainDIR.site.processes.misc.checkFormForPOST import laconicReturning


async def handlerPOST():
    name: str = request.form.get('name')
    surname: str = request.form.get('surname')
    patronymic: str = request.form.get('patronymic')
    region: str = request.form.get('region')
    birthdate: str = request.form.get('birthdate')
    passport: str = request.form.get('passport')
    passportDate: str = request.form.get('passportDate')
    email: str = request.form.get('email')

    exception = await laconicReturning()
    if exception and exception[1] == 400:
        return exception

    with connect('databaseSITE.db') as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO orders "
                    "(name, surname, patronymic, region, birthdate, passport, passportDate, email, state) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, surname, patronymic, region, birthdate, passport, passportDate, email, 'Ожидает оплаты'))
        conn.commit()
        cur.execute("SELECT id FROM orders ORDER BY id DESC")
        ID = cur.fetchall()[0][0]

    RequesterData.name = name
    RequesterData.surname = surname
    RequesterData.patronymic = patronymic
    RequesterData.region = region
    RequesterData.birthdate = birthdate
    RequesterData.passport = passport
    RequesterData.passportDate = passportDate

    return render_template(
        'requestResult.html',
        id_document=ID,
        name=name,
        surname=surname,
        patronymic=patronymic,
        region=region,
        birthdate=birthdate,
        docnumber=passport,
        docdate=passportDate,
        email=email
    )