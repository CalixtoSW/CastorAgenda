from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd

class DatabaseFetchAll:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def execute_query(self, query: str):
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query))
            return result.fetchall()
        finally:
            session.close()

    def execute_query_fetchone(self, query: str, params=None):
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query), params or {})
            row = result.fetchone()
            if row:
                return dict(row._mapping)
            return None
        finally:
            session.close()

    def execute_query_ddl(self, query: str, params=None):
        session: Session = self.SessionLocal()
        try:
            session.execute(text(query), params or {})
            session.commit()
        finally:
            session.close()

    def execute_query_df(self, query: str):
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        finally:
            session.close()

    def execute_query_zip(self, query, params=None):
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query), params or {})
            if result.keys():  # Check if query returns results
                result_dict = [dict(zip(result.keys(), row)) for row in result.fetchall()]
                return result_dict
            return []
        finally:
            session.close()

    def execute_query_fetchone_commit(self, query: str, params=None):
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query), params or {})
            session.commit()
            row = result.fetchone()
            if row:
                return row[0]
            return None
        finally:
            session.close()

