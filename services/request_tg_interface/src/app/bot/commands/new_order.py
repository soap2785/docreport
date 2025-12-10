from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.types import CallbackQuery

from .start import onStart


router = Router(name=__name__)


@router.callback_query(F.data == 'new_order')
async def new_order(event: CallbackQuery, state: FSMContext):
    return await onStart(event.message, state)
