import os

from dotenv import find_dotenv, load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

if not find_dotenv():
    exit('Переменные окружения не загружены, так как отсутствует файл .env')
else:
    load_dotenv()


    class Settings(BaseSettings):
        bot_api: SecretStr = os.getenv('BOT_TOKEN', None)
        rapid_api_key: SecretStr = os.getenv('RAPID_API_KEY', None)


    DEFAULT_COMMANDS = (
        ('start', 'Запустить бота'),
        ('high', 'Вывод максимальных показателей'),
        ('low', 'Вывод минимальных показателей'),
        ('custom', 'Вывод показателей пользовательского диапазона'),
        ('history', 'Вывод истории запросов пользователей')
    )
