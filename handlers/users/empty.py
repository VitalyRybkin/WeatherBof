from telebot import types

import data
from keyboards.inline.inline_buttons import (
    inline_add_location_prompt_btn,
    inline_cancel_btn,
    inline_empty_wishlist_btn,
)

from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Wishlist, User
from states.bot_states import States


@bot.message_handler(commands=["empty"])
@bot.message_handler(state=States.empty_wishlist)
def empty_wishlist(message) -> None:
    """
    Function. Executes empty command. Clear wishlist prompt. Setting empty_wishlist state.
    :param message:
    :return:
    """

    # if (
    #     not data.globals.users_dict[message.from_user.id]["message_id"] == 0
    #     and not bot.get_state(message.from_user.id, message.chat.id)
    #     == States.empty_wishlist
    # ):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[message.from_user.id]["message_id"],
    #         reply_markup="",
    #     )

    query = (
        f"SELECT {Wishlist.name} "
        f"FROM {Wishlist.table_name} "
        f"WHERE {Wishlist.wishlist_user_id}="
        f"({User.get_user_id(message.from_user.id)})"
        f"ORDER BY {Wishlist.name}"
    )
    get_wishlist = read_data(query)

    if get_wishlist:
        msg_text = "Your wishlist:\n"
        for loc in get_wishlist:
            msg_text += f"         - {loc[0]}\n"

        markup = types.InlineKeyboardMarkup()
        empty_wishlist_keyboard = markup.row(
            inline_empty_wishlist_btn(), inline_cancel_btn()
        )
        msg = bot.send_message(
            message.chat.id, msg_text, reply_markup=empty_wishlist_keyboard
        )

        bot.set_state(message.from_user.id, States.empty_wishlist, message.chat.id)

    else:
        markup = types.InlineKeyboardMarkup()
        add_location = inline_add_location_prompt_btn()
        cancel = inline_cancel_btn()
        add_city_menu = markup.row(add_location, cancel)

        msg = bot.send_message(
            message.chat.id, "Your wishlist is empty now!", reply_markup=add_city_menu
        )

    data.globals.users_dict[message.from_user.id]["message_id"] = msg.message_id
