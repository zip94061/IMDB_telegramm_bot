from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.Settings().bot_api.get_secret_value(), state_storage=storage)
