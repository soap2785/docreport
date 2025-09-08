import datetime
from sqlite3 import connect

from aiogram.types import Message

from mainDIR.bot.config import bot
from mainDIR.processes.bot.classes import TempStorageForAdmin


async def nextOrder(self, userMessage: Message) -> None:
    try:
        message = TempStorageForAdmin.messageForEdit
        TempStorageForAdmin.absID -= 1
        ID = TempStorageForAdmin.absID
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM orders WHERE id = ? ORDER BY id DESC', (ID,))
            data = cur.fetchall()
        data = data[0]
        if data[6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)

        # keyboardWithBackButton = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])

        birthdate = data[3]
        docDate = data[5]

        if type(birthdate) is not datetime.datetime:
            birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d %H:%M:%S")
            birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
        else:
            birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")

        if type(docDate) is not datetime.datetime:
            docDate = datetime.datetime.strptime(docDate, "%Y-%m-%d %H:%M:%S")
            docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")
        else:
            docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")

        if ID != len(data) - 1:
            message = await bot.edit_message_text(
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
                # reply_markup = keyboardWithBackButton,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorageForAdmin.messageForEdit = message
            return None
        else:
            messageForDelete = await bot.edit_message_text(
                text='Админка'
                     '\n\n'
                     f'\nФИО: {data[1]}'
                     f'\nРегион: {data[2]}'
                     f'\nДата рождения: {birthdate}'
                     f'\nПаспорт: {data[4]}'
                     f'\nДата выдачи: {docDate}'
                     f'\nСостояние заказа: {orderState}'
                     f'\nID заказа: {data[0]}'
                     '\n/back | /retry',
                # reply_markup = keyboard,
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            TempStorageForAdmin.messageForEdit = messageForDelete
    except IndexError:
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)
        await bot.send_message(text = 'Это крайний запрос',
                         chat_id = userMessage.chat.id)
        TempStorageForAdmin.absID = 6