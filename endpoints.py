import json
import pathlib
import re
from datetime import datetime
from datetime import date
from config import regions, auth
from flask import jsonify, request, app, render_template, send_from_directory
from werkzeug.security import check_password_hash
from flask_mail import Message
import time
from yoo_pay import addYooKassaPay
import os

from generators.generator_1 import generate_PDF_report
from database.command_to_db import (add_new_orders, set_id_order, delete_orders, get_all_orders, set_status_order,
                                    get_order_by_id_order, get_order_by_id)


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/admin')
@auth.login_required
def index():
    return render_template('admin_panel.html')


# Coder
@app.route("/robots.txt")
@app.route('/sitemap.xml')
def static_from_robots():
    return send_from_directory(app.static_folder, request.path[1:])


# Coder


# @app.route('/yandex_2193512d5ec2b4c5.html')
# @auth.login_required
# def index():
#     return render_template('yandex_2193512d5ec2b4c5.html')

@app.route('/retry', methods=['GET', 'POST'])
@auth.login_required
async def retry():
    html = """
    <p>В приложении к письму прикреплен заказанный Вами отчет о физическом лице. </p>
    <p>Полнота и корректность данных зависит от верности данных заполненных Вами при оформлении заказа. </p>
    <p>Мы &ndash; за достоверную информацию, поэтому используем только официальные базы данных. </p>
    <p>&nbsp; </p>
    <p>&nbsp; </p>
    <p>С уважением, </p>
    <p>DOCREPORT.RU </p> 
    """

    try:
        id = int(json.loads(request.data)['id'])
        order = get_order_by_id(id)
        passport_raw = order[6]
        passport = passport_raw[0:2] + " " + passport_raw[2:4] + " " + passport_raw[4:]
        name = order[1]
        surname = order[2]
        middlename = order[3]
        region = order[4]
        birth_date = order[5]
        passport_date = order[7]

        # 0, 2, 1, 3, 4, 5, 7
        # айди, фамилия, имя, отчество, регион, день рождения, паспорт, дата выдачи паспорта

        await generate_PDF_report.generatePDFreport(id, surname, name, middlename, region, birth_date, passport,
                                                    passport_date)
        msg = Message(f'Docreport отчёт №{order[0]}', sender="info24@docreport.ru", recipients=[order[8]])

        file = str(pathlib.Path(
            "../Отчёты",
            f"Отчёт № {order[0]}.docx"
        )
        )

        file_pdf = str(pathlib.Path(
            "../Отчёты"
        )
        )

        generate_pdf(
            file,
            file_pdf
        )

        pdf_path = str(
            pathlib.Path(
                "../Отчёты",
                f"Отчёт № {order[0]}.pdf"
            )
        )

        time.sleep(30)

        with app.open_resource(pdf_path) as fp:

            msg.attach(
                f"Отчёт №{order[0]}.pdf",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                fp.read()
            )

            msg.html = html

        mail.send(msg)
        print("Sending email")
        return "OK"

    except Exception as ex:
        print(f"Ошибка в retry: {ex}")
        return "ERROR", 400


@app.route('/getData', methods=['GET', 'POST'])
@auth.login_required
def getData():
    page = int(json.loads(request.data)['page'])
    data = get_all_orders()
    result = []
    last_page = page // 20 + 2
    if page > last_page or page < 1:
        return []
    if last_page == page:
        for i in range(page * 20 - 20, len(data)):
            result.append(data[i])
    else:
        for i in range(page * 20 - 20, page * 20):
            result.append(data[i])

    result = json.dumps(result, ensure_ascii=False).encode('utf8')
    return result


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        name = request.form.get('name')
        if name == None or len(name) == 0:
            return "Пожалуйста, введите имя. На текущий момент поле не заполнено.", 400
        if not bool(re.search('[А-Яа-яЁё]', name)):
            return "Пожалуйста, введите имя, используя только русские буквы.", 400

        surname = request.form.get('surname')
        if surname == None or len(name) == 0:
            return "Пожалуйста, введите фамилию. На текущий момент поле не заполнено.", 400
        if not bool(re.search('[А-Яа-яЁё]', surname)):
            return "Пожалуйста, введите фамилию, используя только русские буквы.", 400

        patronymic = request.form.get('patronymic')
        if patronymic == None or len(patronymic) == 0:
            return "Пожалуйста, введите отчество. На текущий момент поле не заполнено.", 400
        if not bool(re.search('[А-Яа-яЁё]', patronymic)):
            return "Пожалуйста, введите отчество, используя только русские буквы.", 400

        region = request.form.get('region')
        if region == None or len(region) == 0:
            return "Пожалуйста, выберите регион. На текущий момент поле не заполнено.", 400
        if region not in regions:
            return "Пожалуйста, выберите корректный регион", 400

        birthdate = request.form.get('birthdate')
        format = "%Y-%m-%d"
        if birthdate == None or len(birthdate) == 0:
            return "Пожалуйста, введите дату рождения. На текущий момент поле не заполнено.", 400
        try:
            res = bool(datetime.strptime(birthdate, format))
        except ValueError:
            res = False
        if res == False:
            return "Пожалуйста, введите корректную дату рождения.", 400
        birthdate_check = datetime.strptime(birthdate, format)
        if datetime.now().year - birthdate_check.year > 100:
            return "Пожалуйста, введите корректную дату рождения.", 400

        passport = request.form.get('docnumber')
        docnumber = re.sub('\D', '', passport)
        if docnumber == None or len(docnumber) == 0:
            return "Пожалуйста, введите корректную серию и номер паспорта.", 400
        docnumber = docnumber.replace(' ', '')
        if not docnumber.isdigit() or len(docnumber) != 10:
            return "Пожалуйста, введите корректную серию и номер паспорта.", 400

        docdate = request.form.get('docdate')
        if docdate == None or len(docdate) == 0:
            return "Пожалуйста, введите корректную дату выдачи паспорта. На текущий момент поле не заполнено.", 400
        try:
            res = bool(datetime.strptime(docdate, format))
        except ValueError:
            res = False
        if res == False:
            return "Пожалуйста, введите корректную дату выдачи паспорта.", 400
        docdate_check = datetime.strptime(docdate, format)
        if docdate_check.year < 1991:
            return "Пожалуйста, введите корректную дату выдачи паспорта.", 400
        email = request.form.get('email')
        if email == None or len(email) == 0:
            return "Пожалуйста, введите корректную почту.", 400
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            return "Пожалуйста, введите корректную почту.", 400
        id_document = add_new_orders(name, surname, patronymic, region, birthdate, docnumber, docdate, email)

        return render_template('request_result.html',
                               id_document=id_document,
                               name=name,
                               surname=surname,
                               patronymic=patronymic,
                               region=region,
                               birthdate=birthdate,
                               docnumber=passport,
                               docdate=docdate,
                               email=email)
    else:
        return render_template('request.html',
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


@app.route('/yookassa/alert', methods=['GET', 'POST'])
async def alertYoo():
    print(request.json.get('type'))
    print(request.json.get('event'))
    object = request.json.get('object')
    print(object['id'])
    print(object['metadata']['orderMerchNumber'])

    if request.json.get('type') == 'notification' and request.json.get('event') == 'payment.succeeded':
        orderId = object['metadata']['orderMerchNumber']
        order = get_order_by_id_order(orderId)
        print(order)

        if order[9] != 'Отправлено' and order[9] != 'Оплачено':
            set_status_order(orderId, 'Оплачено')
            docnumber = order[6]
            docnumber = docnumber[0:2] + " " + docnumber[2:4] + " " + docnumber[4:]
            await generate_PDF_report(order[0], order[2], order[1], order[3], order[4], order[5], docnumber, order[7],
                                      "Api")
            msg = Message(f'Docreport отчёт №{order[0]}', sender="info24@docreport.ru", recipients=[order[8]])
            file = str(pathlib.Path("../Отчёты", f"Отчёт № {order[0]}.docx"))
            file_pdf = str(pathlib.Path("../Отчёты"))
            generate_pdf(file, file_pdf)
            pdf_path = str(pathlib.Path("../Отчёты", f"Отчёт № {order[0]}.pdf"))
            time.sleep(30)
            with app.open_resource(pdf_path) as fp:
                msg.attach(f"Отчёт №{order[0]}.pdf",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           fp.read())
            mail.send(msg)
            print("Sending email")
            set_status_order(orderId, 'Отправлено')
            # text = "Отчет отправлен order[0]"
            # send_message(text)

    data = {
        "type": "success"
    }
    return jsonify(request.json.get('object'))


@app.route('/create', methods=['GET', 'POST'])
def create():
    id_document = request.form.get('id_document')
    action = request.form.get('action')
    if action == 'РЕДАКТИРОВАТЬ':
        name = request.form.get('name')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        region = request.form.get('region')
        birthdate = request.form.get('birthdate')
        passport = request.form.get('docnumber')
        docnumber = re.sub('\D', '', passport)
        docdate = request.form.get('docdate')
        email = request.form.get('email')
        delete_orders(id_document)
        return render_template('request.html', id_document=id_document,
                               name=name,
                               surname=surname,
                               patronymic=patronymic,
                               region=region,
                               birthdate=birthdate,
                               docnumber=passport,
                               docdate=docdate,
                               email=email,
                               pasdatamax=str(date.today()),
                               dobdatamin=str(datetime.now().year - 100)
                               )
    if action == 'ОПЛАТИТЬ QIWI':
        id_document = request.form.get('id_document')
        # Отправка оповещение о нажатии на кнопку оплаты id_document
        # text = "Нажали кнопку оплатить по документу id_document"
        # send_message(text)
        return render_template('paypage.html', id_document=id_document, email=request.form.get('email'))

    if action == 'ОПЛАТИТЬ':
        id_document = request.form.get('id_document')
        kassa = addYooKassaPay(100, 'RUB', id_document, request.form)
        # Отправка оповещение о нажатии на кнопку оплаты id_document
        # text = "Нажали кнопку оплатить по документу id_document"
        # send_message(text)
        return render_template('paypage_yoo.html', id_document=id_document, email=request.form.get('email'),
                               form=request.form, url=kassa)

    return 'Ошибка при формировании отчёта', 400


@app.route('/paymentsAPI', methods=['GET', 'POST'])
async def paymentsAPI():
    html = """<p>В приложении к письму прикреплен заказанный Вами отчет о физическом лице.</p>
                <p>Полнота и корректность данных зависит от верности данных заполненных Вами при оформлении заказа.</p>
                <p>Мы &ndash; за достоверную информацию, поэтому используем только официальные базы данных.</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>С уважением,</p>
                <p>DOCREPORT.RU</p> """

    try:
        orderId = request.form.get('orderId')
        paymentStatus = request.form.get('paymentStatus')
        if paymentStatus == '5':
            order = get_order_by_id_order(orderId)
            if order[9] != 'Отправлено' and order[9] != 'Оплачено':
                set_status_order(orderId, 'Оплачено')
                doc_number = order[6]
                doc_number = doc_number[0:2] + " " + doc_number[2:4] + " " + doc_number[4:]
                print('101', order)
                await generate_PDF_report(order[0], order[2], order[1], order[3], order[4], order[5], doc_number,
                                          order[7], "Api")
                msg = Message(f'Docreport отчёт №{order[0]}', sender="info24@docreport.ru", recipients=[order[8]])
                file = str(pathlib.Path("../Отчёты", f"Отчёт № {order[0]}.docx"))
                file_pdf = str(pathlib.Path("../Отчёты"))
                generate_pdf(file, file_pdf)
                pdf_path = str(pathlib.Path("../Отчёты", f"Отчёт № {order[0]}.pdf"))
                time.sleep(30)
                with app.open_resource(pdf_path) as fp:
                    msg.attach(f"Отчёт №{order[0]}.pdf",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               fp.read())
                    msg.html = html
                mail.send(msg)
                print("Sending email")
                set_status_order(orderId, 'Отправлено')
                # text = "Отчет отправлен order[0]"
                # send_message(text)
        return ('OK')
    except Exception as ex:
        print(ex)
        return ('OK')


@app.route('/fuse', methods=['GET', 'POST'])
def fuse():
    try:
        data = request.data.decode('utf-8')
        data = json.loads(data)
        id_document = data['id_document'].replace('Заказ №', '')
        id_order = data['id_order']
        set_id_order(id_document, id_order)
        return "id платежа успешно привязан"
    except:
        return "Ошибка при установки id платежа"


@app.route('/oferta', methods=['GET', 'POST'])
def oferta():
    return render_template('Публичная оферта.html')


@app.route('/personal-data', methods=['GET', 'POST'])
def personal_data():
    return render_template('Политика.html')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    return render_template('Контакты.html')


@app.route('/yookassa', methods=['GET', 'POST'])
def yookassa_create():
    res = "yoomoney"
    return res


@app.route('/icon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'icon.ico', mimetype='icon.icon')