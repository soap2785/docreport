from aiogram import Router, F
from infrastructure.repositories.postgresql.request import (
    PostgreSQLRequestRepository
)

from datetime import datetime
from app.bot.states import OrderStorage
from aiogram.fsm.context import FSMContext
from config import ADMINS
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton as IKB,
    InlineKeyboardMarkup as IKM
)


router = Router(name=__name__)


@router.callback_query(F.from_user.id in ADMINS and F.data == 'next')
async def nextOrder(event: CallbackQuery, state: FSMContext) -> Message:
    order_id = (await state.get_data())['order_id']
    repo = PostgreSQLRequestRepository()
    nextOrder = await repo.get_by_id(order_id - 1)
    await state.update_data({'order_id': nextOrder.id})
    keyboard = IKM(
        inline_keyboard=[
            [
                IKB(text='◀️ Назад', callback_data='back'),
                IKB(text='▶️ Вперёд', callback_data='next')
            ], [
                IKB(text='🔁 Повторить', callback_data='retry'),
                IKB(text='🆔 Показать по ID', callback_data='show')
            ]
        ]
    )

    if not await repo.get_by_id(nextOrder.id + 1):
        del keyboard.inline_keyboard[0][0]
        if not await repo.get_by_id(nextOrder.id - 1):
            del keyboard.inline_keyboard[0][0]
    elif not await repo.get_by_id(nextOrder.id - 1):
        del keyboard.inline_keyboard[0][0]
        if not await repo.get_by_id(nextOrder.id + 1):
            del keyboard.inline_keyboard[0][0]

    passport_date = datetime.strftime(
        nextOrder.passport_date.date(), '%d.%m.%Y'
    )
    return await event.message.edit_text(
        'Админка\n\n'
        f'ФИО: {nextOrder.fullname}\n'
        f'Регион: {nextOrder.region}\n'
        f'Дата рождения: {nextOrder.birthdate}\n'
        f'Паспорт: {nextOrder.passport_series} {nextOrder.passport_number}\n'
        f'Дата выдачи: {passport_date}\n'
        f'Дата выдачи: {nextOrder.passport_date}\n'
        f'Статус оплаты: {"Оплачен" if nextOrder.state else "Не оплачен"}\n'
        f'ID заказа: {nextOrder.id}',
        reply_markup=keyboard
    )


@router.callback_query(F.from_user.id in ADMINS and F.data == 'back')
async def prevOrder(event: CallbackQuery, state: FSMContext) -> Message:
    order_id = (await state.get_data())['order_id']
    repo = PostgreSQLRequestRepository()
    prevOrder = repo.get_by_id(order_id + 1)
    await state.update_data({'order_id': prevOrder.id})
    keyboard = event.message.reply_markup

    if not await repo.get_by_id(prevOrder.id + 1):
        del keyboard.inline_keyboard[0][0]
        if not await repo.get_by_id(prevOrder.id - 1):
            del keyboard.inline_keyboard[0][0]
    elif not await repo.get_by_id(prevOrder.id - 1):
        del keyboard.inline_keyboard[0][0]
        if not await repo.get_by_id(prevOrder.id + 1):
            del keyboard.inline_keyboard[0][0]

    return await event.message.edit_text(
        'Админка\n\n'
        f'ФИО: {prevOrder.fullname}\n'
        f'Регион: {prevOrder.region}\n'
        f'Дата рождения: {prevOrder.birthdate}\n'
        f'Паспорт: {prevOrder.passport}\n'
        f'Дата выдачи: {prevOrder.passport_date}\n'
        f'Статус оплаты: {"Оплачен" if prevOrder.state else "Не оплачен"}\n'
        f'ID заказа: {prevOrder.id}',
        reply_markup=keyboard
    )


@router.callback_query(F.from_user.id in ADMINS and F.data == 'show')
async def showOrderByID(event: CallbackQuery, state: FSMContext):
    await state.set_state(OrderStorage.order_id)
    return await event.message.answer(
        'Укажите ID заказа для показа:',
        reply_markup=IKM(
            inline_keyboard=[[IKB(text='❌ Отмена', callback_data='cancel')]]
        )
    )


@router.message(F.from_user.id in ADMINS and OrderStorage.order_id)
async def showOrderByIDProcessor(
    event: CallbackQuery, state: FSMContext
) -> Message:
    order_id = (await state.get_data())['order_id']
    repo = PostgreSQLRequestRepository()
    order = repo.get_by_id(order_id + 1)
    await state.clear()
    await state.update_data({'order_id': order.id})
    keyboard = event.message.reply_markup

    if not await repo.get_by_id(order.id + 1):
        del keyboard.inline_keyboard[0][0]
        if not await repo.get_by_id(order.id - 1):
            del keyboard.inline_keyboard[0][0]
    elif not await repo.get_by_id(order.id - 1):
        del keyboard.inline_keyboard[0][1]
        if not await repo.get_by_id(order.id + 1):
            del keyboard.inline_keyboard[0][0]

    return await event.message.edit_text(
        'Админка\n\n'
        f'ФИО: {order.fullname}\n'
        f'Регион: {order.region}\n'
        f'Дата рождения: {order.birthdate}\n'
        f'Паспорт: {order.passport}\n'
        f'Дата выдачи: {order.passport_date}\n'
        f'Статус оплаты: {"Оплачен" if order.state else "Не оплачен"}\n'
        f'ID заказа: {order.id}',
        reply_markup=keyboard
    )
