from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    ref_code = State()
    name = State()
    email = State()
    again = State()