from aiogram import Router
from app.bot.processes.searching import StartOSINT
from aiogram import F

from os import remove as removeFile

from aiogram.types import Message, FSInputFile

router = Router(name=__name__)


@router.message(F.text == 'test')
async def test(message: Message) -> Message:
    if message.from_user.id != 1647244236:
        return
    file = await StartOSINT('test')
    await message.answer_document(FSInputFile(file))
    removeFile(file)
    return await message.answer('Тест завершён')
