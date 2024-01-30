import copy
import re

from requests import Response
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

import data.globals
from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_add_location_btn,
    inline_set_location_prompt_btn,
    inline_set_location_btn,
    inline_change_location_btn,
    inline_change_location_prompt_btn,
)

from loader import bot
from midwares.api_conn_center import api_search_location
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["set"])
@bot.message_handler(state=States.set_location)
def set_city_prompt(message) -> None:
    """
    Function. Execute set command.
    :param message:
    :return: None
    """
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id

    get_loc_info = read_data_row(User.get_user_location_info(bot_user_id=user_id))[0]

    if get_loc_info["id"] is None:
        markup = types.InlineKeyboardMarkup()
        cancel = inline_cancel_btn()
        set_location = inline_set_location_prompt_btn()
        set_location_keyboard = markup.add(set_location, cancel)
        msg = bot.send_message(
            chat_id,
            "You haven't set your favorite location, yet!",
            reply_markup=set_location_keyboard,
        )
    else:
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        cancel: InlineKeyboardButton = inline_cancel_btn()
        change_location: InlineKeyboardButton = inline_change_location_prompt_btn()
        change_location_keyboard = markup.add(change_location, cancel)
        msg = bot.send_message(
            chat_id,
            f"Your favorite location is: <b>{get_loc_info['name']}</b>!\nChange it?",
            reply_markup=change_location_keyboard,
            parse_mode="HTML",
        )
    bot.set_state(message.from_user.id, States.set_location, message.chat.id)
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


@bot.message_handler(state=States.search_location)
def search_location(message) -> None:
    """
    Function. API search for users favorite city.
    :return: None
    """

    chat_id: int = message.chat.id
    user_id: int = message.from_user.id

    delete_msg(chat_id, user_id)
    # if not data.globals.users_dict[user_id]["message_id"] == 0:
    #     delete_msg(chat_id, user_id)
    #     data.globals.users_dict[user_id]["message_id"] = 0

    # edit_reply_msg(chat_id, user_id)

    bot_answer_formatting: list = [
        _.lower().capitalize() for _ in re.split("\\s+|-", message.text.strip())
    ]
    city_name: str = "%20".join(bot_answer_formatting)

    response: Response = api_search_location(city_name)

    if not response.json():
        bot.send_message(chat_id, "\U0001F937 Location not found!")
        msg = type_location(chat_id)
        data.globals.users_dict[user_id]["message_id"] = msg.message_id
    else:
        States.search_location.loc_dict = copy.deepcopy(response.json())
        for row in States.search_location.loc_dict:
            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            if States.search_location.operation == "Set prompt":
                markup.add(inline_set_location_btn("favorite", str(row["id"])))
            elif States.search_location.operation == "Change prompt":
                markup.add(inline_change_location_btn("favorite", str(row["id"])))
            elif States.search_location.operation == "Add prompt":
                markup.add(inline_add_location_btn("wishlist", str(row["id"])))
            msg: Message = bot.send_message(
                chat_id,
                f"Add location found: \n"
                f"{'name:':<10} {row['name']}\n"
                f"{'region:':<10}  {row['region']}\n"
                f"{'country:':<10} {row['country']}",
                reply_markup=markup,
            )
            data.globals.users_dict[user_id]["message_list"].append(msg.message_id)

        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        markup.add(inline_cancel_btn())
        msg = bot.send_message(
            chat_id,
            "Cancel or send me new location to search for!",
            reply_markup=markup,
        )

        data.globals.users_dict[user_id]["message_id"] = msg.message_id


def type_location(chat_id: int) -> Message:
    """
    Function. Type location message.
    :param chat_id:
    :return: Message
    """
    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    cancel_keyboard: InlineKeyboardMarkup = markup.row(inline_cancel_btn())
    msg: Message = bot.send_message(
        chat_id,
        "\U0001F524 Type in location name:",
        reply_markup=cancel_keyboard,
    )
    return msg
