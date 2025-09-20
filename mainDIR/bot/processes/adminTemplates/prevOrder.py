import datetime
from aiosqlite import connect

from aiogram.types import Message

from mainDIR.bot.src.config import bot
from mainDIR.bot.processes.classesForBot import TempStorageForAdmin


async def showPrevOrder(self, userMessage: Message) -> None:
    try:
        message = TempStorageForAdmin.messageForEdit
        TempStorageForAdmin.absID += 1
        async with connect('database.db') as conn:
            async with conn.cursor() as cur:
                await cur.execute('SELECT * FROM orders WHERE id = ? ORDER BY id DESC', (TempStorageForAdmin.absID,))
                data = await cur.fetchone()

        ID = TempStorageForAdmin.absID
        if data[6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)

        # if ID >= 1:
        #     keyboard = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])
        # else:
        #     keyboard = InlineKeyboardMarkup(inline_keyboard=[[retryButton, nextButton]])


        birthdate = data[3]
        docDate = data[5]

        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        docDate = datetime.datetime.strptime(docDate, "%Y-%m-%d")
        birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
        docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")

        if ID != 0:
            messageForDelete = await bot.edit_message_text(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[1]}'
                f'\nРегион: {data[2]}'
                f'\nДата рождения: {birthdate}'
                f'\nПаспорт: {data[4]}'
                f'\nДата выдачи: {docDate}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[0]}'
                '\n/next | /retry | /back',
                # reply_markup = keyboard,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorageForAdmin.messageForEdit = messageForDelete
            return None
        else:
            messageForDelete = await bot.edit_message_text(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[1]}'
                f'\nРегион: {data[2]}'
                f'\nДата рождения: {birthdate}'
                f'\nПаспорт: {data[4]}'
                f'\nДата выдачи: {docDate}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[0]}'
                '\n/next | /retry',
                # reply_markup = keyboard,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorageForAdmin.messageForEdit = messageForDelete

    except IndexError:
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)
        await bot.send_message(text='Это крайний запрос',
                               chat_id=userMessage.chat.id)
        TempStorageForAdmin.absID = 1