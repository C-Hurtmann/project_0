from marshmallow import Schema, fields, EXCLUDE


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
