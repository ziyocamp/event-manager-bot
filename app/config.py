import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Bot
    BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "database")


settings = Settings()
