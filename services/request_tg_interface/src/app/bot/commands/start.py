from app.bot.commands.admin.start import showAdminPanel
from aiogram.filters import CommandStart
from aiogram import Router

from aiogram.fsm.context import FSMContext

from app.bot.states import Data
from config import ADMINS
from aiogram.types import (
    InlineKeyboardButton as IKB,
    InlineKeyboardMarkup as IKM,
    Message
)

router = Router(name=__name__)


KEYBOARD = IKM(
    inline_keyboard=[
        [
            IKB(text='ФИО', callback_data='fullname'),
            IKB(text='Регион', callback_data='region'),
            IKB(text='Дата рождения', callback_data='birthdate')
        ], [
            IKB(text='Серия паспорта', callback_data='passport_series'),
            IKB(text='Номер паспорта', callback_data='passport_number'),
            IKB(text='Дата выдачи паспорта', callback_data='passport_date')
        ], [
            IKB(text='Готово', callback_data='submit'),
            IKB(text='Отмена', callback_data='cancel')
        ]
    ]
)


@router.message(CommandStart())
async def onStart(
    message: Message, state: FSMContext
) -> Message:
    if message.from_user.id in ADMINS:
        return await showAdminPanel(message, state)

    await state.update_data(
        fullname='...', region='...', birthdate='...',
        birthdate_datetime='...', passport_series='...',
        passport_number='', passport_date='...'
    )
    await state.set_state(Data.fullname)
    return await state.update_data(
        index_message=await message.answer(
            'Добро пожаловать! Введите данные интересующего лица.\n\n'
            f'ФИО: {await state.get_value("fullname")}\n'
            f'Регион: {await state.get_value("region")}\n'
            f'Дата рождения: {await state.get_value("birthdate")}\n'
            'Серия и номер паспорта: '
            f'{await state.get_value("passport_series")} '
            f'{await state.get_value("passport_number")}\n'
            f'Дата выдачи паспорта: {await state.get_value("passport_date")}',
            reply_markup=KEYBOARD
        )
    )
