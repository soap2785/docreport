import datetime
from aiosqlite import connect

from aiogram.types import Message

from mainDIR.bot.src.config import admins, bot
from mainDIR.bot.processes.classesForBot import TempStorageForAdmin


async def showAdminPanel(message: Message) -> None:
    if message.from_user.id in admins:
        async with connect('database.db') as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM orders ORDER BY id DESC")
                data = await cur.fetchone()

        TempStorageForAdmin.absID = data[0]
        if data[6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        birthdate = data[3]
        docDate = data[5]
        birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
        docDate = datetime.datetime.strptime(docDate, "%Y-%m-%d")
        birthdate = datetime.datetime.strftime(birthdate, "%d.%m.%Y")
        docDate = datetime.datetime.strftime(docDate, "%d.%m.%Y")

        messageForDelete = await bot.send_message(
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
            chat_id = message.chat.id
        )
        TempStorageForAdmin.messageForEdit = messageForDelete
        return None

    else:
        return None