import re

from telebot import types

import data.globals
from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_add_location_btn,
    inline_set_location_prompt_btn, inline_set_location_btn, inline_change_location_btn,
    inline_change_location_prompt_btn,
)
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Users
from states.bot_states import States
from data.config import API
import requests


@bot.message_handler(commands=["set"])
def set_city_prompt(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    query = (f"SELECT {Users.user_id}, {Users.user_city} "
             f"FROM {Users.table_name} "
             f"WHERE {Users.user_id}={user_id}")
    get_user_info = read_data(query)
    if not get_user_info or get_user_info[0][1] is None:
        markup = types.InlineKeyboardMarkup()
        cancel = inline_cancel_btn()
        set_location = inline_set_location_prompt_btn()
        set_location_keyboard = markup.add(set_location, cancel)
        msg = bot.send_message(
            chat_id,
            "You haven't set your favorite location, yet!",
            reply_markup=set_location_keyboard,
        )
        data.globals.users_dict[user_id]['message_id'] = msg.message_id
        print(data.globals.users_dict[user_id]['message_id'])
    else:
        markup = types.InlineKeyboardMarkup()
        cancel = inline_cancel_btn()
        change_location = inline_change_location_prompt_btn()
        change_location_keyboard = markup.add(change_location, cancel)
        msg = bot.send_message(chat_id,
                               f"Your favorite location name: {get_user_info[0][1]}",
                               reply_markup=change_location_keyboard)
        data.globals.users_dict[user_id]['message_id'] = msg.message_id


@bot.message_handler(state=States.search_location)
def search_location(message):
    """
    Function. Setting users favorite city.
    :return:
    """

    chat_id = message.chat.id
    user_id = message.from_user.id

    bot_answer_formatting = [
        _.lower().capitalize() for _ in re.split("\\s+|-", message.text.strip())
    ]
    city_name = "%20".join(bot_answer_formatting)

    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={API}&q={city_name}&aqi=no"
    )

    if "error" in response.json().keys() and response.json()["error"]["code"] == 1006:
        bot.send_message(chat_id, response.json()["error"]["message"])
        markup = types.InlineKeyboardMarkup()
        cancel_keyboard = markup.row(inline_cancel_btn())
        msg = bot.send_message(chat_id, "Type in city name:", reply_markup=cancel_keyboard)
    else:
        markup = types.InlineKeyboardMarkup()
        set_location_keyboard = None
        if States.search_location.operation == "Set prompt":
            set_location_keyboard = markup.row(
                inline_set_location_btn("favorite", response.json()["location"]["name"]),
                inline_cancel_btn(),
            )
        elif States.search_location.operation == "Add prompt":
            set_location_keyboard = markup.row(
                inline_add_location_btn("wishlist", response.json()["location"]["name"]),
                inline_cancel_btn())
        elif States.search_location.operation == "Change prompt":
            set_location_keyboard = markup.row(
                inline_change_location_btn("favorite", response.json()["location"]["name"]),
                inline_cancel_btn(),
            )
        msg = bot.send_message(
            chat_id,
            f"Location found: \n"
            f"{'name:':<10} {response.json()['location']['name']}\n"
            f"{'region:':<10}  {response.json()['location']['region']}\n"
            f"{'country:':<10} {response.json()['location']['country']}",
            reply_markup=set_location_keyboard,
        )
    bot.edit_message_reply_markup(
        message.chat.id,
        message_id=data.globals.users_dict[user_id]['message_id'],
        reply_markup=""
    )
    data.globals.users_dict[user_id]['message_id'] = msg.message_id
