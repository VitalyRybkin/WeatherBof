from telebot import types
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from midwares.db_conn_center import read_data, read_data_row
from midwares.sql_lib import Wishlist, User


def reply_bottom_menu_kb(user_id) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
    markup: ReplyKeyboardMarkup | ReplyKeyboardRemove = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    query: str = (
        f"SELECT {User.name}, {User.reply_menu} "
        f"FROM {User.table_name} "
        f"WHERE {User.bot_user_id}={user_id}"
    )
    get_user_reply_menu_setting: list = read_data_row(query)

    if get_user_reply_menu_setting[0]["reply_menu"]:
        if get_user_reply_menu_setting[0]["name"] is not None:
            markup.add(
                types.KeyboardButton(f"/my - {get_user_reply_menu_setting[0]['name']}")
            )
            markup.add(
                types.KeyboardButton(
                    f"/onetouch - {get_user_reply_menu_setting[0]['name']}"
                )
            )
        query: str = (
            f"SELECT {Wishlist.name} "
            f"FROM {Wishlist.table_name} "
            f"WHERE {Wishlist.wishlist_user_id}="
            f"({User.get_user_id(user_id)})"
        )
        get_user_wishlist: list = read_data(query)

        if get_user_wishlist:
            markup.add(types.KeyboardButton("/wishlist"))
    else:
        markup = types.ReplyKeyboardRemove()

    return markup
