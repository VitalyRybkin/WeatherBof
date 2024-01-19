from telebot import types

import data.globals
from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_add_location_prompt_btn,
)
from loader import bot
from midwares.db_conn_center import write_data, read_data
from midwares.sql_lib import User, Favorite
from states.bot_states import States


@bot.message_handler(commands=["add"])
@bot.message_handler(state=States.add_location)
def add_wishlist_location(message) -> None:
    """
    Function. Executes add command. Add location to wishlist prompt. Setting add_location state.
    :param message:
    :return:
    """
    # print("add : ", bot.get_state(message.from_user.id, message.chat.id))
    # if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0
    #         and not bot.get_state(message.from_user.id, message.chat.id) == States.add_location):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[message.from_user.id]['message_id'],
    #         reply_markup="")

    markup = types.InlineKeyboardMarkup()
    add_location_keyboard = markup.row(
        inline_add_location_prompt_btn(), inline_cancel_btn()
    )
    msg = bot.send_message(
        message.chat.id,
        "Add location to your wishlist?",
        reply_markup=add_location_keyboard,
    )
    data.globals.users_dict[message.from_user.id]["message_id"] = msg.message_id

    bot.set_state(message.from_user.id, States.add_location, message.chat.id)
    print("add : ", bot.get_state(message.from_user.id, message.chat.id))


#
# @bot.callback_query_handler(func=lambda call: "Add|" in call.data)
# def callback_query(call) -> None:
#     """
#     Function. Adding location to a wishlist or set as favorite.
#     :param call:
#     :return:
#     """
#     parse_call_data = call.data.split("|")
#
#     if parse_call_data[1] == "favorite":
#         bot.send_message(call.message.chat.id, "\U00002705 Favorite location set!")
#         query = (
#             f"UPDATE {User.table_name} "
#             f"SET {User.user_city}='{parse_call_data[2]}' "
#             f"WHERE {User.bot_user}={call.from_user.id}"
#         )
#         write_data(query)
#         data.globals.users_dict[call.from_user.id]['city'] = parse_call_data[2]
#     elif parse_call_data[1] == "wishlist":
#         query = (
#             f"SELECT {Favorite.user_favorite_city_name} "
#             f"FROM {Favorite.table_name} "
#             f"WHERE {Favorite.favorite_user_id}="
#             # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
#             f"({User.get_user_id(call.from_user.id)}) "
#             f"AND {Favorite.user_favorite_city_name}='{parse_call_data[2]}'"
#         )
#         get_wishlist_info = read_data(query)
#
#         if not get_wishlist_info:
#             bot.send_message(
#                 call.message.chat.id, "\U00002705 Location added to wishlist!"
#             )
#             # bot.answer_callback_query(call.id, show_alert=True, text="Location added to wishlist!")
#             query = (
#                 f"INSERT INTO {Favorite.table_name} "
#                 f"({Favorite.favorite_user_id}, {Favorite.user_favorite_city_name}) "
#                 f"VALUES (({User.get_user_id(call.from_user.id)}), '{parse_call_data[2]}')"
#             )
#             write_data(query)
#
#             query = (
#                 f"SELECT {User.user_city} "
#                 f"FROM {User.table_name} "
#                 f"WHERE {User.user_id}={call.from_user.id} "
#                 f"AND {User.user_city}='{parse_call_data[2]}'"
#             )
#             get_favorite_location = read_data(query)
#             if get_favorite_location:
#                 bot.send_message(
#                     call.message.chat.id,
#                     "\U00002705 This location used to be set as favorite too!",
#                 )
#         else:
#             bot.send_message(
#                 call.message.chat.id, "\U00002757 Location is in your wishlist!"
#             )
#             markup = types.InlineKeyboardMarkup()
#             cancel_keyboard = markup.row(inline_cancel_btn())
#             msg = bot.send_message(
#                 call.message.chat.id,
#                 "\U00002328 Type in location name:",
#                 reply_markup=cancel_keyboard,
#             )
#             bot.edit_message_reply_markup(
#                 call.message.chat.id,
#                 message_id=data.globals.users_dict[call.from_user.id]["message_id"],
#                 reply_markup="",
#             )
#             data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id
#             return
#
#     bot.delete_state(call.from_user.id, call.message.chat.id)
#
#     bot.edit_message_reply_markup(
#         call.message.chat.id,
#         message_id=data.globals.users_dict[call.from_user.id]["message_id"],
#         reply_markup="",
#     )
#     data.globals.users_dict[call.from_user.id]["message_id"] = 0
