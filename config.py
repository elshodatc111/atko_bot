import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
PRIVATE_CONTENT_GROUP_ID = int(os.getenv("PRIVATE_CONTENT_GROUP_ID", 0))
LOG_START = int(os.getenv("LOG_START", 0))
LOG_PHONE_1 = int(os.getenv("LOG_PHONE_1", 0))
LOG_PHONE_2 = int(os.getenv("LOG_PHONE_2", 0))
LOG_STATS = int(os.getenv("LOG_STATS", 0))