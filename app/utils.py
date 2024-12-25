from datetime import datetime
import time


def unix_time(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))
