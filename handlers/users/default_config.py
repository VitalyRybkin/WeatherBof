import copy

from telebot import types

import data
from keyboards.inline.inline_buttons import inline_save_settings_btn, inline_exit_btn
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Default, Hourly, Daily, User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["default"])
@bot.message_handler(state=States.default_config_prompt)
def default_settings_prompt(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    bot.set_state(user_id, States.default_config_prompt, chat_id)

    query = Default.get_default_settings(f"({User.get_user_id(user_id)})")

    get_default_settings = read_data_row(query)
    States.default_setting.settings_dict = copy.deepcopy(get_default_settings[0])
    settings_change_output(chat_id, message, user_id)


@bot.message_handler(state=States.default_setting)
def default_config_setting(message):
    user_id = States.default_setting.user_id
    chat_id = message.chat.id

    settings_change_output(chat_id, message, user_id)


@bot.message_handler(state=States.set_duration_prompt)
def set_duration(message):
    user_id = States.default_setting.user_id
    chat_id = message.chat.id
    msg_text = ""

    if States.set_duration_prompt.duration == Daily.table_name:
        try:
            duration = int(message.text)
            if duration in range(4):
                States.default_setting.settings_dict["daily_weather"] = int(
                    message.text
                )
                bot.set_state(user_id, States.default_setting, chat_id)
                default_config_setting(message)
                return
            else:
                msg_text = "\U00002757 Days must be in range 1 to 3! (3-day forecast recommended)"
        except ValueError:
            msg_text = "Type in number of days forecast - <b>1 to 3-day forecast available</b>:"

    if States.set_duration_prompt.duration == Hourly.table_name:
        try:
            duration = int(message.text)
            if duration in range(13):
                States.default_setting.settings_dict["hourly_weather"] = int(
                    message.text
                )
                bot.set_state(user_id, States.default_setting, chat_id)
                default_config_setting(message)
                return
            else:
                msg_text = "\U00002757 Hours must be in range 1 to 12! (6-hour forecast recommended)"
        except ValueError:
            msg_text = (
                "Type in of hours forecast - <b>1 to 12-hour forecast available</b>:"
            )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("\U00002B05 Back", callback_data="back"))
    delete_msg(chat_id, user_id)
    msg = bot.send_message(
        message.chat.id, msg_text, reply_markup=markup, parse_mode="HTML"
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


def settings_change_output(chat_id, message, user_id):
    markup = types.InlineKeyboardMarkup()
    current = (
        f"\U0001F4C4 CURRENT WEATHER: "
        f'{"yes" if States.default_setting.settings_dict["current_weather"] else "no"}'
    )
    hourly = f"\U000023F3 HOURLY WEATHER: {States.default_setting.settings_dict['hourly_weather']}-hour forecast"
    daily = f"\U0001F4C6 DAILY WEATHER: {States.default_setting.settings_dict['daily_weather']}-day forecast"
    markup.add(types.InlineKeyboardButton(current, callback_data="current_weather"))
    markup.add(types.InlineKeyboardButton(hourly, callback_data=Hourly.table_name))
    markup.add(types.InlineKeyboardButton(daily, callback_data=Daily.table_name))
    delete_msg(chat_id, user_id)
    markup.add(inline_save_settings_btn(Default.table_name))
    markup.add(inline_exit_btn())
    msg = bot.send_message(
        message.chat.id, "Tap to change setting:", reply_markup=markup
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id
