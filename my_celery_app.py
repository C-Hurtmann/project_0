from datetime import datetime, timedelta
import os
from celery import Celery
from celery.signals import worker_ready
from dotenv import load_dotenv
from requests import get

from app.schemas.transaction import TransactionSchema
from app.utils import datetime_to_unix


load_dotenv()

MONO_API_USER_TOKEN = os.getenv('MONO_API_USER_TOKEN')
SOURCE_PATH = 'https://api.monobank.ua/'

MONO_API_USER_TOKEN = os.getenv('MONO_API_USER_TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

app = Celery(
    'app',
    broker=f'redis://{REDIS_HOST}:{REDIS_PORT}/0',
    backend=f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
)


@app.task(max_retries=1, default_retry_delay=60)
def get_bank_statement(from_: int, to_: int) -> set[TransactionSchema]:
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = get(SOURCE_PATH + root, headers={'X-Token': MONO_API_USER_TOKEN})
    if res.status_code == 200:
        return res.content
    raise ConnectionError('Bank service do not respond')


@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    now = datetime.now()
    week_ago = datetime_to_unix(now - timedelta(days=7))
    get_bank_statement.s(
        from_=week_ago, to_=datetime_to_unix(now)
    ).delay()


if __name__ == '__main__':
    args = ['worker', '--loglevel=INFO']
    app.worker_main(argv=args)
