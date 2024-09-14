# CastorAgenda\CastorAgenda\engine\database_fetchall.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

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

    def execute_query_ddl(self, query: str):
        session: Session = self.SessionLocal()
        try:
            session.execute(text(query))
            session.commit()
        finally:
            session.close()

    def execute_query_df(self, query: str):
        import pandas as pd
        session: Session = self.SessionLocal()
        try:
            result = session.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        finally:
            session.close()
