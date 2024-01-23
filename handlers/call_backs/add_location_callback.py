from telebot.types import Message, ReplyKeyboardMarkup

import data
from handlers.users.set_location import type_location
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import write_data, read_data
from midwares.sql_lib import User, Favorite
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.callback_query_handler(
    func=lambda call: call.data == "Set prompt"
    or call.data == "Add prompt"
    or call.data == "Change prompt"
)
def search_location_prompt(call) -> None:
    """
    Function. Location to search prompt.
    :param call:
    :return: None
    """
    bot.set_state(call.from_user.id, States.search_location, call.message.chat.id)

    States.search_location.operation = call.data

    if not data.globals.users_dict[call.from_user.id]["message_id"] == 0:
        delete_msg(call.message.chat.id, call.from_user.id)

    msg: Message = type_location(call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id


@bot.callback_query_handler(func=lambda call: "Add|" in call.data)
def add_location_to_db(call) -> None:
    """
    Function. Adding location to a wishlist or set as favorite.
    :param call:
    :return: None
    """
    parse_call_data = call.data.split("|")

    if parse_call_data[1] == "favorite":
        bot.send_message(call.message.chat.id, "\U00002705 Favorite location set!")
        query: str = (
            f"UPDATE {User.table_name} "
            f"SET {User.user_city}='{parse_call_data[2]}' "
            f"WHERE {User.bot_user}={call.from_user.id}"
        )
        write_data(query)

    elif parse_call_data[1] == "wishlist":
        query = (
            f"SELECT {Favorite.user_favorite_city_name} "
            f"FROM {Favorite.table_name} "
            f"WHERE {Favorite.favorite_user_id}="
            f"({User.get_user_id(call.from_user.id)}) "
            f"AND {Favorite.user_favorite_city_name}='{parse_call_data[2]}'"
        )
        get_wishlist_info = read_data(query)

        if not get_wishlist_info:
            bot.send_message(
                call.message.chat.id, "\U00002705 Location added to wishlist!"
            )

            query = (
                f"INSERT INTO {Favorite.table_name} "
                f"({Favorite.favorite_user_id}, {Favorite.user_favorite_city_name}) "
                f"VALUES (({User.get_user_id(call.from_user.id)}), '{parse_call_data[2]}')"
            )
            write_data(query)

            query = (
                f"SELECT {User.user_city} "
                f"FROM {User.table_name} "
                f"WHERE {User.bot_user}={call.from_user.id} "
                f"AND {User.user_city}='{parse_call_data[2]}'"
            )
            get_favorite_location = read_data(query)

            if get_favorite_location:
                bot.send_message(
                    call.message.chat.id,
                    "\U00002705 This location has been set as favorite also!",
                )
        else:
            bot.send_message(
                call.message.chat.id, "\U00002757 Location is in your wishlist!"
            )
            msg: Message = type_location(call.message.chat.id)
            data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id
            return

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    # bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0

    keyboards: ReplyKeyboardMarkup = reply_bottom_menu_kb(call.from_user.id)
    bot.send_message(
        call.message.chat.id,
        "You can hide bottom menu here /userconfig !",
        reply_markup=keyboards,
    )
