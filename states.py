from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    wait_for_confirmation = State()
    confirmed = State()
