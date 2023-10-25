from os import path

from loguru import logger


logger.add(path.join('logs', 'log.log'), format="{time} {level} {message}",
           level='DEBUG', rotation='100 MB', backtrace=True)
