import requests
from celery import shared_task


SOURCE_PATH = 'https://api.monobank.ua/'


@shared_task(max_retries=1, default_retry_delay=60)
def get_bank_statement(from_: int, to_: int) -> list[TransactionSchema]:
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = requests.get(
        SOURCE_PATH + root, headers={'X-Token': MONO_API_USER_TOKEN}
    )
    if res.status_code == 200:
        return TransactionSchema(many=True).loads(res.content)
    raise ConnectionError('Bank service do not respond')
