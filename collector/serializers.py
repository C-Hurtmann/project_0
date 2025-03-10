from typing import Any
from enum import Enum
from marshmallow import Schema, fields as f, EXCLUDE, pre_load


class KeyMap(Enum):
    JSON = {
        'id': 'bank_id',
        'time': 'unix_time',
        'operationAmount': 'operation_amount',
        'currencyCode': 'currency_code',
        'commissionRate': 'commission_rate'
    }
    CSV = {}


class TransactionSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    bank_id = f.Str()
    unix_time = f.Int()
    mcc = f.Int()
    amount = f.Int()
    operation_amount = f.Int()
    currency_code = f.Int()
    commission_rate = f.Int()
    balance = f.Int()

    def __init__(self, key_map: KeyMap, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.key_map = key_map

    @pre_load
    def preproccess_source(self, data: dict, **kwargs: Any) -> dict:
        normalized_data = {}
        for key, value in data.items():
            normalized_data[self.key_map.value.get(key, key)] = value
        return normalized_data
