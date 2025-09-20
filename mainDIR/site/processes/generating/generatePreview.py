import datetime

from businessLogic.classForParsers import CompiledData
from mainDIR.site.processes.misc.classesForSite import RequesterData


async def generatePreview() -> str:
    surname = RequesterData.surname
    name = RequesterData.name
    patronymic = RequesterData.patronymic
    region = RequesterData.region
    birthdate = RequesterData.birthdate
    passport = RequesterData.passport
    passportDate = RequesterData.passportDate
    fullname = surname + ' ' + name + ' ' + patronymic

    try:
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        passportDate = datetime.datetime.strptime(passportDate, "%Y-%m-%d")
        birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
        passportDate = datetime.datetime.strftime(passportDate, "%d.%m.%Y")

    except Exception as e:
        print(e)

    inn = CompiledData.inn
    fns = CompiledData.fns
    ter = CompiledData.ter
    civ = CompiledData.civ
    bank = CompiledData.bank
    iss = CompiledData.iss

    if iss and iss not in ('Ничего не найдено', 'Сервис недоступен'):
        text = f"""<p>ФИО: {fullname}</p>
        <p>Регион: {region}</p>
        <p>Дата рождения: {birthdate}</p>
        <p>Серия и номер паспорта: {passport}</p>
        <p>Дата выдачи паспорта: {passportDate}</p>
        <p>&nbsp;</p>
        <p>ИНН: {inn}</p>
        <p>ФНС: {fns}</p>
        <p>База террористов: {ter}</p>
        <p>Госслужба: {civ}</p>
        <p>Банкротство: {bank}</p>
        <p>Исполнительные производства в файлах.</p>
        <p>Количество записей: {len(iss)}</p>"""

    else:
        text = f"""<p>&nbsp;</p>
        <p>ФИО: {fullname}</p>
        <p>Регион: {region}</p>
        <p>Дата рождения: {birthdate}</p>
        <p>Серия и номер паспорта: {passport}</p>
        <p>Дата выдачи паспорта: {passportDate}</p>
        <p>&nbsp;</p>
        <p>ИНН: {inn}</p>
        <p>ФНС: {fns}</p>
        <p>База террористов: {ter}</p>
        <p>Госслужба: {civ}</p>
        <p>Банкротство: {bank}</p>
        <p>Исполнительные производства: {iss}</p>"""
    return text