from marshmallow import Schema, fields, EXCLUDE, post_load
from dataclasses import dataclass


@dataclass
class TransactionDTO:
    bank_id: str
    unix_time: int
    mcc: int
    original_mcc: int
    amount: int
    original_amount: int
    currency_code: int
    commission_rate: int
    balance: int

    def __hash__(self) -> int:
        return hash(self.bank_id)


class TransactionSchema(Schema):

    class Meta:
        unknown = EXCLUDE

    bank_id = fields.Str(data_key='id')
    unix_time = fields.Int(data_key='time')
    mcc = fields.Int()
    original_mcc = fields.Int(data_key='originalMcc')
    amount = fields.Int()
    original_amount = fields.Int(data_key='operationAmount')
    currency_code = fields.Int(data_key='currencyCode')
    commission_rate = fields.Int(data_key='commissionRate')
    balance = fields.Int(data_key='balance')

    @post_load
    def create_transaction(self, data, **kwargs) -> TransactionDTO:
        return TransactionDTO(**data)
