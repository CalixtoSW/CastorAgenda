from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

class DatabaseConfig:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = quote_plus(os.getenv('DB_PASSWORD'))  # Encode password

        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        print(f"Database: {self.database}")
        print(f"User: {self.user}")
        print(f"Password: {self.password}")  # Print encoded password

    def get_uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?client_encoding=utf8"

# Exemplo de teste
if __name__ == "__main__":
    config = DatabaseConfig()
    print(config.get_uri())
