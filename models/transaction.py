from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bank_id = Column(String, nullable=False)
    unix_time = Column(Integer, nullable=False)
    mcc = Column(Integer, nullable=False)
    original_mcc = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    original_amount = Column(Integer, nullable=False)
    currency_code = Column(Integer, nullable=False)
    commission_rate = Column(Integer, nullable=False)
