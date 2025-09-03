from datetime import datetime
from time import strptime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message # InlineKeyboardButton, InlineKeyboardMarkup

from config import dp, regions, bot
from processes.compilator import compilation
from processes.admin import admin, admins, nextOrder, prevOrder, showByID, retry


currentUser = {}
mainRouter = Router()
adminPanel = []
curTGID = []
blacklistOfWordsForUser = ('admin', '/show', '/retry', '/next', '/back')


class Messages:
    class Start:
        start: str = 'Добро пожаловать! Напишите ФИО интересующего лица.'

    class Fullname:
        valid: str = 'Введите регион интересующего лица'
        exception: str = 'Введите фамилию, имя и отчество'

    class Region:
        valid: str = 'Введите дату рождения'
        exception: str = 'Регион невалиден'

    class Birthdate:
        valid: str = 'Введите серию и номер паспорта'
        exception: str = 'Введите дату рождения в данном формате: ДД.ММ.ГГГГ'

    class Passport:
        class Number:
            valid: str = 'Введите дату выдачи паспорта'
            exception: str = 'Введённые серия и номер паспорта невалидны. Введите в формате 12 34 567890'

        class Date:
            valid: str = 'Тут должна быть оплата, после которой отправится отчёт в формате PDF.'
            exceptionTimeFormat: str = 'Введите корректную дату выдачи паспорта в формате ДД.ММ.ГГГГ'
            exceptionLessThan14: str = 'Дата выдачи невалидна - она меньше 14 лет.'


class Data(StatesGroup):
    fullname = State()
    region = State()
    birthdate = State()
    passport = State()
    passportDate = State()


class LessThan14Error(Exception):
    pass


@mainRouter.message(Command('next'))
async def nextOrderHandler(message: Message) -> None:
    await nextOrder(None, message)


@mainRouter.message(Command('back'))
async def prevOrderHandler(message: Message) -> None:
    await prevOrder(None, message)


@mainRouter.message(Command('retry'))
async def retryHandler(message: Message) -> None:
    await retry(message)


@mainRouter.message(Command('show'))
async def showByIDHandler(message: Message) -> None:
    await showByID(message)


@dp.message(CommandStart())
async def commandStartHandler(message: Message, state: FSMContext) -> None:
    await state.set_state(Data.fullname)
    if message.from_user.id not in admins:
        await message.answer(Messages.Start.start)
        currentUser.setdefault(message.from_user.id, {'fullname': str, 'region': str, 'birthdate': datetime, 'passport': str, 'passportDate': datetime})


@mainRouter.message(F.text == 'admin')
async def adminHandler(message: Message):
    await admin(message)


@mainRouter.message(F.text, Data.fullname)
async def processFullname(message: Message, state: FSMContext) -> None:
    if message.text != 'admin' and "/" and "skip" not in message.text:
        fullname = message.text.split()

        if len(fullname) == 3:
            currentUser[message.from_user.id]['fullname'] = message.text
            await state.set_state(Data.region)
            await message.answer(Messages.Fullname.valid)

        else:
            await message.answer(Messages.Fullname.exception)
            await state.set_state(Data.fullname)


@mainRouter.message(Data.region)
async def processRegion(message: Message, state: FSMContext) -> None:
    if message.text in regions:
        currentUser[message.from_user.id]['region'] = message.text
        await state.set_state(Data.birthdate)
        await message.answer(Messages.Region.valid)

    else:
        await message.answer(Messages.Region.exception)
        await state.set_state(Data.region)


@mainRouter.message(Data.birthdate)
async def processBirthdate(message: Message, state: FSMContext):
    try:
        currentUser[message.from_user.id]['birthdate'] = datetime.strptime(message.text, '%d.%m.%Y')
        await state.set_state(Data.passport)
        await message.answer(Messages.Birthdate.valid)

    except ValueError:
        await message.answer(Messages.Birthdate.exception)
        await state.set_state(Data.birthdate)


@mainRouter.message(Data.passport)
async def processPassport(message: Message, state: FSMContext):
    try:
        if message.text[2] == ' ' and message.text[5] == ' ' and len(message.text) == 12:
            currentUser[message.from_user.id]['passport'] = message.text
            await state.set_state(Data.passportDate)
            await message.answer(Messages.Passport.Number.valid)

        else:
            await message.answer(Messages.Passport.Number.exception)
            await state.set_state(Data.passport)
    except IndexError:
        await message.answer(Messages.Passport.Number.exception)
        await state.set_state(Data.passport)


@mainRouter.message(Data.passportDate)
async def processPassportDate(message: Message, state: FSMContext):
    try:
        passportDate = strptime(message.text, '%d.%m.%Y')
        birthdate = currentUser.get(message.from_user.id).get('birthdate')
        passportDateDatetime = datetime(*passportDate[:6])
        dates_diff = passportDateDatetime - birthdate
        age_in_days = dates_diff.days
        age_in_years = age_in_days / 365
        if age_in_years < 14:
            raise LessThan14Error

        currentUser[message.from_user.id]['passportDate'] = passportDateDatetime
        await message.answer(Messages.Passport.Date.valid)
        returned = await compilation(currentUser, message.from_user.id, message.chat.id)
        await bot.send_document(message.chat.id, returned[0])
        await bot.send_document(message.chat.id, returned[1])

    except LessThan14Error:
        await message.answer(Messages.Passport.Date.exceptionLessThan14)
        await state.set_state(Data.passportDate)

    except ValueError:
        await message.answer(Messages.Passport.Date.exceptionTimeFormat)
