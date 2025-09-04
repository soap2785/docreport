import datetime

import requests

from mainDIR.config import proxies


def suggestInnPOST(fullname, birthdate, docNumber, docDate):
    url = "https://service.nalog.ru/inn-proc.do"

    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]

    if type(birthdate) is not datetime.datetime:
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d %H:%M:%S")
        birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
    else:
        birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")

    if type(docDate) is not datetime.datetime:
        docDate = datetime.datetime.strptime(docDate, "%Y-%m-%d %H:%M:%S")
        docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")
    else:
        docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")

    data = {
        "fam": surname,
        "nam": name,
        "otch": patronymic,
        "bdate": birthdate,
        "bplace": "",
        "doctype": "21",
        "docno": docNumber,
        "docdt": docDate,
        "c": "innMy",
        "captcha": "",
        "captchaToken": "",
    }
    resp = requests.post(url=url, data=data, proxies=proxies)
    resp.raise_for_status()
    return resp.json()
