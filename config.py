import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

SOURCES = [
    {"name": "motor", "url": "https://motor.ru/", "enabled": True},
    {"name": "drom", "url": "https://news.drom.ru/", "enabled": True},
    {"name": "drive", "url": "https://www.drive.ru/", "enabled": True},
    {"name": "kolesa", "url": "https://www.kolesa.ru/news/", "enabled": True},
]

POST_TIMES = ["10:00", "17:00"]  # MSK

NEWS_PER_SESSION = 1

PROXY = os.getenv("PROXY", "")

DB_PATH = "news.db"