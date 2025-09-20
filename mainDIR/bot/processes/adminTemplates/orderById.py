import datetime
from aiosqlite import connect

from aiogram.types import Message

from mainDIR.bot.src.config import bot
from mainDIR.bot.processes.classesForBot import TempStorageForAdmin


async def showOrderByID(userMessage: Message) -> None:
    message = TempStorageForAdmin.messageForEdit
    ID = userMessage.text.split()[1]

    async with connect('database.db') as conn:
        async with conn.cursor() as cur:
            await cur.execute('SELECT * FROM orders WHERE id = ? ORDER BY id DESC', (int(ID),))
            data = await cur.fetchone()

    if data[6] is None or False:
        orderState = 'Оплата ожидается'
    else:
        orderState = 'Оплачено'
    await bot.delete_message(userMessage.chat.id, userMessage.message_id)

    # keyboardWithBackButton = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])

    birthdate = data[3]
    docDate = data[5]

    birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
    docDate = datetime.datetime.strptime(docDate, "%Y-%m-%d")
    birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
    docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")

    messageForDelete = await bot.edit_message_text(
        text = 'Админка'
             '\n\n'
             f'\nФИО: {data[1]}'
             f'\nРегион: {data[2]}'
             f'\nДата рождения: {data[3]}'
             f'\nПаспорт: {data[4]}'
             f'\nДата выдачи: {data[5]}'
             f'\nСостояние заказа: {orderState}'
             f'\nID заказа: {data[0]}'
             '\n/next | /retry | /back',
        # reply_markup = keyboardWithBackButton,
        message_id = message.message_id,
        chat_id = message.chat.id
    )
    TempStorageForAdmin.messageForEdit = messageForDelete
    return None