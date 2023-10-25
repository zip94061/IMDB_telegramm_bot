from os import path

from telebot.types import Message

from loader import bot
from utils.saver import save_history
from database.database_conf import create_database
from utils.loguru import logger


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    logger.log('INFO', str(f'{message.from_user.id} : /start'))
    if path.exists(path.join('database', 'database.db')):
        bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name}!')
    else:
        create_database()
        bot.send_message(message.from_user.id, f'Добро пожаловать, {message.from_user.first_name}!')
