import pytest
import json

from unittest.mock import patch
from dataclasses import asdict
from datetime import datetime
from django.conf import settings
from collector.tasks import get_bank_statement
from .utils import BankTransaction, random_timestamp


@pytest.mark.celery
@patch('collector.tasks.requests.get')
def test_get_bank_statement_success(mock_get) -> None:
    transaction = BankTransaction()
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = json.dumps([asdict(transaction)])
    from_ = random_timestamp()
    to_ = datetime.now().timestamp()

    result = get_bank_statement(from_, to_)
    assert result == [
        {
            'bank_id': transaction.id,
            'unix_time': transaction.time,
            'mcc': transaction.mcc,
            'original_mcc': transaction.originalMcc,
            'amount': transaction.amount,
            'original_amount': transaction.operationAmount,
            'currency_code': transaction.currencyCode,
            'commission_rate': transaction.commissionRate,
            'balance': transaction.balance
        }
    ]


@pytest.mark.celery
@patch('collector.tasks.requests.get')
def test_get_bank_statement_connection_error(mock_get) -> None:
    transaction = BankTransaction()
    mock_get.return_value.status_code = 404
    mock_get.return_value.content = json.dumps([asdict(transaction)])
    from_ = random_timestamp()
    to_ = datetime.now().timestamp()

    with pytest.raises(ConnectionError):
        result = get_bank_statement(from_, to_)