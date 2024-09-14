from sqlalchemy import text
from sqlalchemy.orm import Session

class DatabaseFetchAll:
    def __init__(self, connection):
        self.connection = connection

    def execute_query(self, query: str):
        session: Session = self.connection.session_maker()
        try:
            return session.execute(text(query)).fetchall()
        finally:
            session.close()

    def execute_query_ddl(self, query: str):
        session: Session = self.connection.session_maker()
        try:
            session.execute(text(query))
            session.commit()
        finally:
            session.close()

    def execute_query_df(self, query: str):
        import pandas as pd
        session: Session = self.connection.session_maker()
        try:
            result = session.execute(text(query))
            return pd.DataFrame(result.fetchall(), columns=result.keys())
        finally:
            session.close()
