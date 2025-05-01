import time
import json

from datetime import datetime
from functools import lru_cache

import xml.etree.ElementTree as ET


def to_unix(datetime_: datetime) -> int:
    return int(time.mktime(datetime_.timetuple()))


def to_datetime(unix_time: int) -> datetime:
    return datetime.fromtimestamp(unix_time)


@lru_cache(maxsize=64)
def get_currency_code_by_name(currency_name: str) -> int:
    root = ET.parse('resources/currency-codes.xml').getroot()
    for ccy_ntry in root.findall('.//CcyNtry'):
        ccy = ccy_ntry.find('Ccy')
        if ccy is not None and ccy.text == currency_name:
            ccy_nbr = ccy_ntry.find('CcyNbr')
            return int(ccy_nbr.text)
    raise KeyError(f'Invalid currency name {currency_name}')


def mcc_to_category(mcc_code: int) -> str:
    with open('resources/mcc.json') as f:
        category = json.load(f)
    return category.get(str(mcc_code), 'Unknown')
