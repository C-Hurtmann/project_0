from marshmallow import Schema, fields as f, EXCLUDE


class TransactionSerializer(Schema):

    class Meta:
        unknown = EXCLUDE

    bank_id = f.Str(data_key='id')
    unix_time = f.Int(data_key='time')
    mcc = f.Int()
    original_mcc = f.Int(data_key='originalMcc')
    amount = f.Int()
    original_amount = f.Int(data_key='operationAmount')
    currency_code = f.Int(data_key='currencyCode')
    commission_rate = f.Int(data_key='commissionRate')
    balance = f.Int(data_key='balance')
