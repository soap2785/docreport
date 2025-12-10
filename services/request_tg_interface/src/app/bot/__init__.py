from asyncio import run

from app.app import dp, bot
from app.bot import commands
from databases.postgresql.session_manager import sessionmanager
from databases.postgresql.middlewares import DBSessionMiddleware


async def Start() -> None:
    dp.include_routers(*commands.__all__)
    sessionmanager.init(
        "postgresql+asyncpg://user:password@users_db:5432/users_db"
    )
    dp.message.middleware(DBSessionMiddleware())
    dp.callback_query.middleware(DBSessionMiddleware())
    await dp.start_polling(bot, skip_updates=True)
    await sessionmanager.close()


run(Start())
