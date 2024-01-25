from data.config import admins
import logging
from loader import bot


def admin_notify() -> None:
    """
    Function. Admin notifications - bot started.
    :return: None
    """
    for admin in admins:
        try:
            bot.send_message(admin, text="Bot has started!")
        except Exception as e:
            logging.exception(e)


def stopped() -> None:
    """
    Function. Admin notifications - bot stopped!.
    :return: None
    """
    for admin in admins:
        try:
            bot.send_message(admin, text="Bot has stopped!")
        except Exception as e:
            logging.exception(e)