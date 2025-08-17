import requests

from oldconfig import proxies

def suggestInn(fullname, birthdate, docnumber, docdate) -> dict:
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]
    url = "https://service.nalog.ru/inn-proc.do"
    data = {
        "fam": surname,
        "nam": name,
        "otch": patronymic,
        "bdate": birthdate,
        "bplace": "",
        "doctype": "21",
        "docno": docnumber,
        "docdt": docdate,
        "c": "innMy",
        "captcha": "",
        "captchaToken": "",
    }
    resp = requests.post(url = url, data = data, proxies = proxies)
    resp.raise_for_status()
    return resp.json()