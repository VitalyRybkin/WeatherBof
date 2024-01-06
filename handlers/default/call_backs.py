from telebot import types

from keyboards.inline.inline_buttons import inline_cancel_btn, inline_set_wishlist_btn
from loader import bot
from midwares.db_conn_center import write_data, read_data
from midwares.sql_lib import Users, Favorites
from states.bot_states import States
import data.globals


@bot.callback_query_handler(func=lambda call: call.data == "Cancel")
def cancel(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.send_message(call.message.chat.id, "\U0000274C Canceled!")
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    data.globals.users_dict[call.from_user.id]['message_id'] = 0


@bot.callback_query_handler(
    func=lambda call: call.data == "Set prompt" or call.data == "Add prompt" or call.data == "Change prompt")
def prompt(call):
    bot.set_state(call.from_user.id, States.search_location, call.message.chat.id)
    States.search_location.operation = call.data
    markup = types.InlineKeyboardMarkup()
    cancel_keyboard = markup.row(inline_cancel_btn())
    msg = bot.send_message(
        call.message.chat.id, "\U0001F524 Type in location name:", reply_markup=cancel_keyboard
    )
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    data.globals.users_dict[call.from_user.id]['message_id'] = msg.message_id


@bot.callback_query_handler(func=lambda call: call.data == "Clear wishlist")
def clear_wishlist(call):
    query = (f"DELETE FROM {Favorites.table_name} "
             f"WHERE {Favorites.favorites_user_id}={call.from_user.id}")
    write_data(query)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    # bot.send_message(call.message.chat.id, "Your /wishlist is empty! /add location?")
    bot.send_message(call.message.chat.id, "\U00002705 Your wishlist is empty now! /add location?")
    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]['message_id'] = 0


@bot.callback_query_handler(func=lambda call: call.data == "Change wishlist")
def change_wishlist(call):
    for loc, isSet in States.change_wishlist.wishlist.items():
        if not isSet:
            query = (f"DELETE FROM {Favorites.table_name} "
                     f"WHERE {Favorites.user_favorite_city_name}='{loc}'")
            write_data(query)
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    bot.send_message(call.message.chat.id, "New /wishlist was set!")
    data.globals.users_dict[call.from_user.id]['message_id'] = 0


@bot.callback_query_handler(func=lambda call: "Remove" in call.data)
def remove_from_wishlist(call):
    parse_call_data = call.data.split("|")
    States.change_wishlist.wishlist[parse_call_data[1]] = False
    markup = types.InlineKeyboardMarkup()
    for loc, isSet in States.change_wishlist.wishlist.items():
        if isSet:
            markup.add(types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove|{loc}"))
    markup.row(inline_set_wishlist_btn())
    markup.row(inline_cancel_btn())

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(func=lambda call: "Add" in call.data)
def callback_query(call):
    parse_call_data = call.data.split("|")

    if parse_call_data[1] == "favorite":
        bot.send_message(call.message.chat.id, "\U00002705 Favorite location set!")
        query = (
            f"UPDATE {Users.table_name} "
            f"SET {Users.user_city}='{parse_call_data[2]}' "
            f"WHERE {Users.user_id}={call.from_user.id}"
        )
        write_data(query)
    elif parse_call_data[1] == "wishlist":
        query = (
            f"SELECT {Favorites.user_favorite_city_name} "
            f"FROM {Favorites.table_name} "
            f"WHERE {Favorites.favorites_user_id}={call.from_user.id} "
            f"AND {Favorites.user_favorite_city_name}='{parse_call_data[2]}'"
        )
        get_wishlist_info = read_data(query)

        if not get_wishlist_info:
            bot.send_message(call.message.chat.id, "\U00002705 Location added to wishlist!")
            # bot.answer_callback_query(call.id, show_alert=True, text="Location added to wishlist!")
            query = (
                f"INSERT INTO {Favorites.table_name} "
                f"({Favorites.favorites_user_id}, {Favorites.user_favorite_city_name}) "
                f"VALUES ({call.from_user.id}, '{parse_call_data[2]}')"
            )
            write_data(query)

            query = (
                f"SELECT {Users.user_city} "
                f"FROM {Users.table_name} "
                f"WHERE {Users.user_id}={call.from_user.id} "
                f"AND {Users.user_city}='{parse_call_data[2]}'"
            )
            get_favorite_location = read_data(query)
            if get_favorite_location:
                bot.send_message(call.message.chat.id, "\U00002705 This location used to be set as favorite too!!")
        else:
            bot.send_message(call.message.chat.id, "\U00002757 Location is in your wishlist!")
            markup = types.InlineKeyboardMarkup()
            cancel_keyboard = markup.row(inline_cancel_btn())
            msg = bot.send_message(
                call.message.chat.id, "\U00002328 Type in location name:", reply_markup=cancel_keyboard
            )
            bot.edit_message_reply_markup(
                call.message.chat.id,
                message_id=data.globals.users_dict[call.from_user.id]['message_id'],
                reply_markup="")
            data.globals.users_dict[call.from_user.id]['message_id'] = msg.message_id
            return

    bot.delete_state(call.from_user.id, call.message.chat.id)

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    data.globals.users_dict[call.from_user.id]['message_id'] = 0
