from telebot import types

from midwares.db_conn_center import read_data, read_data_row
from midwares.sql_lib import Favorite, User


def reply_bottom_menu_kb(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    query = (
        f"SELECT {User.user_city}, {User.reply_menu} "
        f"FROM {User.table_name} "
        f"WHERE {User.bot_user}={user_id}"
    )
    get_user_reply_menu_setting = read_data_row(query)

    if get_user_reply_menu_setting[0]["reply_menu"]:
        if get_user_reply_menu_setting[0]["user_city"] is not None:
            markup.add(
                types.KeyboardButton(
                    f"/my - {get_user_reply_menu_setting[0]['user_city']}"
                )
            )
            markup.add(
                types.KeyboardButton(
                    f"/onetouch - {get_user_reply_menu_setting[0]['user_city']}"
                )
            )
        query = (
            f"SELECT {Favorite.user_favorite_city_name} "
            f"FROM {Favorite.table_name} "
            f"WHERE {Favorite.favorite_user_id}="
            f"({User.get_user_id(user_id)})"
        )
        get_user_wishlist = read_data(query)

        if get_user_wishlist:
            markup.add(types.KeyboardButton("/wishlist"))
    else:
        markup = types.ReplyKeyboardRemove()

    return markup
