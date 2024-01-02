from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_add_location_prompt_btn, \
    inline_set_wishlist_btn
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Favorites
from states.bot_states import States


@bot.message_handler(commands=["change"])
def get_wishlist(message):
    query = (
        f"SELECT {Favorites.user_favorite_city_name} "
        f"FROM {Favorites.table_name} "
        f"WHERE {Favorites.favorites_user_id}={message.from_user.id} "
        f"ORDER BY {Favorites.user_favorite_city_name}"
    )
    get_wishlist_data = read_data(query)

    if get_wishlist_data:
        States.change_wishlist.wishlist = {}
        for loc in get_wishlist_data:
            States.change_wishlist.wishlist[loc[0]] = True

        bot.set_state(message.from_user.id, States.change_wishlist, message.chat.id)

        markup = types.InlineKeyboardMarkup()
        for loc, isSet in States.change_wishlist.wishlist.items():
            if isSet:
                markup.add(types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove location|{loc}"))
        markup.row(inline_set_wishlist_btn())
        markup.row(inline_cancel_btn())

        msg = bot.send_message(message.chat.id, "Tap location name to remove from wishlist:", reply_markup=markup)

    else:
        markup = types.InlineKeyboardMarkup()
        add_location = inline_add_location_prompt_btn()
        cancel = inline_cancel_btn()
        add_city_menu = markup.row(add_location, cancel)
        msg = bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)

    data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id

# @bot.message_handler(state=States.change_wishlist)
# def change_wishlist(message):
#     print('state')
#     if States.change_wishlist.wishlist:
#         markup = types.InlineKeyboardMarkup()
#         for loc, isSet in States.change_wishlist.wishlist.items():
#             if isSet:
#                 markup.add(types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove location|{loc}"))
#         markup.row(inline_set_wishlist_btn())
#         markup.row(inline_cancel_btn())
#
#         # msg = bot.send_message(call.message.chat.id, "Tap location name to remove from wishlist:", reply_markup=markup)
#
#         bot.edit_message_reply_markup(
#             message.chat.id,
#             message_id=data.globals.users_dict[message.from_user.id]['message_id'],
#             reply_markup=markup)
#     else:
#         markup = types.InlineKeyboardMarkup()
#         add_location = inline_add_location_prompt_btn()
#         cancel = inline_cancel_btn()
#         add_city_menu = markup.row(add_location, cancel)
#         msg = bot.send_message(message.chat.id, 'Your wishlist is empty!', reply_markup=add_city_menu)
#
#     data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     parse_call_data = call.data.split("|")
#     States.change_wishlist.remove_location = []
#     if parse_call_data[0] == "Remove location":
#         States.change_wishlist.remove_location.append(parse_call_data[1])
#         States.change_wishlist.wishlist.remove(parse_call_data[1])
#         msg = message_output(call.message.chat.id)
#         bot.edit_message_reply_markup(
#             call.message.chat.id,
#             message_id=data.globals.users_dict[call.from_user.id]['message_id'],
#             reply_markup="")
#         data.globals.users_dict[call.from_user.id]['message_id'] = msg.message_id


# def message_output(chat_id):
#     markup = types.InlineKeyboardMarkup()
#     for loc, isSet in States.change_wishlist.wishlist.items():
#         if isSet:
#             markup.add(types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove location|{loc}"))
#     markup.row(inline_set_wishlist_btn())
#     markup.row(inline_cancel_btn())
#     msg = bot.send_message(chat_id, "Tap location name to remove from wishlist:", reply_markup=markup)
#     return msg
