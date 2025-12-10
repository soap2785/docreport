from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from .start import onStart

from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery


router = Router(name=__name__)


@router.callback_query(F.data == 'cancel')
async def cancelHandler(
    event: CallbackQuery, state: FSMContext
) -> AnswerCallbackQuery:
    await state.clear()
    await event.message.edit_text('❌ Действие отменено.')
    return await onStart(event.message, state)
