from data.config import admins
import logging
from loader import bot


def admin_notify():
    for admin in admins:
        try:
            bot.send_message(admin, text="Bot has started!")
        except Exception as e:
            logging.exception(e)
