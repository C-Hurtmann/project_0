from celery import Celery, chain
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta, timezone
from typing import Any

from .tasks import get_bank_statement, save_transactions
from .utils import to_unix, to_datetime, load_metadata, Bot


logger = get_task_logger('celery.signal')


@worker_ready.connect
def run_collector(sender: Celery, **kwargs: Any):
    now = datetime.now(tz=timezone.utc)
    from_ = now - timedelta(days=30)
    collect_transactions_chain = chain(
        get_bank_statement.s(from_=to_unix(from_), to_=to_unix(now)),
        save_transactions.s()
    )
    last_run = load_metadata().get('last_run')
    if last_run and (
        time_before_run := (now - to_datetime(last_run))
    ) < timedelta(days=1):
        logger.info(f'Time to collect {time_before_run}')
        collect_transactions_chain.apply_async(
            countdown=time_before_run.total_seconds()
        )
        task_state = (
            f'scheduled to {now + timedelta(days=1) - time_before_run}'
        )
    else:
        collect_transactions_chain.delay()
        task_state = 'started'
    status_message = f'Collect {task_state}'
    Bot.send_message(message=status_message)
    logger.info(status_message)
