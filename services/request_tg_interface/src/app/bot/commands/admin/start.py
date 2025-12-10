from aiogram import Router
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardButton as IKB,
    InlineKeyboardMarkup as IKM
)

router = Router(name=__name__)


async def showAdminPanel(message: Message, state: FSMContext) -> Message:
    last: Order = Order.select().order_by(Order.id.desc()).first()
    await state.update_data({'order_id': last.id})
    birthdate = datetime.strftime(last.birthdate.date(), '%d.%m.%Y')
    passport_date = datetime.strftime(last.passport_date.date(), '%d.%m.%Y')

    return await message.answer(
        'Админка\n\n'
        f'ФИО: {last.fullname}\n'
        f'Регион: {last.region}\n'
        f'Дата рождения: {birthdate}\n'
        f'Паспорт: {last.passport_series} {last.passport_number}\n'
        f'Дата выдачи: {passport_date}\n'
        f'Статус оплаты: {"Оплачен" if last.state else "Не оплачен"}\n'
        f'ID заказа: {last.id}',
        reply_markup=IKM(
            inline_keyboard=[
                [IKB(text='▶️ Вперёд', callback_data='next')],
                [
                    IKB(text='🔁 Повторить', callback_data='retry'),
                    IKB(text='🆔 Показать по ID', callback_data='show')
                ]
            ]
        )
    )
