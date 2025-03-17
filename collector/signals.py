import csv
import os

from celery.worker.consumer import Consumer
from celery.signals import worker_ready
from celery.utils.log import get_task_logger
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from typing import Any

from collector.serializers import SourceFrom, TransactionSerializer

from .tasks import collect_transactions, save_bank_transactions
from .models import StatementFile


logger = get_task_logger('collector.signals')


@worker_ready.connect
def on_worker_ready(sender: Consumer, **kwargs: Any) -> None:
    StatementFile.objects.all().delete()
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


@receiver(post_save, sender=StatementFile)
def proccess_csv_file(sender, instance, created, **kwargs) -> None:
    if created and not instance.proccessed:
        with open(instance.file.path, mode='r', newline='') as csvfile:
            reader = list(csv.DictReader(csvfile))
        dataset = TransactionSerializer(
            many=True, source_from=SourceFrom.CSV
        ).load(reader)
        save_bank_transactions.delay(dataset, True)
        instance.proccessed = True
        instance.save()


@receiver(post_delete, sender=StatementFile)
def delete_file(sender, instance, **kwargs) -> None:
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
