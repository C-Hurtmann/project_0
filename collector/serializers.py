import base64
from datetime import datetime
import os
from typing import Any
from enum import Enum
from marshmallow import Schema, fields as f, EXCLUDE, pre_load

from .utils import get_currency_code_by_name


class SourceFrom(Enum):
    JSON = {
        'id': 'bank_id',
        'time': 'unix_time',
        'operationAmount': 'operation_amount',
        'currencyCode': 'currency_code',
        'commissionRate': 'commission_rate'
    }
    CSV = {
        'Date and time': 'unix_time',
        'MCC': 'mcc',
        'Card currency amount, (UAH)': 'amount',
        'Operation amount': 'operation_amount',
        'Commission, (UAH)': 'commission_rate',
        'Operation currency': 'currency_code',
        'Balance': 'balance'
    }


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

    def __init__(
            self, source_from: SourceFrom, *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.source_from = source_from

    @pre_load
    def preproccess_source(self, data: dict, **kwargs: Any) -> dict:
        def to_cents(raw_amount: str) -> int:
            if raw_amount == '—':
                return 0
            return int(float(raw_amount) * 100)
        data = {
            self.source_from.value.get(key, key): value
            for key, value in data.items()
        }
        if self.source_from == SourceFrom.CSV:
            data['bank_id'] = base64.urlsafe_b64encode(
                os.urandom(14)
            ).decode('utf-8').rstrip('=')
            data['unix_time'] = int(
                datetime.strptime(
                    data['unix_time'], '%d.%m.%Y %H:%M:%S'
                ).timestamp()
            )
            data['mcc'] = int(data['mcc'])
            data['amount'] = to_cents(data['amount'])
            data['operation_amount'] = to_cents(data['operation_amount'])
            data['currency_code'] = get_currency_code_by_name(
                data['currency_code']
            )
            data['commission_rate'] = to_cents(data['commission_rate'])
            data['balance'] = to_cents(data['balance'])
        return data
