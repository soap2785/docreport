import asyncio
from sqlite3 import connect

from config import bot, dp
from endpointsForBot import mainRouter


async def main():
    dp.include_router(mainRouter)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    print("Бот запускается...")
    with connect('database.db') as conn:
        conn.cursor().execute("""
        CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        region TEXT,
        birthdate DATE,
        passport TEXT,
        passportDate DATE,
        state BOOLEAN,
        curTime DATETIME,
        messageChatId INTEGER
        )
        """)
    asyncio.run(main())
