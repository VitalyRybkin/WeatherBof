from telebot import types

import data
from handlers.users.my import my_prompt_msg
from keyboards.inline.inline_buttons import inline_set_wishlist_btn, inline_cancel_btn
from loader import bot
from midwares.db_conn_center import write_data
from midwares.sql_lib import Favorite, User
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: call.data == "Clear wishlist")
def clear_wishlist(call) -> None:
    """
    Function. Clearing wishlist.
    :param call:
    :return:
    """
    query = (
        f"DELETE FROM {Favorite.table_name} "
        f"WHERE {Favorite.favorite_user_id}="
        # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
        f"({User.get_user_id(call.from_user.id)})"
    )
    write_data(query)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    # bot.send_message(call.message.chat.id, "Your /wishlist is empty! /add location?")
    bot.send_message(
        call.message.chat.id, "\U00002705 Your wishlist is empty now! /add location?"
    )
    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: call.data == "Change wishlist")
def change_wishlist(call) -> None:
    """
    Function. Changing wishlist content.
    :param call:
    :return:
    """
    for loc, isSet in States.change_wishlist.wishlist.items():
        if not isSet:
            query = (
                f"DELETE FROM {Favorite.table_name} "
                f"WHERE {Favorite.user_favorite_city_name}='{loc}' "
                f"AND {Favorite.favorite_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            write_data(query)
    bot.delete_state(call.from_user.id, call.message.chat.id)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )
    bot.send_message(call.message.chat.id, "New /wishlist was set!")
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: "Remove" in call.data)
def remove_from_wishlist(call) -> None:
    """
    Function. Removing item from wishlist (created class dict) while in change_wishlist state.
    :param call:
    :return:
    """
    parse_call_data = call.data.split("|")
    States.change_wishlist.wishlist[parse_call_data[1]] = False
    markup = types.InlineKeyboardMarkup()
    for loc, isSet in States.change_wishlist.wishlist.items():
        if isSet:
            markup.add(
                types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove|{loc}")
            )
    markup.row(inline_set_wishlist_btn())
    markup.row(inline_cancel_btn())

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: "Wishlist output" in call.data)
def wishlist_loc_output(call):
    States.my_prompt.user_id = call.from_user.id
    parse_callback = call.data.split("|")
    States.my_prompt.city = parse_callback[1]
    my_prompt_msg(call.message)
