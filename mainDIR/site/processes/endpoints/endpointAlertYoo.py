import pathlib
from sqlite3 import connect

from flask import request, jsonify
from flask_mail import Message

from mainDIR.site.processes.compile.compilingProcess import compileData
from mainDIR.site.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.site.processes.generating.generatePDFReportFile import generatePDFReport
from mainDIR.site.src.config import app, mail


async def alertYoo():
    html = """<p>В приложении к письму прикреплен заказанный Вами отчет о физическом лице.</p>
                <p>Полнота и корректность данных зависит от верности данных заполненных Вами при оформлении заказа.</p>
                <p>Мы &ndash; за достоверную информацию, поэтому используем только официальные базы данных.</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>С уважением,</p>
                <p>DOCREPORT.RU</p> """
    print(request.json.get('type'))
    print(request.json.get('event'))
    object = request.json.get('object')
    print(object['id'])
    print(object['metadata']['orderMerchNumber'])
    try:

        if request.json.get('type') == 'notification' and request.json.get('event') == 'payment.succeeded':
            orderId = object['metadata']['orderMerchNumber']
            with connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM orders WHERE idForOrder = ?", (orderId,))
                order = cur.fetchone()

            print(order)
            if order[9] != 'Отправлено' and order[9] != 'Оплачено':
                with connect('databaseSITE.db') as conn:
                    cur = conn.cursor()
                    cur.execute("UPDATE orders SET state = ? WHERE id = ?", (orderId, "Оплачено"))
                    conn.commit()

                await compileData()
                await generatePDFReport()
                await generateDOCXReport()
                msg = Message(f'Docreport отчёт №{order[0]}', sender="info24@docreport.ru", recipients=[order[8]])

                pdf_path = str(pathlib.Path(f"reportSITE.pdf"))
                docx_path = str(pathlib.Path(f"reportSITE.docx"))
                with app.open_resource(docx_path) as fp:
                    msg.attach("reportSITE.pdf",
                               "application/pdf",
                               fp.read())
                with app.open_resource(pdf_path) as fp:
                    msg.attach("reportSITE.docx",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               fp.read())
                    msg.html = html
                mail.send(msg)
                print("Sending email")
                with connect('databaseSITE.db') as conn:
                    cur = conn.cursor()
                    cur.execute("UPDATE orders SET state = ? WHERE idForOrder = ?", ('Отправлено', orderId,))
                    conn.commit()
                # text = "Отчет отправлен order[0]"
                # send_message(text)

        data = {"type": "success"}
        return jsonify(request.json.get('object'))

    except Exception as e:
        print("Ошибка в endpointAlertYoo:", e)
        return None