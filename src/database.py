from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
from settings import DATABASE_URI

engine = create_engine(DATABASE_URI)


class Base(DeclarativeBase):
    pass


def create_table():
    Base.metadata.create_all(engine)


@contextmanager
def get_db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
