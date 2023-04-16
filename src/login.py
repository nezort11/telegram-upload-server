import os

from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_HASH = os.getenv("APP_HASH")
PHONE = os.getenv("PHONE")
PASSWORD = os.getenv("PASSWORD")

if __name__ == "__main__":
    client = TelegramClient(StringSession(), APP_ID, APP_HASH)
    client.start(PHONE, PASSWORD)
    print(client.session.save())
