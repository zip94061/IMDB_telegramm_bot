from datetime import datetime

from telebot.types import Message

from database.database_conf import History


def save_history(message: Message, user_request: str) -> None:
    insert = History(user_id=message.from_user.id,
                     user_name=message.from_user.username,
                     date=datetime.now().strftime('%Y.%m.%d %H:%M:%S'),
                     requests=user_request)
    insert.save()
    return
