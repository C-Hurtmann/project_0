from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    bank_id = serializers.CharField(source='id')
    unix_time = serializers.IntegerField(source='time')
    mcc = serializers.IntegerField(source='mcc')
    original_mcc = serializers.IntegerField(source='originalMcc')
    amount = serializers.IntegerField(source='amount')
    original_amount = serializers.IntegerField(source='operationAmount')
    currency_code = serializers.IntegerField(source='currencyCode')
    commission_rate = serializers.IntegerField(source='commissionRate')
    balance = serializers.IntegerField(source='balance')

    class Meta:
        model = Transaction
        fields = [
            'bank_id',
            'unix_time',
            'mcc',
            'original_mcc',
            'amount',
            'original_amount',
            'currency_code', 
            'commission_rate',
            'balance'
        ]
