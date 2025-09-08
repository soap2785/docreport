import datetime
from sqlite3 import connect

from aiogram.types import Message

from mainDIR.bot.config import admins, bot
from mainDIR.processes.bot.classes import TempStorageForAdmin


async def admin(message: Message) -> None:
    if message.from_user.id in admins:
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders ORDER BY id DESC")
            data = cur.fetchall()
            TempStorageForAdmin.absID = data[0][0]
        if data[0][6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        birthdate = data[0][3]
        docDate = data[0][5]

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

        messageForDelete = await bot.send_message(
            text = 'Админка'
            '\n\n'
            f'\nФИО: {data[0][1]}'
            f'\nРегион: {data[0][2]}'
            f'\nДата рождения: {birthdate}'
            f'\nПаспорт: {data[0][4]}'
            f'\nДата выдачи: {docDate}'
            f'\nСостояние заказа: {orderState}'
            f'\nID заказа: {data[0][0]}'
            '\n/next | /retry',
            chat_id = message.chat.id
        )
        TempStorageForAdmin.messageForEdit = messageForDelete
        return None

    else:
        return None