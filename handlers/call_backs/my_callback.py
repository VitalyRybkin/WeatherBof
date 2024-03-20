from icecream import ic

import data
from handlers.users.my import my_prompt_msg, weather_output_hourly, weather_output_daily
from loader import bot
from midwares.api_conn_center import (
    get_current_weather,
    get_daily_forecast_weather,
    get_hourly_forecast_weather,
)
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Hourly, Daily, Current, User
from states.bot_states import States
from utils.global_functions import edit_reply_msg


@bot.callback_query_handler(
    func=lambda call: call.data
    in [f"{Hourly.table_name}_display", f"{Daily.table_name}_display"]
)
def set_weather_display(call) -> None:
    """
    Function. Setting next state.
    :param call:
    :return:
    """
    if call.data == f"{Hourly.table_name}_display":
        bot.set_state(
            call.from_user.id, States.weather_display_hourly, call.message.chat.id
        )
        States.weather_display_hourly.user_id = call.from_user.id

        data.globals.users_dict[call.from_user.id]["state"] = bot.get_state(
            call.from_user.id, call.message.chat.id
        )
        weather_output_hourly(call.message)

    if call.data == f"{Daily.table_name}_display":
        bot.set_state(
            call.from_user.id, States.weather_display_daily, call.message.chat.id
        )
        States.weather_display_daily.user_id = call.from_user.id

        data.globals.users_dict[call.from_user.id]["state"] = bot.get_state(
            call.from_user.id, call.message.chat.id
        )
        weather_output_daily(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_weather_prompt")
def hourly_weather_prompt(call) -> None:
    """
    Function. Setting previous state.
    :param call:
    :return:
    """
    bot.set_state(call.from_user.id, States.my_prompt, call.message.chat.id)
    my_prompt_msg(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == f"{Current.table_name}_display"
)
def display_current_weather(call):
    current_weather(call.from_user.id, call.message.chat.id)


def current_weather(user, chat):
    bot.delete_state(user, chat)
    current_weather_pic = get_current_weather(States.my_prompt.loc_id, user)
    edit_reply_msg(chat, user)
    with open(current_weather_pic, "rb") as p:
        bot.send_photo(chat, p)
    data.globals.users_dict[user]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: f"{Daily.table_name}|day|" in call.data)
def display_daily_weather(call):
    parsed_call_data = call.data.split("|")
    daily_weather(call.from_user.id, call.message.chat.id, parsed_call_data[2])


def daily_weather(user, chat, days):
    bot.delete_state(user, chat)
    query = User.get_user_location_info(bot_user_id=user)
    loc_id = read_data_row(query)[0]
    forecast_weather_pic = get_daily_forecast_weather(loc_id["id"], user, days)
    with open(forecast_weather_pic, "rb") as p:
        bot.send_photo(chat, p)
    data.globals.users_dict[user]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: f"{Hourly.table_name}|hour|" in call.data)
def display_hourly_weather(call):
    # query = User.get_user_location_info(bot_user_id=call.from_user.id)
    # loc_id = read_data_row(query)[0]
    # parsed_call_data = call.data.split("|")
    #
    # forecast_weather_pic_arr = get_hourly_forecast_weather(
    #     loc_id["id"], call.from_user.id, parsed_call_data[2]
    # )
    # for forecast_weather_pic in forecast_weather_pic_arr:
    #     with open(forecast_weather_pic, "rb") as p:
    #         bot.send_photo(call.message.chat.id, p)
    # data.globals.users_dict[call.from_user.id]["message_id"] = 0
    parsed_call_data = call.data.split("|")
    hourly_weather(call.from_user.id, call.message.chat.id, parsed_call_data[2])


def hourly_weather(user, chat, hours):
    bot.delete_state(user, chat)
    query = User.get_user_location_info(bot_user_id=user)
    loc_id = read_data_row(query)[0]

    forecast_weather_pic_arr = get_hourly_forecast_weather(loc_id["id"], user, hours)
    for forecast_weather_pic in forecast_weather_pic_arr:
        with open(forecast_weather_pic, "rb") as p:
            bot.send_photo(chat, p)
    data.globals.users_dict[user]["message_id"] = 0
