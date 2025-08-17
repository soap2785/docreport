from datetime import datetime
from time import strptime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from config import dp, regions
from processes.compilator import compilation


currentUser = {}
mainRouter = Router()

class Data(StatesGroup):
    fullname = State()
    region = State()
    birthdate = State()
    passport = State()
    passportDate = State()


@dp.message(CommandStart())
async def commandStartHandler(message: Message, state: FSMContext) -> None:
    await state.set_state(Data.fullname)
    await message.answer('Добро пожаловать! Напишите ФИО интересующего лица.')
    currentUser.setdefault(message.from_user.id, {'fullname': '', 'region': '', 'birthdate': '', 'passport': '', 'passportDate': ''})


@mainRouter.message(Data.fullname)
async def process_fullname(message: Message, state: FSMContext) -> None:
    currentUser[message.from_user.id]['fullname'] = message.text
    await state.set_state(Data.region)
    await message.answer('Введите регион интересующего лица')


@mainRouter.message(Data.region)
async def process_region(message: Message, state: FSMContext) -> None:
    if message.text in regions:
        currentUser[message.from_user.id]['region'] = message.text
        await state.set_state(Data.birthdate)
        await message.answer('Введите дату рождения')

    else:
        await message.answer('Регион невалиден')


@mainRouter.message(Data.birthdate)
async def process_birthdate(message: Message, state: FSMContext):
    try:
        strptime(message.text, '%d.%m.%Y')
        currentUser[message.from_user.id]['birthdate'] = message.text
        await state.set_state(Data.passport)
        await message.answer('Введите серию и номер паспорта')

    except:
        await message.answer('Введите дату рождения в данном формате: ДД.ММ.ГГГГ')
        await state.set_state(Data.birthdate)


@mainRouter.message(Data.passport)
async def process_passport(message: Message, state: FSMContext):
    if message.text[2] == ' ' and message.text[5] == ' ' and len(message.text) == 10:
        currentUser[message.from_user.id]['passport'] = message.text
        await state.set_state(Data.passportDate)
        await message.answer('Введите дату выдачи паспорта')

    else:
        await message.answer('Введённые серия и номер паспорта невалидны. Введите в формате 12 34 5678')
        await state.set_state(Data.passport)


@mainRouter.message(Data.passportDate)
async def process_passportDate(message: Message, state: FSMContext):
    try:
        passportDate = strptime(message.text, '%d.%m.%Y')
        birthdate = strptime(currentUser.get(message.from_user.id).get('birthdate'), '%d.%m.%Y')
        passportDate_datetime = datetime(*passportDate[:6])
        birthdate_datetime = datetime(*birthdate[:6])
        dates_diff = passportDate_datetime - birthdate_datetime
        age_in_days = dates_diff.days
        age_in_years = age_in_days / 365.25
        if age_in_years < 14:
            raise ValueError('Некорректная дата выдачи')

        currentUser[message.from_user.id]['passportDate'] = message.text
        await message.answer('Тут должна быть оплата по ЮКассе')

    except ValueError:
        await message.answer('Дата выдачи невалидна - она меньше 14 лет.')
        del currentUser[message.from_user.id]

    except:
        await message.answer('Введите корректную дату выдачи паспорта')
        await state.set_state(Data.passportDate)
