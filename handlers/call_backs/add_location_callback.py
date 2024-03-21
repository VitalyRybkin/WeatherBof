from telebot.types import Message, ReplyKeyboardMarkup

import data
from handlers.users.set_location import type_location
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import write_data, read_data
from midwares.sql_lib import User, Wishlist
from states.bot_states import States
from utils.global_functions import delete_msg, edit_reply_msg


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

    edit_reply_msg(call.message.chat.id, call.from_user.id)

    msg: Message = type_location(call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = msg.message_id


@bot.callback_query_handler(func=lambda call: "Add|" in call.data)
def add_location_to_db(call) -> None:
    """
    Function. Adding location to a wishlist or set as favorite.
    :param call:
    :return: None
    """
    parse_call_data: str = call.data.split("|")
    loc_info: str = ""

    if parse_call_data[1] == "favorite":
        bot.send_message(call.message.chat.id, "\U00002705 Favorite location set!")
        for row in States.search_location.loc_dict:
            if row["id"] == int(parse_call_data[2]):
                query: str = (
                    f"UPDATE {User.table_name} "
                    f"SET {User.id}={row['id']}, "
                    f"{User.name}='{row['name']}', "
                    f"{User.region}='{row['region']}', "
                    f"{User.country}='{row['country']}' "
                    f"WHERE {User.bot_user_id}={call.from_user.id}"
                )

                loc_info = (
                    f"<b>Location info:</b>\n"
                    f"{'name:':<10} {row['name']}\n"
                    f"{'region:':<10}  {row['region']}\n"
                    f"{'country:':<10} {row['country']}"
                )
                write_data(query)
                break

    elif parse_call_data[1] == "wishlist":
        get_wishlist_info = read_data(
            Wishlist.get_wishlist_loc(
                user_id=call.from_user.id, loc_id=int(parse_call_data[2])
            )
        )

        if not get_wishlist_info:
            bot.send_message(
                call.message.chat.id, "\U00002705 Location added to wishlist!"
            )
            for row in States.search_location.loc_dict:
                if row["id"] == int(parse_call_data[2]):
                    query = (
                        f"INSERT INTO {Wishlist.table_name} "
                        f"({Wishlist.wishlist_user_id}, "
                        f"{Wishlist.id}, "
                        f"{Wishlist.name}, "
                        f"{Wishlist.region}, "
                        f"{Wishlist.country})"
                        f"VALUES (({User.get_user_id(call.from_user.id)}), "
                        f"{row['id']}, "
                        f"'{row['name']}', "
                        f"'{row['region']}', "
                        f"'{row['country']}')"
                    )

                    write_data(query)

                    loc_info = (
                        f"<b>Location added to wishlist:</b>\n"
                        f"{'name:':<10} {row['name']}\n"
                        f"{'region:':<10}  {row['region']}\n"
                        f"{'country:':<10} {row['country']}"
                    )
                    break

            query = (
                f"SELECT {User.id} "
                f"FROM {User.table_name} "
                f"WHERE {User.bot_user_id}={call.from_user.id} "
                f"AND {User.id}='{int(parse_call_data[2])}'"
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

    bot.send_message(call.message.chat.id, loc_info, parse_mode="HTML")

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )

    delete_msg(call.message.chat.id, call.from_user.id)

    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0

    keyboards: ReplyKeyboardMarkup = reply_bottom_menu_kb(call.from_user.id)
    bot.send_message(
        call.message.chat.id,
        "You can hide bottom menu here /userconfig !",
        reply_markup=keyboards,
    )
