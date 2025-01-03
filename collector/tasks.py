from datetime import datetime
from typing import Iterable
import requests

from celery import shared_task
from django.conf import settings
from django.db import transaction

from .models import Transaction
from .serializers import TransactionSerializer
from .utils import to_unix


SOURCE_PATH = 'https://api.monobank.ua/'


@shared_task(max_retries=1, default_retry_delay=60)
def get_bank_statement(from_: int, to_: int) -> list[TransactionSerializer]:
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = requests.get(
        SOURCE_PATH + root, headers={'X-Token': settings.MONO_API_USER_TOKEN}
    )
    if res.status_code == 200:
        return TransactionSerializer(data=res.json(), many=True)
    raise ConnectionError('Bank service do not respond')

@shared_task
def save_transactions(dataset: Iterable[TransactionSerializer]) -> dict | None:
    new_transactions_qty = 0
    for transaction_data in dataset:
        with transaction.atomic():
            if not Transaction.objects.filter(
                bank_id=transaction_data['bank_id']
            ).exists():
                new_transaction = Transaction(**transaction_data)
                new_transaction.save()
                new_transactions_qty += 1
    if new_transactions_qty:
        return {'last_run': to_unix(datetime.now())}
