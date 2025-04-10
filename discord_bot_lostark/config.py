import os
from dotenv import load_dotenv

APP_ENV = os.getenv("APP_ENV", "local")

if APP_ENV == "local":
    load_dotenv()  # 로컬일 때만 .env 파일 로딩

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "charset": "utf8mb4"
}

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
