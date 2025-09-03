import datetime

import aiohttp

from mainDIR.config import proxies


async def suggestInnPOST(fullname, birthdate, docnumber, docdate) -> dict | str:
    fullname = fullname.split()
    surname = fullname[0]
    name = fullname[1]
    patronymic = fullname[2]

    birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d %H:%M:%S')
    birthdate = birthdate.strftime('%d.%m.%Y')

    docdate = datetime.datetime.strptime(docdate, '%Y-%m-%d %H:%M:%S')
    docdate = docdate.strftime('%d.%m.%Y')

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

    proxy = None
    if proxies and proxies.get("httpProxy"):
        proxy = proxies["httpProxy"]

    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(url, data=data, proxy=proxy) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            print(f"[ERROR] HTTP ошибка: {e}")
            return "Ошибка при подключении к ФНС"
