from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
import requests
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from schemas import TransactionSchema
from models import Transaction
from app.utils import unix_to_datetime, datetime_to_unix
from app.logger import Logger
from contextlib import contextmanager


load_dotenv()

MONO_API_USER_TOKEN = os.getenv('MONO_API_USER_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
SOURCE_PATH = 'https://api.monobank.ua/'


engine = create_engine(DATABASE_URL)


@contextmanager
def session_instance(engine: Engine) -> Generator[Session, None, None]:
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    try:
        yield session
    except Exception as e:
        Logger.error(f'Session error {type(e)}: {e}')
        session.rollback()
        raise
    finally:
        session.close()


def get_bank_statement(from_: int, to_: int) -> requests.Response:
    Logger.debug('Get bank statement')
    account = 0
    root = f'personal/statement/{account}/{from_}/{to_}'
    return requests.get(
        SOURCE_PATH + root, headers={'X-Token': MONO_API_USER_TOKEN}
    )


def save_tansactions(dataset: list[TransactionSchema]) -> None:
    need_to_commit = False
    with session_instance(engine=engine) as session:
        for transaction_data in dataset:
            is_exist = bool(
                session.query(Transaction).filter_by(
                    bank_id=transaction_data.bank_id
                ).first()
            )
            if not is_exist:
                transaction = Transaction(**transaction_data.__dict__)
                session.add(transaction)
                need_to_commit = True
        if need_to_commit:
            Logger.debug(
                (
                    'Commit new transaction at '
                    + unix_to_datetime(transaction.unix_time)
                )
            )
            session.commit()
        else:
            Logger.debug('No new transactions')


def main() -> None:
    Logger.info('Starting...')
    circle = 0
    while True:
        circle += 1
        Logger.debug(f'Circle: {circle}')
        transactions = set()
        week_ago = datetime.now() - timedelta(days=7)
        res = get_bank_statement(
            from_=datetime_to_unix(week_ago),
            to_=datetime_to_unix(datetime.now())
        )
        if res.status_code != 200:
            time.sleep(60)
            Logger.debug('Bank service do not respond. Waiting 60 seconds')
            continue
        else:
            transaction_list = TransactionSchema(many=True).loads(res.content)
            transactions.update(transaction_list)
            Logger.debug('Tmp transactions count ' + str(len(transactions)))
            save_tansactions(dataset=transactions)
            time.sleep(60)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        Logger.info('Stopping...')
