from datetime import datetime
from functools import lru_cache
import time


def to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time)


@lru_cache(maxsize=64)
def get_currency_code_by_name(currency_name: str) -> int:
    for ccy_ntry in root.findall('.//CcyNtry'):
        ccy = ccy_ntry.find('Ccy')
        if ccy.text == currency_name:
            ccy_nbr = ccy_ntry.find('CcyNbr')
            return ccy_nbr.text
    raise KeyError(f'Invalid currency name {currency_name}')