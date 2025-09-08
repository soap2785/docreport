import datetime

import httpx

from mainDIR.bot.config import proxies


async def suggestInnPOST(fullname, birthdate, passport, passportDate):
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
    try:
        url = "https://service.nalog.ru/inn-proc.do"

        fullname = fullname.split()
        surname = fullname[0]
        name = fullname[1]
        patronymic = fullname[2]
        birthdate = datetime.datetime.strftime(birthdate, '%d.%m.%Y')
        passportDate = datetime.datetime.strftime(passportDate, '%d.%m.%Y')

        async with httpx.AsyncClient(proxy=proxies.get('https')) as client:
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
            resp = await client.post(url=url, data=data)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        print(e)
        return None
