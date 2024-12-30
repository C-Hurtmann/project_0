from __future__ import absolute_import

from datetime import datetime, timedelta
from celery import Celery, chain
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from typing import Any

from app.collector.tasks import get_bank_statement, save_tansactions
from app.utils import unix_to_datetime, datetime_to_unix, load_metadata


logger = get_task_logger(__name__)


@worker_ready.connect
def setup_collector(sender: Celery, **kwargs: Any):
    now = datetime.now()
    week_ago = datetime_to_unix(now - timedelta(days=7))
    save_transactions = chain(
        get_bank_statement.s(from_=week_ago, to_=datetime_to_unix(now)),
        save_tansactions.s()
    )
    last_run = load_metadata().get('last_run')
    if last_run and (
        time_before_run := (now - unix_to_datetime(last_run))
    ) < timedelta(days=1):
        save_transactions.apply_async(
            countdown=time_before_run.total_seconds()
        )
        task_state = f'screduled to {now + time_before_run}'
    else:
        save_transactions.delay()
        task_state = 'started'
    logger.info(f'Collect {task_state}')
