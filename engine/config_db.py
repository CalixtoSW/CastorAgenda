from dotenv import load_dotenv
import os

class DatabaseConfig:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

    def get_uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
