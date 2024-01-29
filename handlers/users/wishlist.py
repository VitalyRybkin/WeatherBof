from telebot import types
from telebot.types import InlineKeyboardMarkup, Message, InlineKeyboardButton

import data.globals
from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_add_location_prompt_btn,
)
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Wishlist, User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["wishlist"])
@bot.message_handler(state=States.wishlist)
def wishlist_prompt(message) -> None:
    """
    Function. Execute wishlist command. Starting prompt.
    :param message:
    :return: None
    """
    # if (
    #     not data.globals.users_dict[message.from_user.id]["message_id"] == 0
    #     and not bot.get_state(message.from_user.id, message.chat.id) == States.wishlist
    # ):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[message.from_user.id]["message_id"],
    #         reply_markup="",
    #     )

    if not data.globals.users_dict[message.from_user.id]["message_id"] == 0:
        delete_msg(message.chat.id, message.from_user.id)

    query: str = (
        f"SELECT {Wishlist.name} "
        f"FROM {Wishlist.table_name} "
        f"WHERE {Wishlist.wishlist_user_id}="
        f"({User.get_user_id(message.from_user.id)})"
        f"ORDER BY {Wishlist.name}"
    )
    get_wishlist: list = read_data(query)

    if get_wishlist:
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        for loc in get_wishlist:
            markup.add(
                types.InlineKeyboardButton(
                    loc[0], callback_data=f"Wishlist output|{loc[0]}"
                )
            )
        markup.add(inline_cancel_btn())

        msg: Message = bot.send_message(
            message.chat.id, "Your wishlist:", reply_markup=markup
        )
        bot.set_state(message.from_user.id, States.wishlist, message.chat.id)
    else:
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        add_location: InlineKeyboardButton = inline_add_location_prompt_btn()
        cancel: InlineKeyboardButton = inline_cancel_btn()
        add_city_menu: InlineKeyboardMarkup = markup.row(add_location, cancel)
        msg: Message = bot.send_message(
            message.chat.id, "Your wishlist is empty!", reply_markup=add_city_menu
        )

    data.globals.users_dict[message.from_user.id]["message_id"] = msg.message_id
