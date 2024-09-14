#CastorAgenda\CastorAgenda\engine\conn.py
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from config_db import DatabaseConfig

class DatabaseConnection:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine: Engine = None
        self.session_maker: sessionmaker = None

    def connect(self):
        if not self.engine:
            self.engine = create_engine(self.config.get_uri())
            self.session_maker = sessionmaker(bind=self.engine)

    def close(self):
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.session_maker = None

    def is_connected(self) -> bool:
        return self.engine is not None
