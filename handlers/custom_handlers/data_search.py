from telebot.types import Message, ReplyKeyboardRemove
from requests import RequestException

from loader import bot
from utils.saver import save_history
from keyboards.reply import keyboard
from states.core_states import CoreStates
from utils.rapidapi import get_title
from utils.loguru import logger


@bot.message_handler(state="*", commands=['low', 'high', 'custom'])
def low(message: Message) -> None:  # Выбираем тип сортировки.
    bot.set_state(message.from_user.id, CoreStates.endpoint, message.chat.id)
    bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=keyboard.gen_markup_top())
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = message.text
        logger.log('INFO', str(f'{message.from_user.id} : {data}'))


@bot.callback_query_handler(func=lambda call: True)
@bot.message_handler(state=CoreStates.endpoint)  # Выбираем какой список тайтлов
def endpoint_get(message: Message) -> None:
    endpoint = None
    if message.text == 'Топ 250 фильмов':
        endpoint = 'get-top-rated-movies'
    elif message.text == 'Топ 250 сериалов':
        endpoint = 'get-top-rated-tv-shows'
    else:
        bot.send_message(message.chat.id, 'Ошибка ввода')

    if endpoint:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['endpoint'] = endpoint
            logger.log('INFO', str(f'{message.from_user.id} : {data}'))
            if data['command'] == '/custom':
                bot.send_message(message.chat.id, 'Доступен поиск по оценке')
                bot.send_message(message.chat.id, 'Введите значение', reply_markup=ReplyKeyboardRemove())
                bot.set_state(message.from_user.id, CoreStates.custom, message.chat.id)
            else:
                bot.send_message(message.chat.id, 'Выберите размер результата',
                                 reply_markup=keyboard.gen_markup_units())
                bot.set_state(message.from_user.id, CoreStates.number_of_units, message.chat.id)


@bot.message_handler(state=CoreStates.custom)
def custom_get(message: Message) -> None:  # Устанавливаем фильтр поиска
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['search_filter'] = message.text
        logger.log('INFO', str(f'{message.from_user.id} : {data}'))
    bot.send_message(message.chat.id, 'Выберите размер результата',
                     reply_markup=keyboard.gen_markup_units())
    bot.set_state(message.from_user.id, CoreStates.number_of_units, message.chat.id)


@bot.message_handler(state=CoreStates.number_of_units)
def number_of_units_get(message: Message) -> None:  # Выбираем количество тайтлов которые нужно вывести
    number_of_units = int(message.text)
    # msg: str = ''
    count: int = 1

    bot.send_message(message.from_user.id, 'Выгружаю данные...', reply_markup=ReplyKeyboardRemove())

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['number_of_units'] = number_of_units
        logger.log('INFO', str(f'{message.from_user.id} : {data}'))
        save_history(message, user_request=data)  # Сохраняем запрос в историю
        try:
            if data['command'] == '/low':
                title_list = get_title(endpoint=data['endpoint'],
                                       number_of_units=-number_of_units - 2,
                                       start=-1,
                                       step=-1)
            elif data['command'] == '/high':
                title_list = get_title(endpoint=data['endpoint'],
                                       number_of_units=number_of_units - 1)
            elif data['command'] == '/custom':
                title_list = get_title(endpoint=data['endpoint'],
                                       number_of_units=number_of_units - 1,
                                       search_filter=data['search_filter'])
            if len(title_list) != 0:
                for title in title_list:
                    msg = '{count}.Название: {name}, рейтинг: {rating}, дата выхода: {year}\n'.format(
                        count=count, name=title['name'], rating=title['rating'], year=title['year'])
                    count += 1
                    msg += title['url']
                    bot.send_photo(message.chat.id, photo=title['image'], caption=msg)
            else:
                bot.send_message(message.chat.id, 'К сожалению, ничего не нашел')
        except RequestException:
            bot.send_message(message.from_user.id, 'Упс, что то пошло не так 🤔')
    bot.delete_message(message.chat.id, message.message_id + 1)
    bot.delete_state(message.from_user.id, message.chat.id)
