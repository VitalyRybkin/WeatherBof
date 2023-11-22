import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

DB = str(os.getenv('DB_FILE'))

admins = [
        66283995
]
