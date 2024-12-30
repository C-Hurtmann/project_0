from datetime import datetime, timedelta
from requests import get
from app.schemas.transaction import TransactionSchema
from app.utils import datetime_to_unix
from my_celery_app import MONO_API_USER_TOKEN, SOURCE_PATH, app
from celery.signals import worker_ready


@app.task
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
    try:
        return get_bank_statement.delay(
            from_=week_ago, to_=datetime_to_unix(now)
        )
    except ConnectionError:
        return get_bank_statement.apply_async(
            kwargs={'from_': week_ago, 'to_': datetime_to_unix(now)},
            countdown=60
        )
