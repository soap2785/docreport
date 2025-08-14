import requests

from config import proxies

def suggest_inn(surname, name, patronymic, birthdate, docnumber, docdate) -> dict:
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