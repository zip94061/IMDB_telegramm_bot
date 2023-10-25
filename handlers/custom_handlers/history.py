from telebot.types import Message

from loader import bot
from utils.loguru import logger
from database.database_conf import History


@bot.message_handler(state='*', commands=['history'])
def get_history(message: Message) -> None:
    logger.log('INFO', str(f'{message.from_user.id} : /history'))
    bot.send_message(message.from_user.id, 'Выгружаю последние 10 запросов...')
    history_alias = History.alias()
    query = (History
             .select(History.requests)
             .where(History.id << (
                    history_alias
                    .select(history_alias.id)
                    .where(history_alias.user_id == message.chat.id)
                    .order_by(history_alias.date.desc())
                    .limit(10))))

    for row in query:
        data = eval(row.requests)
        msg = f"{data['command']}"
        endpoint = data.get('endpoint')
        search_filter = data.get('search_filter')
        number_of_units = data.get('number_of_units')
        if endpoint:
            msg += f', категория: {endpoint}'
        if search_filter:
            msg += f', фильтр: {search_filter}'
        if number_of_units:
            msg += f', количество: {number_of_units}'
        bot.send_message(message.chat.id, msg)
