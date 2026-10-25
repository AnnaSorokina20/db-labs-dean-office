
import os

from typing import Any
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConn:
    engine = None
    session: Any = None

    def __init__(self):

        #PG_USER = os.environ['PG_USER']
        #PG_PASS = os.environ['PG_PASS']
        #PG_HOST = os.environ['PG_HOST']
        #PG_PORT = os.environ['PG_PORT']
        #PG_DATABASE = os.environ['PG_DATABASE']

        conn_str = "postgresql+psycopg2://testuser:password@postgres_db:5432/lab3"
        #conn_str = f'postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'

        DBConn.engine = create_engine(conn_str, echo=False)
        DBConn.session = sessionmaker(DBConn.engine)

    @staticmethod
    @contextmanager
    def get_session(**kwargs):
        """
        with DBConn.get_session() as session:
            # do stuff
        """
        session = DBConn.session(**kwargs)
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
