from datetime import datetime
import time


def datetime_to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def unix_to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time)
