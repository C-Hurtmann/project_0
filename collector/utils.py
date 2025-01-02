from datetime import datetime, timezone
from django.conf import settings
from zoneinfo import ZoneInfo
import time
import json


def to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time, tz=timezone.utc)


def load_metadata() -> dict:
    if not settings.METADATA_PATH.exists():
        return {}
    with open(settings.METADATA_PATH / 'metadata.json', 'r') as f:
        return json.load(f)


def dump_metadata(data: dict) -> None:
    with open(settings.METADATA_PATH / 'metadata.json', 'w') as f:
        json.dump(data, f, indent=4)
