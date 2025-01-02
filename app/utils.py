from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import time
from pathlib import Path
import json


METADATA_PATH = Path(__file__).parent.parent / '.meta/'
TIMEZONE = ZoneInfo('Europe/Kiev')


def datetime_to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def unix_to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time, tz=TIMEZONE)


def load_metadata() -> dict:
    if not METADATA_PATH.exists():
        return {}
    with open(METADATA_PATH / 'metadata.json', 'r') as f:
        return json.load(f)


def dump_metadata(data: dict) -> None:
    with open(METADATA_PATH / 'metadata.json', 'w') as f:
        json.dump(data, f, indent=4)
