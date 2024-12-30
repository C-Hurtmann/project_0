from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
from requests import get, ConnectionError

from schemas import TransactionSchema
from models import Transaction
from utils import datetime_to_unix
from database import session_instance


load_dotenv()

MONO_API_USER_TOKEN = os.getenv('MONO_API_USER_TOKEN')


SOURCE_PATH = 'https://api.monobank.ua/'


def get_bank_statement(from_: int, to_: int) -> set[TransactionSchema]:
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    res = get(SOURCE_PATH + root, headers={'X-Token': MONO_API_USER_TOKEN})
    if res.status_code == 200:
        return TransactionSchema(many=True).loads(res.content)
    raise ConnectionError('Bank service do not respond')


def save_tansactions(dataset: set[TransactionSchema]) -> None:
    with session_instance() as session:
        for transaction_data in dataset:
            is_exist = bool(
                session.query(Transaction).filter_by(
                    bank_id=transaction_data.bank_id
                ).first()
            )
            if not is_exist:
                transaction = Transaction(**transaction_data.__dict__)
                session.add(transaction)
        if session.new:
            session.commit()
        else:


def main() -> None:
    circle = 0
    while True:
        circle += 1
        transactions = set()
        week_ago = datetime.now() - timedelta(days=30)
        try:
            transaction_list = get_bank_statement(
                from_=datetime_to_unix(week_ago),
                to_=datetime_to_unix(datetime.now())
            )
        except ConnectionError:
            time.sleep(60)
            continue
        else:
            transactions.update(transaction_list)
            save_tansactions(dataset=transactions)
            time.sleep(60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
