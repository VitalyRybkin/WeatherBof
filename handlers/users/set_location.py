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
from midwares.api_conn_center import get_current_weather
from midwares.db_conn_center import read_data
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

    # if (
    #     not data.globals.users_dict[user_id]["message_id"] == 0
    #     and not bot.get_state(user_id, chat_id) == States.set_location
    # ):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[user_id]["message_id"],
    #         reply_markup="",
    #     )

    query: str = (
        f"SELECT {User.user_city} "
        f"FROM {User.table_name} "
        f"WHERE {User.bot_user}={user_id}"
    )
    get_user_info = read_data(query)

    if get_user_info[0][0] is None:
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
            f"Your favorite location is: {get_user_info[0][0]}",
            reply_markup=change_location_keyboard,
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

    if not data.globals.users_dict[user_id]["message_id"] == 0:
        delete_msg(chat_id, user_id)

    bot_answer_formatting: list = [
        _.lower().capitalize() for _ in re.split("\\s+|-", message.text.strip())
    ]
    city_name: str = "%20".join(bot_answer_formatting)

    response: Response = get_current_weather(city_name)

    if "error" in response.json().keys() and response.json()["error"]["code"] == 1006:
        bot.send_message(chat_id, response.json()["error"]["message"])
        msg = type_location(chat_id)
    else:
        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        set_location_keyboard: InlineKeyboardMarkup | None = None
        if States.search_location.operation == "Set prompt":
            set_location_keyboard = markup.row(
                inline_set_location_btn(
                    "favorite", response.json()["location"]["name"]
                ),
                inline_cancel_btn(),
            )
        elif States.search_location.operation == "Add prompt":
            set_location_keyboard = markup.row(
                inline_add_location_btn(
                    "wishlist", response.json()["location"]["name"]
                ),
                inline_cancel_btn(),
            )
        elif States.search_location.operation == "Change prompt":
            set_location_keyboard = markup.row(
                inline_change_location_btn(
                    "favorite", response.json()["location"]["name"]
                ),
                inline_cancel_btn(),
            )
        msg: Message = bot.send_message(
            chat_id,
            f"Location found: \n"
            f"{'name:':<10} {response.json()['location']['name']}\n"
            f"{'region:':<10}  {response.json()['location']['region']}\n"
            f"{'country:':<10} {response.json()['location']['country']}",
            reply_markup=set_location_keyboard,
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
