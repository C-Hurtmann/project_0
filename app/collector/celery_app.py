from __future__ import absolute_import
import os

from celery import Celery
from dotenv import load_dotenv


load_dotenv()

BROKER_URL = f'redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0'


app = Celery(
    'collector',
    broker=BROKER_URL,
    backend=BROKER_URL,
    include=['app.collector.tasks', 'app.collector.signals']
)


if __name__ == '__main__':
    args = ['worker', '--loglevel=INFO']
    app.worker_main(argv=args)
