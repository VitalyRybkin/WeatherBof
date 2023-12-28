from telebot.handler_backends import StatesGroup, State


class States(StatesGroup):
    start = State()
    add_city = State()
    search_location = State()
    help = State()
    cancel = State()