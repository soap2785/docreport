import datetime

from aiogram.types import Message

from mainDIR.processes.bot.classes import RequesterData


async def generateMessage(message: Message, compiledData: dict) -> str:
    birthdate = datetime.datetime.strftime(RequesterData.birthdate, '%d.%m.%Y')
    passportDate = datetime.datetime.strftime(RequesterData.passportDate, '%d.%m.%Y')
    fullname = RequesterData.fullname
    region = RequesterData.region
    passport = RequesterData.passport
    text = (f"ФИО: {fullname}"
            f"\nРегион: {region}"
            f"\nДата рождения: {birthdate}"
            f"\nСерия и номер паспорта: {passport}"
            f"\nДата выдачи паспорта: {passportDate}"
            f"\n"
            f"\nИНН: {compiledData.get('inn').get('inn')}"
            f"\nФНС: {compiledData.get('fns')}"
            f"\nБаза террористов: {compiledData.get('ter')}"
            f"\nГосслужба: {compiledData.get('civ')}"
            f"\nБанкротство: {compiledData.get('bank')}"
            f"\nИсполнительные производства в файлах. \nКоличество записей: {len(compiledData.get('iss'))}"
            f"\n")
    return text