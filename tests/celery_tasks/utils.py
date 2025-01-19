import uuid
import string

from datetime import datetime, timedelta
from dataclasses import dataclass, field
from random import randint, choice, choices



def random_timestamp() -> int:
    return int((datetime.now() - timedelta(days=randint(1, 30))).timestamp())


@dataclass
class BankTransaction:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:18])
    time: int = field(default_factory=random_timestamp)
    description: str = field(
        default_factory=lambda: f'MS K {randint(100, 999)}'
    )
    mcc: int = field(default_factory=lambda: choice([5912, 5411, 5999]))
    originalMcc: int = field(
        default_factory=lambda: choice([5912, 5411, 5999])
    )
    amount: int = field(
        default_factory=lambda: randint(-1000, 1000)
    )
    operationAmount: int = field(default_factory=lambda: randint(-1000, 1000))
    currencyCode: int = field(default_factory=lambda: choice([980, 840, 978]))
    commissionRate: int = field(default_factory=lambda: randint(0, 100))
    cashbackAmount: int = field(default_factory=lambda: randint(0, 500))
    balance: int = field(default_factory=lambda: randint(1000, 2000000))
    hold: bool = field(default_factory=lambda: True)
    receiptId: str = field(
        default_factory=lambda: (
            f'{randint(1000, 9999)}-{choices(string.ascii_uppercase, k=4)}-'
            f'{randint(1000, 9999)}-{choices(string.ascii_uppercase, k=4)}'
        )
    )
    