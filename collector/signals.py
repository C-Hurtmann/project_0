from celery import Celery, chain
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta
from typing import Any

from .tasks import get_bank_statement
from .utils import to_unix, to_datetime, load_metadata


logger = get_task_logger(__name__)


@worker_ready.connect
def setup_collector(sender: Celery, **kwargs: Any):
    now = datetime.now()
    week_ago = to_unix(now - timedelta(days=7))
    save_transactions = chain(
        get_bank_statement.s(from_=week_ago, to_=to_unix(now)),
        save_transactions.s()
    )
    last_run = load_metadata().get('last_run')
    if last_run and (
        time_before_run := (now - to_datetime(last_run))
    ) < timedelta(days=1):
        save_transactions.apply_async(
            countdown=time_before_run.total_seconds()
        )
        task_state = f'scheduled to {now + time_before_run}'
    else:
        save_transactions.delay()
        task_state = 'started'
    logger.info(f'Collect {task_state}')
