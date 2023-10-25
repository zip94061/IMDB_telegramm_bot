from telebot.handler_backends import State, StatesGroup

# Базовые состояния пользователя


class CoreStates(StatesGroup):
    endpoint = State()
    number_of_units = State()
    custom = State()
    search_filter = State()
