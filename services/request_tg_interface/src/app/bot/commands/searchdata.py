from datetime import datetime
from aiogram import Router, F
from asyncio import sleep as asleep
from app.app import bot
from json import dumps
from .search import successfulPaymentHandler
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.methods import AnswerCallbackQuery

from infrastructure.repositories.postgresql.request import (
    PostgreSQLRequestRepository
)
from config import REGIONS, PAY_TOKEN
from app.bot.states import Data, RequesterData

router = Router(name=__name__)

MESSAGE = (
    'Добро пожаловать! Введите данные интересующего лица.\n\n'
    'ФИО: {}\n'
    'Регион: {}\n'
    'Дата рождения: {}\n'
    'Серия и номер паспорта: {} {}\n'
    'Дата выдачи паспорта: {}'
)


@router.message(F.text == 'test')
async def test_submit(
    message: Message, state: FSMContext, session: AsyncSession
) -> Message:
    data = await state.get_data()
    if not data.get('fullname') or data['fullname'] == '...':
        return await message.answer('Нет ФИО')
    await state.clear()
    del data['index_message']
    del data['message_for_delete']
    repo = PostgreSQLRequestRepository(session)
    for key in data:
        if data[key] == '...':
            data[key] = None
    order = await repo.create(RequesterData(**data))
    del data['birthdate_datetime']
    await state.update_data(data)
    await state.update_data(order=order.id)
    return await successfulPaymentHandler(message, state, session)


@router.callback_query(F.data == 'fullname')
async def fullname_callback(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.fullname)
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=await event.message.answer('Введите ФИО')
    )


@router.message(Data.fullname)
async def fullname_processor(message: Message, state: FSMContext) -> Message:
    if message.text == await state.get_value('fullname'):
        return await delayed_delete(
            message, await message.answer('Идентичные ФИО уже введены')
        )
    await state.set_state(Data.fullname)
    if len(message.text.split()) == 3:
        await state.update_data(fullname=message.text)
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return await message.delete()
    return await delayed_delete(
        message, await message.answer('Введите фамилию, имя и отчество')
    )


@router.callback_query(F.data == 'region')
async def region_callback(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.region)
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=await event.message.answer('Введите регион')
    )


@router.message(Data.region)
async def region_processor(message: Message, state: FSMContext) -> Message:
    if message.text in (await state.get_data())['index_message'].text:
        return await delayed_delete(
            message, await message.answer('Идентичный регион уже введён')
        )
    await state.set_state(Data.region)
    if message.text.lower() in REGIONS:
        await state.update_data(region=message.text)
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return await message.delete()
    return await delayed_delete(
        message, await message.answer('Неверный регион.')
    )


@router.callback_query(F.data == 'birthdate')
async def birthdate_callback(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.birthdate)
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=await event.message.answer('Введите дату рождения')
    )


@router.message(Data.birthdate)
async def birthdate_processor(message: Message, state: FSMContext) -> Message:
    await state.set_state(Data.birthdate)
    try:
        birthdate_datetime = datetime.strptime(message.text, '%d.%m.%Y')
        if (datetime.now() - birthdate_datetime).days / 365 < 14:
            return await message.answer(
                'Возраст интересующего лица должен быть не менее 14 лет. '
            )
        await state.update_data(
            birthdate_datetime=datetime.strptime(message.text, '%d.%m.%Y'),
            birthdate=message.text
        )
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return await message.delete()
    except ValueError:
        return await delayed_delete(
            message, await message.answer(
                'Введите дату рождения в данном формате: ДД.ММ.ГГГГ'
            )
        )


@router.callback_query(F.data == 'passport_date')
async def passport_date_callback(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.passport_date)
    birthdate: datetime = (await state.get_data())['birthdate_datetime']
    if birthdate == '...':
        return await delayed_delete(
            None, await event.message.answer(
                'Сначала введите дату рождения интересующего лица.'
            )
        )
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=(
            await event.message.answer('Введите дату выдачи паспорта')
        )
    )


@router.message(Data.passport_date)
async def passport_date_processor(
    message: Message, state: FSMContext
) -> Message:
    await state.set_state(Data.passport_date)
    data = await state.get_data()
    try:
        passportDatetime = datetime.strptime(message.text, '%d.%m.%Y')
        birthdate: datetime = data['birthdate_datetime']

        if (passportDatetime - birthdate).days / 365 < 14:
            return await delayed_delete(message, await message.answer(
                'Возраст интересующего лица должен быть не менее 14 лет.'
            ))
        await state.update_data(passport_date=message.text)
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return message.delete()
    except ValueError:
        return await delayed_delete(
            message, await message.answer(
                'Введите дату выдачи паспорта в данном формате: ДД.ММ.ГГГГ'
            )
        )


@router.callback_query(F.data == 'passport_series')
async def passport_series_callback(
    event: CallbackQuery, state: FSMContext
) -> Message:
    await state.set_state(Data.passport_series)
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=await event.message.answer('Введите серию паспорта')
    )


@router.message(Data.passport_series)
async def passport_series_processor(
    message: Message, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.passport_series)
    passportSeries = message.text.replace(' ', '')
    if passportSeries.isdigit() and len(passportSeries) == 4:
        passportSeries = f'{passportSeries[:2]} {passportSeries[2:4]}'
        await state.update_data(passport_series=passportSeries)
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return await message.delete()
    return await delayed_delete(
        message, await message.answer(
            'Введённае серия паспорта неверна. '
            'Введите в формате 12 34'
        )
    )


@router.callback_query(F.data == 'passport_number')
async def passport_number_callback(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.set_state(Data.passport_number)
    await event.answer()
    if await state.get_value('message_for_delete'):
        await (await state.get_value('message_for_delete')).delete()
    return await state.update_data(
        message_for_delete=await event.message.answer('Введите номер паспорта')
    )


@router.message(Data.passport_number)
async def passportProcessor(message: Message, state: FSMContext) -> Message:
    await state.set_state(Data.passport_number)
    passportNumber = message.text.replace(' ', '')
    if passportNumber.isdigit() and len(passportNumber) == 6:
        await state.update_data(passport_number=passportNumber)
        index_message: Message = await state.get_value('index_message')
        data = await state.get_data()
        await index_message.edit_text(
            MESSAGE.format(
                data['fullname'], data['region'], data['birthdate'],
                data['passport_series'], data['passport_number'],
                data['passport_date']
            ), reply_markup=index_message.reply_markup
        )
        await data['message_for_delete'].delete()
        await state.update_data(message_for_delete=None)
        return await message.delete()
    return await delayed_delete(
        message, await message.answer(
            'Введённый номер паспорта неверен. '
            'Введите в формате 567890'
        )
    )


@router.callback_query(F.data == 'submit')
async def submit_callback(
    event: CallbackQuery, state: FSMContext, session: AsyncSession
) -> Message:
    data = await state.get_data()
    if not data.get('fullname') or data['fullname'] == '...':
        return await delayed_delete(
            None, await event.message.answer('Нет ФИО')
        )
    await state.clear()
    del data['index_message']
    del data['message_for_delete']
    repo = PostgreSQLRequestRepository(session)
    for key in data:
        if data[key] == '...':
            data[key] = None
    order = await repo.create(RequesterData(**data))
    del data['birthdate_datetime']
    await state.update_data(data)
    await state.update_data(order=order.id)
    await event.answer()
    return await bot.send_invoice(
        event.from_user.id,
        'Покупка отчёта', f'Покупка отчёта по лицу {order.fullname}',
        'invoice', 'RUB', [
            LabeledPrice(label='Отчёт', amount=10000)
        ], provider_token=PAY_TOKEN, provider_data=dumps(
            {
                "receipt": {
                    'items': [
                        {
                            "description":
                                f'Покупка отчёта по лицу {order.fullname}',
                            "quantity": 1.000,
                            "amount": {"value": 100.00, "currency": "RUB"},
                            "vat_code": 1,
                            'payment_mode': 'full_payment',
                            'payment_subject': 'service'
                        }
                    ]
                }
            }
        ), need_email=True, send_email_to_provider=True
    )


async def delayed_delete(
    message_from_user: Message,
    message_from_bot: Message
) -> None:
    await asleep(4)
    if message_from_user:
        await message_from_user.delete()
    return await message_from_bot.delete()
