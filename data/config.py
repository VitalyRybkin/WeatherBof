import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

DB = str(os.getenv('DB_FILE'))

API = str(os.getenv('API_TOKEN'))

admins = [
        66283995
]
