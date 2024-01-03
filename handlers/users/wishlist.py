from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_add_location_prompt_btn
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Favorites
from states.bot_states import States


@bot.message_handler(commands=["wishlist"])
@bot.message_handler(state=States.wishlist)
def wishlist_command(message):
    print("wishlist : ", bot.get_state(message.from_user.id, message.chat.id))
    if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0
            and not bot.get_state(message.from_user.id, message.chat.id) == States.wishlist):
        bot.edit_message_reply_markup(
            message.chat.id,
            message_id=data.globals.users_dict[message.from_user.id]['message_id'],
            reply_markup="")

    query = (f'SELECT {Favorites.user_favorite_city_name} '
             f'FROM {Favorites.table_name} '
             f'WHERE {Favorites.favorites_user_id}={message.from_user.id} '
             f'ORDER BY {Favorites.user_favorite_city_name}')
    get_wishlist = read_data(query)

    if get_wishlist:
        markup = types.InlineKeyboardMarkup()
        for loc in get_wishlist:
            markup.add(types.InlineKeyboardButton(loc[0], callback_data="Set up output"))
        markup.add(inline_cancel_btn())
        msg = bot.send_message(message.chat.id, 'Your wishlist:', reply_markup=markup)
        bot.set_state(message.from_user.id, States.wishlist, message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        add_location = inline_add_location_prompt_btn()
        cancel = inline_cancel_btn()
        add_city_menu = markup.row(add_location, cancel)
        msg = bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)

    data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id
    print("wishlist : ", bot.get_state(message.from_user.id, message.chat.id))
