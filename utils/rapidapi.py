from typing import List, Dict, Callable, Any
import requests
from requests.exceptions import RequestException
import json
from functools import wraps

from config_data import config
from utils.loguru import logger

data = []
RapidAPI_Key = config.Settings().rapid_api_key.get_secret_value()  # Уникальный ключ RapidAPI
RapidAPI_Host = 'online-movie-database.p.rapidapi.com'


def cache(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        cache_key = args
        if cache_key not in wrapper.cache:
            wrapper.cache[cache_key] = func(*args, **kwargs)
        return wrapper.cache[cache_key]
    wrapper.cache = {}
    return wrapper


@logger.catch
def _get_top_rated(endpoint) -> List:
    # формируем запрос для api
    url = f'https://online-movie-database.p.rapidapi.com/title/{endpoint}'
    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": RapidAPI_Host
    }
    response = requests.get(url, headers=headers, timeout=20)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        raise ConnectionError('Wrong response', response.status_code)


@cache
def _get_details(title) -> Dict:
    # Получаем название фильма или тв сериала
    url = 'https://online-movie-database.p.rapidapi.com/title/get-details'
    querystring = {"tconst": title}
    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": RapidAPI_Host
    }
    response = requests.get(url, headers=headers, params=querystring, timeout=20)
    return json.loads(response.text)


def get_title(endpoint: str, number_of_units: int, start: int = 0, step: int = 1, search_filter: (None, list)=None) -> List:
    # Главная функция, запрашивает у api информацию по endpoint и возвращает результат
    try:
        title_data: List = _get_top_rated(endpoint)  # запрашиваем список тайтлов
        title_list = []
        # Формируем тайтлов список нужной нам длинны.
        for index in range(start, number_of_units + 1, step):
            # Список состоит из записей типа {id:"/title/tt0108052/" chartRating:8.9}
            # Запрашиваем название тайтла. title = tt0108052
            if search_filter:
                if title_data[index]['chartRating'] != float(search_filter):
                    continue
            title_info = _get_details(title_data[index]['id'].split('/')[2])
            title = {'name': title_info['title'],
                     'rating': title_data[index]['chartRating'],
                     'url': f"https://www.imdb.com/{title_data[index]['id']}",
                     'image': title_info['image']['url'],
                     'year': title_info['year']
                     }
            title_list.append(title)
        logger.log('INFO', title_list)
        return title_list
    except ConnectionError:
        raise RequestException
