import datetime


class RequesterData:
    name: str
    surname: str
    patronymic: str
    region: str
    birthdate: str | datetime.date
    passport: str
    passportDate: str | datetime.date
