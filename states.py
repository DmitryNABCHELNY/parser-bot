from aiogram.dispatcher.filters.state import State, StatesGroup


class New_user(StatesGroup):
    user = State()

class Settings1(StatesGroup):
    procent = State()
    money_from = State()