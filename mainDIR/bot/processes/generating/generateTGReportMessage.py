import datetime

from mainDIR.bot.processes.classesForBot import RequesterData
from businessLogic.classForParsers import CompiledData


async def generateMessage() -> str:
    birthdate = datetime.datetime.strptime(RequesterData.birthdate, "%Y-%m-%d")
    docDate = datetime.datetime.strptime(RequesterData.passportDate, "%Y-%m-%d")
    birthdate = datetime.datetime.strftime(birthdate, '%d.%m.%Y')
    passportDate = datetime.datetime.strftime(docDate, '%d.%m.%Y')

    fullname = RequesterData.fullname
    region = RequesterData.region
    passport = RequesterData.passport

    inn = CompiledData.inn
    fns = CompiledData.fns
    ter = CompiledData.ter
    civ = CompiledData.civ
    bank = CompiledData.bank
    iss = CompiledData.iss

    if CompiledData.iss not in ('Ничего не найдено', 'Сервис недоступен'):
        text = (f"ФИО: {fullname}"
                f"\nРегион: {region}"
                f"\nДата рождения: {birthdate}"
                f"\nСерия и номер паспорта: {passport}"
                f"\nДата выдачи паспорта: {passportDate}"
                f"\n"
                f"\nИНН: {inn}"
                f"\nФНС: {fns}"
                f"\nБаза террористов: {ter}"
                f"\nГосслужба: {civ}"
                f"\nБанкротство: {bank}"
                f"\nИсполнительные производства в файлах. \nКоличество записей: {len(iss)}"
                f"\n")
    else:
        text = (f"ФИО: {fullname}"
                f"\nРегион: {region}"
                f"\nДата рождения: {birthdate}"
                f"\nСерия и номер паспорта: {passport}"
                f"\nДата выдачи паспорта: {passportDate}"
                f"\n"
                f"\nИНН: {inn}"
                f"\nФНС: {fns}"
                f"\nБаза террористов: {ter}"
                f"\nГосслужба: {civ}"
                f"\nБанкротство: {bank}"
                f"\nИсполнительные производства: {iss}"
                f"\n")
    return text