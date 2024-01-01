from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_add_location_prompt_btn
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Favorites


@bot.message_handler(commands=["wishlist"])
def wishlist_command(message):
    query = (f'SELECT {Favorites.user_favorite_city_name} '
             f'FROM {Favorites.table_name} '
             f'WHERE {Favorites.favorites_user_id}={message.from_user.id}')
    get_wishlist = read_data(query)

    markup = types.InlineKeyboardMarkup()
    add_location = inline_add_location_prompt_btn()
    cancel = inline_cancel_btn()
    add_city_menu = markup.row(add_location, cancel)
    if not get_wishlist:
        msg = bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)
        data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id
    else:
        # TODO if wishlist is not empty
        pass
