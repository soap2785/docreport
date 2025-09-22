import datetime

import requests

from businessLogic.classForParsers import CompiledData
from mainDIR.bot.src.config import proxies


def checkINN(fullname, birthdate, passport, passportDate):
    """
    Возвращает ИНН на основе предоставленных данных, используя POST-запрос к сервису Налоговой службы.

    Args:
        fullname: Полное имя (ФИО) в виде строки, разделенной пробелами.
        birthdate: Дата рождения в формате datetime.date.
        passport: Номер паспорта.
        passportDate: Дата выдачи паспорта в формате datetime.date.

    Returns:
        Словарь с данными ответа от Налоговой службы (включая ИНН, если найден)
        или None в случае ошибки.
    """
    print(datetime.datetime.now(), "INN")

    try:
        url = "https://service.nalog.ru/inn-proc.do"

        fullname = fullname.split()
        surname = fullname[0]
        name = fullname[1]
        patronymic = fullname[2]
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        passportDate = datetime.datetime.strptime(passportDate, "%Y-%m-%d")
        birthdate = datetime.datetime.strftime(birthdate, '%d.%m.%Y')
        passportDate = datetime.datetime.strftime(passportDate, '%d.%m.%Y')

        data = {
            "fam": surname,
            "nam": name,
            "otch": patronymic,
            "bdate": birthdate,
            "bplace": "",
            "doctype": "21",
            "docno": passport,
            "docdt": passportDate,
            "c": "innMy",
            "captcha": "",
            "captchaToken": "",
        }

        resp = requests.post(url=url, data=data, proxies={'https': proxies.get('https')})
        resp.raise_for_status()
        resp = resp.json()

        if resp.get('code') in (1, 200):
            CompiledData.inn = resp.get('inn')
        else:
            CompiledData.inn = resp.get('code')

    except requests.exceptions.RequestException as e:  # Более конкретный обработчик исключений
        print(e)
        return None

    except Exception as e:  # Обрабатываем остальные исключения, если они возникнут
        print(f"Произошла ошибка: {e}")
        return None

    finally:
        print(datetime.datetime.now(), "INN")
