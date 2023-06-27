from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterStates(StatesGroup):
    Start = State()
    SharedName = State()
    Authorised = State()