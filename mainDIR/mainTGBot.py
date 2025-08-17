import asyncio

from config import bot, dp
from endpointsForBot import mainRouter


async def main():
    dp.include_router(mainRouter)


    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
