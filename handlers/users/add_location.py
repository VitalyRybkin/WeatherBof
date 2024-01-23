from telebot import types
from telebot.types import InlineKeyboardMarkup, Message

import data.globals
from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_add_location_prompt_btn,
)
from loader import bot
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["add"])
@bot.message_handler(state=States.add_location)
def add_wishlist_location(message) -> None:
    """
    Function. Executes add command. Add location to wishlist prompt. Setting add_location state.
    :param message:
    :return: None
    """
    if not data.globals.users_dict[message.from_user.id]["message_id"] == 0:
        delete_msg(message.chat.id, message.from_user.id)

    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    add_location_keyboard = markup.row(
        inline_add_location_prompt_btn(), inline_cancel_btn()
    )

    msg: Message = bot.send_message(
        message.chat.id,
        "Add location to your wishlist?",
        reply_markup=add_location_keyboard,
    )
    data.globals.users_dict[message.from_user.id]["message_id"] = msg.message_id

    bot.set_state(message.from_user.id, States.add_location, message.chat.id)
