from app.bot.processes.searching import StartOSINT
from infrastructure.repositories.postgresql.request import (
    PostgreSQLRequestRepository
)
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from os import remove as removeFile
from aiogram.types import Message, PreCheckoutQuery, FSInputFile
from aiogram.types import (
    InlineKeyboardButton as IKB,
    InlineKeyboardMarkup as IKM
)


router = Router(name=__name__)


@router.pre_checkout_query()
async def preCheckoutHandler(preCheckoutQuery: PreCheckoutQuery):
    return await preCheckoutQuery.answer(True)


@router.message(F.successful_payment)
async def successfulPaymentHandler(
    message: Message, state: FSMContext, session: AsyncSession
) -> Message:
    await message.answer(
        "Платёж прошёл успешно. Можете заказать ещё отчёт",
        reply_markup=IKM(
            inline_keyboard=[
                [IKB(text='🆕 Новый запрос', callback_data='new_order')]
            ]
        )
    )
    data = await state.get_data()
    await state.clear()
    repo = PostgreSQLRequestRepository(session)
    request = await repo.get_by_id(data['order'])
    if request:
        await repo.update('state', True, data['order'])
        await repo.commit()
    file = await StartOSINT(data)
    await message.answer_document(FSInputFile(file))
    removeFile(file)
    return
