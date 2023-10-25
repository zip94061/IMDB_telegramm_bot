from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def gen_markup_top() -> ReplyKeyboardMarkup:
    # клавиатура выбора эндпоинта для rapidapi
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('Топ 250 фильмов')
    btn2 = KeyboardButton('Топ 250 сериалов')
    markup.row(btn1, btn2)
    return markup


def gen_markup_units() -> ReplyKeyboardMarkup:
    # Клавиатура для выбора количества выводимых элементов поиска
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton('3')
    btn2 = KeyboardButton('5')
    btn3 = KeyboardButton('10')
    markup.row(btn1, btn2, btn3)
    return markup
