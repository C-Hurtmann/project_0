from __future__ import absolute_import

import os
from celery.utils.log import get_task_logger
from datetime import datetime
from dotenv import load_dotenv
from typing import Iterable
from requests import get

from app.collector.celery_app import app
from app.database import session_instance
from app.models import Transaction
from app.schemas import TransactionSchema
from app.utils import datetime_to_unix


load_dotenv()
MONO_API_USER_TOKEN = os.getenv('MONO_API_USER_TOKEN')
SOURCE_PATH = 'https://api.monobank.ua/'

logger = get_task_logger(__name__)


@app.task(max_retries=1, default_retry_delay=60)
def get_bank_statement(from_: int, to_: int) -> list[TransactionSchema]:
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = get(SOURCE_PATH + root, headers={'X-Token': MONO_API_USER_TOKEN})
    if res.status_code == 200:
        return TransactionSchema(many=True).loads(res.content)
    raise ConnectionError('Bank service do not respond')


@app.task
def save_tansactions(dataset: Iterable[TransactionSchema]) -> dict | None:
    with session_instance() as session:
        for transaction_data in dataset:
            if not bool(
                session.query(Transaction).filter_by(
                    bank_id=transaction_data['bank_id']
                ).first()
            ):
                transaction = Transaction(**transaction_data)
                session.add(transaction)
        if new_transactions_qty := len(session.new):
            logger.debug(f'Added {new_transactions_qty} new transactions')
            session.commit()
            return {'last_run': datetime_to_unix(datetime.now())}
