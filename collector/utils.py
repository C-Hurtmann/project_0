from functools import wraps
from typing import Any, Callable
from datetime import datetime, timezone
from django.conf import settings
from telebot import TeleBot
import time
import json



def to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)


def load_metadata() -> dict:
    if not settings.METADATA_DIR.exists():
        return {}
    with open(settings.METADATA_DIR / 'metadata.json', 'r') as f:
        return json.load(f)


def dump_metadata(func: Callable) -> None:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any):
        data = func(*args, **kwargs)
        if isinstance(data, dict):
            settings.METADATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(settings.METADATA_DIR / 'metadata.json', 'w') as f:
                json.dump(data, f, indent=4)
        return data
    return inner
        

class Bot:
    __bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)
    
    @classmethod
    def send_message(cls, message: str) -> None:
        my_id = 345736809
        cls.__bot.send_message(my_id, message)
