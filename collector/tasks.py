from datetime import datetime, timedelta
from typing import Iterable, Any
import requests

from celery import shared_task, chain
from django.conf import settings
from django.db import transaction

from .models import Transaction
from .serializers import TransactionSerializer
from .utils import to_unix

from celery.utils.log import get_task_logger
from datetime import datetime

from .utils import to_unix, to_datetime, Bot


SOURCE_PATH = 'https://api.monobank.ua/'

logger = get_task_logger(__name__)

@shared_task
def handle_error(
    task_id: str, exc: Exception, traceback: str, **kwargs: Any
) -> None:
    Bot.send_message(f'{exc} occurred in {task_id=}\n{traceback}')


@shared_task(
    max_retries=1, default_retry_delay=60, autoretry_for=(ConnectionError,)
)
def get_bank_statement(from_: int, to_: int) -> list[dict]:
    logger.info(
        f'Get bank statement from {to_datetime(from_)} to {to_datetime(to_)}'
    )
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = requests.get(
        SOURCE_PATH + root, headers={'X-Token': settings.MONO_API_USER_TOKEN}
    )
    if res.status_code == 200:
        logger.info(f'Raw content: {res.content}')
        return TransactionSerializer(many=True).loads(res.content)
    raise ConnectionError(f'Bank service do not respond {res.status_code}')

@shared_task
def save_bank_transactions(
    dataset: Iterable[TransactionSerializer]
) -> dict | None:
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
        now = datetime.now()
        Bot.send_message(
            f'Collector run at {now} is successful. '
            f'{new_transactions_qty} transactions saved'
        )
        return {'last_run': to_unix(now)}
    Bot.send_message('Nothing to collect')


@shared_task
def collect_transactions() -> None:
    now = datetime.now()
    chain(
        get_bank_statement.s(
            from_=to_unix(now - timedelta(days=30)), to_=to_unix(now)
            ),
        save_bank_transactions.s()
    ).apply_async(link_error=handle_error.s())