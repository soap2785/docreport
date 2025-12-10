from aiogram.fsm.state import StatesGroup, State


class OrderStorage(StatesGroup):
    """ Class for order viewing state """
    order_id = State()
