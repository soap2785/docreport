import os
import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from mainDIR.bot.config import dp, regions, bot, admins
from mainDIR.processes.bot.adminTemplates.ShowOrderById import showByID
from mainDIR.processes.bot.adminTemplates.resendCurrentOrder import resend
from mainDIR.processes.bot.adminTemplates.showAdminPanel import admin
from mainDIR.processes.bot.adminTemplates.showNextOrder import nextOrder
from mainDIR.processes.bot.adminTemplates.showPrevOrder import prevOrder
from mainDIR.processes.compile.compileHandler import compilation
from mainDIR.processes.bot.classes import RequesterData, Messages, Data, LessThan14Error

mainRouter = Router()
blacklistOfWordsForUser = ('admin', '/show', '/retry', '/next', '/back')


@mainRouter.message(Command('next'))
async def nextOrderHandler(message: Message) -> None:
    await nextOrder(None, message)


@mainRouter.message(Command('back'))
async def prevOrderHandler(message: Message) -> None:
    await prevOrder(None, message)


@mainRouter.message(Command('retry'))
async def retryHandler(message: Message) -> None:
    await resend(message)


@mainRouter.message(Command('show'))
async def showByIDHandler(message: Message) -> None:
    await showByID(message)


@dp.message(CommandStart())
async def commandStartHandler(message: Message, state: FSMContext) -> None:
    if message.from_user.id not in admins:
        await state.set_state(Data.fullname)
        await message.answer(Messages.Start.start)
    else:
        await admin(message)


@mainRouter.message(F.text, Data.fullname)
async def processFullname(message: Message, state: FSMContext) -> None:
    if message.text != 'admin' and "/" and "skip" not in message.text:
        fullname = message.text.split()

        if len(fullname) == 3:
            RequesterData.fullname = message.text
            await state.set_state(Data.region)
            await message.answer(Messages.Fullname.valid)

        else:
            await message.answer(Messages.Fullname.exception)
            await state.set_state(Data.fullname)


@mainRouter.message(Data.region)
async def processRegion(message: Message, state: FSMContext) -> None:
    if message.text in regions:
        RequesterData.region = message.text
        await state.set_state(Data.birthdate)
        await message.answer(Messages.Region.valid)

    else:
        await message.answer(Messages.Region.exception)
        await state.set_state(Data.region)


@mainRouter.message(Data.birthdate)
async def processBirthdate(message: Message, state: FSMContext):
    try:
        RequesterData.birthdate = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
        await state.set_state(Data.passport)
        await message.answer(Messages.Birthdate.valid)

    except ValueError:
        await message.answer(Messages.Birthdate.exception)
        await state.set_state(Data.birthdate)


@mainRouter.message(Data.passport)
async def processPassport(message: Message, state: FSMContext):
    try:
        if message.text[2] == ' ' and message.text[5] == ' ' and len(message.text) == 12:
            RequesterData.passport = message.text
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
        passportDate = datetime.datetime.strptime(message.text, '%d.%m.%Y').date()
        birthdate = RequesterData.birthdate
        dates_diff = passportDate - birthdate
        age_in_days = dates_diff.days
        age_in_years = age_in_days / 365
        if age_in_years < 14:
            raise LessThan14Error

        RequesterData.passportDate = passportDate
        await message.answer(Messages.Passport.Date.valid)
        print(datetime.datetime.now())
        returned = await compilation(message.from_user.id, message)
        await bot.send_message(message.chat.id, returned[0])
        await bot.send_document(message.chat.id, FSInputFile(returned[1]))
        await bot.send_document(message.chat.id, FSInputFile(returned[2]))
        print(datetime.datetime.now())
        os.remove(returned[1])
        os.remove(returned[2])

    except LessThan14Error:
        await message.answer(Messages.Passport.Date.exceptionLessThan14)
        await state.set_state(Data.passportDate)

    except ValueError as e:
        print(e)
        await message.answer(Messages.Passport.Date.exceptionTimeFormat)
