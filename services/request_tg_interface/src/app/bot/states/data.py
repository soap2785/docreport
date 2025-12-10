from aiogram.fsm.state import StatesGroup, State


class Data(StatesGroup):
    """ Class for message waiting state """
    fullname = State()
    region = State()
    birthdate = State()
    passport_series = State()
    passport_number = State()
    passport_date = State()
