import datetime
import json
import os
import pathlib
from sqlite3 import connect

from flask import request
from flask_mail import Message

from mainDIR.site.processes.misc.classesForSite import RequesterData
from mainDIR.site.processes.compile.compilingProcess import compileData
from mainDIR.site.processes.generating.generateDOCXReportFile import generateDOCXReport
from mainDIR.site.processes.generating.generatePDFReportFile import generatePDFReport
from mainDIR.site.processes.generating.generatePreview import generatePreview
from mainDIR.site.src.config import app, mail


async def retry():
    try:
        ID = int(json.loads(request.data)['id'])
        with connect('databaseSITE.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE id = ?", (ID,))
            order = cur.fetchone()

        RequesterData.name = order[1]
        RequesterData.surname = order[2]
        RequesterData.patronymic = order[3]
        RequesterData.region = order[4]
        RequesterData.birthdate = order[5]
        RequesterData.passport = order[6]
        RequesterData.passportDate = order[7]

        try:
            birthdate = datetime.datetime.strptime(order[5], "%d.%m.%Y")
            RequesterData.birthdate = datetime.datetime.strftime(birthdate, "%Y-%m-%d")
            passportDate = datetime.datetime.strptime(order[7], "%d.%m.%Y")
            RequesterData.passportDate = datetime.datetime.strftime(passportDate, "%Y-%m-%d")

        except Exception as e:
            print(e)
        await compileData()
        await generatePDFReport()
        await generateDOCXReport()
        preview = await generatePreview()

        msg = Message(f'Docreport отчёт №{order[0]}', sender="info24@docreport.ru", recipients=[order[8]])
        pdf_path = str(pathlib.Path(f"reportSITE.pdf"))
        docx_path = str(pathlib.Path(f"reportSITE.docx"))
        html = f"""<p>В приложении к письму прикреплен заказанный Вами отчет о физическом лице.</p>
                <p>Полнота и корректность данных зависит от верности данных заполненных Вами при оформлении заказа.</p>
                <p>Мы &ndash; за достоверную информацию, поэтому используем только официальные базы данных.</p>
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                {preview}
                <p>&nbsp;</p>
                <p>&nbsp;</p>
                <p>С уважением,</p>
                <p>DOCREPORT.RU</p> """

        with app.open_resource(pdf_path) as fp:
            msg.attach(f"reportSITE.pdf",
                       "application/pdf",
                       fp.read())

        with app.open_resource(docx_path) as fp:
            msg.attach(f"reportSITE.docx",
                       "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                       fp.read())
            msg.html = html

        mail.send(msg)
        print("Sending email")
        os.remove(f"reportSITE.docx")
        os.remove(f"reportSITE.pdf")
        return "OK"

    except Exception as e:
        print(f"Ошибка в retry: {e}")
        return "ERROR", 400