from sqlite3 import connect

from aiogram.types import Message

from mainDIR.config import admins, bot


class TempStorage:
    messageForDelete: Message
    chatID: int
    absID: int


async def admin(message: Message) -> None:
    if message.from_user.id in admins:
        TempStorage.absID = 0
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM orders ORDER BY id DESC')
            data = cur.fetchall()
            ID = 0
            if data[ID][6] is None or False:
                orderState = 'Оплата ожидается'
            else:
                orderState = 'Оплачено'
            messageForDelete = await bot.send_message(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[ID][1]}'
                f'\nРегион: {data[ID][2]}'
                f'\nДата рождения: {data[ID][3]}'
                f'\nПаспорт: {data[ID][4]}'
                f'\nДата выдачи: {data[ID][5]}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[ID][0]}'
                '\n/next',
                # reply_markup = keyboard
                chat_id = message.chat.id
            )
            TempStorage.messageForDelete = messageForDelete
            return None

    else:
        return None


async def nextOrder(self, userMessage: Message) -> None:
    try:
        message = TempStorage.messageForDelete
        TempStorage.absID += 1
        ID = TempStorage.absID
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM orders ORDER BY id DESC')
            data = cur.fetchall()
        if data[ID - 1][6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)

        # keyboardWithBackButton = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])

        if ID != len(data) - 1:
            message = await bot.edit_message_text(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[ID][1]}'
                f'\nРегион: {data[ID][2]}'
                f'\nДата рождения: {data[ID][3]}'
                f'\nПаспорт: {data[ID][4]}'
                f'\nДата выдачи: {data[ID][5]}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[ID][0]}'
                '\n/next | /back',
                # reply_markup = keyboardWithBackButton,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorage.messageForDelete = message
            return None
        else:
            messageForDelete = await bot.edit_message_text(
                text='Админка'
                     '\n\n'
                     f'\nФИО: {data[ID][1]}'
                     f'\nРегион: {data[ID][2]}'
                     f'\nДата рождения: {data[ID][3]}'
                     f'\nПаспорт: {data[ID][4]}'
                     f'\nДата выдачи: {data[ID][5]}'
                     f'\nСостояние заказа: {orderState}'
                     f'\nID заказа: {data[ID][0]}'
                     '\n/back',
                # reply_markup = keyboard,
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            TempStorage.messageForDelete = messageForDelete
    except IndexError:
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)
        await bot.send_message(text = 'Это крайний запрос',
                         chat_id = userMessage.chat.id)
        TempStorage.absID = 6


async def prevOrder(self, userMessage: Message) -> None:
    try:
        message = TempStorage.messageForDelete
        TempStorage.absID -= 1
        with connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM orders ORDER BY id DESC')
            data = cur.fetchall()
        ID = TempStorage.absID
        if data[ID][6] is None or False:
            orderState = 'Оплата ожидается'
        else:
            orderState = 'Оплачено'
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)

        # if ID >= 1:
        #     keyboard = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])
        # else:
        #     keyboard = InlineKeyboardMarkup(inline_keyboard=[[retryButton, nextButton]])
        if ID != 0:
            messageForDelete = await bot.edit_message_text(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[ID][1]}'
                f'\nРегион: {data[ID][2]}'
                f'\nДата рождения: {data[ID][3]}'
                f'\nПаспорт: {data[ID][4]}'
                f'\nДата выдачи: {data[ID][5]}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[ID][0]}'
                '\n/next | /back',
                # reply_markup = keyboard,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorage.messageForDelete = messageForDelete
            return None
        else:
            messageForDelete = await bot.edit_message_text(
                text = 'Админка'
                '\n\n'
                f'\nФИО: {data[ID][1]}'
                f'\nРегион: {data[ID][2]}'
                f'\nДата рождения: {data[ID][3]}'
                f'\nПаспорт: {data[ID][4]}'
                f'\nДата выдачи: {data[ID][5]}'
                f'\nСостояние заказа: {orderState}'
                f'\nID заказа: {data[ID][0]}'
                '\n/next',
                # reply_markup = keyboard,
                chat_id = message.chat.id,
                message_id = message.message_id
            )
            TempStorage.messageForDelete = messageForDelete

    except IndexError:
        await bot.delete_message(userMessage.chat.id, userMessage.message_id)
        await bot.send_message(text='Это крайний запрос',
                               chat_id=userMessage.chat.id)
        TempStorage.absID = 1



async def showByID(userMessage: Message) -> None:
    message = TempStorage.messageForDelete
    ID = userMessage.text.split()[1]
    with connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM orders WHERE id = ? ORDER BY id DESC', (int(ID),))
        data = cur.fetchall()
    if data[0][6] is None or False:
        orderState = 'Оплата ожидается'
    else:
        orderState = 'Оплачено'
    await bot.delete_message(userMessage.chat.id, userMessage.message_id)

    # keyboardWithBackButton = InlineKeyboardMarkup(inline_keyboard=[[backButton, retryButton, nextButton]])

    data = data[0]
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
             '\n/next | /back',
        # reply_markup = keyboardWithBackButton,
        message_id = message.message_id,
        chat_id = message.chat.id
    )
    TempStorage.messageForDelete = messageForDelete
    return None
