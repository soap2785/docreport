import requests

from mainDIR.config import proxies

def suggestInn(fullname, birthdate, docnumber, docdate) -> dict:
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]
    print(surname, name, patronymic, 'adiawdiadawkdkasdkawdkaiwdiawkd')
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