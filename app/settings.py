import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.POSTGRES_USER = os.getenv("POSTGRES_USER")
            cls._instance.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
            cls._instance.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
            cls._instance.POSTGRES_PORT = os.getenv("POSTGRES_PORT")
            cls._instance.POSTGRES_DB = os.getenv("POSTGRES_DB")
        return cls._instance

    @property
    def async_database_url(self) -> str:
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_HOST}"
                f":{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")


settings = Settings()
