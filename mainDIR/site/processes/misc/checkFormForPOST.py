import re
from datetime import datetime, date

from flask import request

from mainDIR.site.src.config import regions


async def laconicReturning() -> str | None | tuple:
    forRequest = ['name', 'surname', 'patronymic', 'region', 'birthdate', 'passport', 'passportDate', 'email']
    forRequestRussian = ['имя', 'фамилию', 'отчество', 'регион', 'дату рождения', 'серию и номер паспорта',
                         'дату выдачи паспорта', 'почту']

    for index, inputForm in enumerate(forRequest):
        if inputForm != 'region' and inputForm != 'birthdate' and inputForm != 'passportDate' and inputForm != 'email' and inputForm != 'passport':
            if request.form.get(inputForm) is None or len(request.form.get(inputForm)) == 0:
                return f"Пожалуйста, введите {forRequestRussian[index]}. На текущий момент поле не заполнено.", 400
            if not bool(re.search('[А-Яа-яЁё]', request.form.get(inputForm))):
                return f"Пожалуйста, введите {forRequestRussian[index]}, используя только русские буквы.", 400

        elif inputForm == 'region':
            if request.form.get(inputForm) is None or len(request.form.get(inputForm)) == 0:
                return "Пожалуйста, выберите регион. На текущий момент поле не заполнено.", 400
            if request.form.get(inputForm) not in regions:
                return "Пожалуйста, выберите корректный регион", 400

        elif inputForm == 'birthdate' or inputForm == 'passportDate':

            if request.form.get(inputForm) is None or len(request.form.get(inputForm)) == 0:
                return f"Пожалуйста, введите {forRequestRussian[index]}. На текущий момент поле не заполнено.", 400
            try:
                res = bool(datetime.strptime(request.form.get(inputForm), "%d.%m.%Y"))
            except ValueError:
                return f"Пожалуйста, введите корректную {forRequestRussian[index]}.", 400
            if datetime.now().year - datetime.strptime(request.form.get(inputForm), "%d.%m.%Y").year > 100:
                return f"Пожалуйста, введите корректную {forRequestRussian[index]}.", 400
            passportDate: date = datetime.strptime(request.form.get(inputForm), "%d.%m.%Y")
            if passportDate.year < 1991:

                return "Пожалуйста, введите корректную дату выдачи паспорта.", 400

        elif inputForm == 'email':
            if request.form.get(inputForm) is None or len(request.form.get(inputForm)) == 0:
                return "Пожалуйста, введите корректную почту.", 400
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if not re.fullmatch(regex, request.form.get(inputForm)):
                return "Пожалуйста, введите корректную почту.", 400
        elif inputForm == 'passport':
            passport = re.sub('\D', '', request.form.get(inputForm))
            if passport is None or len(passport) == 0:
                return "Пожалуйста, введите корректную серию и номер паспорта.", 400
            passport = passport.replace(' ', '')
            if not passport.isdigit() or len(passport) != 10:
                return "Пожалуйста, введите корректную серию и номер паспорта.", 400
    return None
