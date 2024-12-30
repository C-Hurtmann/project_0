import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import URL
from contextlib import contextmanager
from typing import Generator


load_dotenv()

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
    database=DATABASE_NAME
)

ENGINE = create_engine(DATABASE_URL)


@contextmanager
def session_instance(
    engine: Engine = ENGINE
) -> Generator[Session, None, None]:
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
