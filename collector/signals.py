from celery import Celery
from celery.worker.consumer import Consumer
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from typing import Any

from .tasks import collect_transactions


logger = get_task_logger('collector.signals')


@worker_ready.connect
def on_worker_ready(sender: Consumer, **kwargs: Any):
    PeriodicTask.objects.all().delete()
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=1, period=IntervalSchedule.HOURS
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Collect transactions',
        task='collector.tasks.collect_transactions'
    )
    collect_transactions.delay()