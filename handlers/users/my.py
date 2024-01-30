from telebot import types
from telebot.types import Message

import data.globals
from keyboards.inline.inline_buttons import (
    inline_daily_weather_btn,
    inline_cancel_btn,
    inline_current_weather_btn,
    inline_hourly_weather_btn,
)
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User, Daily, Hourly
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["my"])
def my(message) -> None:
    """
    Function. Executes 'my' command. Display weather user's favorite location.
    :param message:
    :return:
    """
    chat_id: int = message.chat.id

    # if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0 and
    #         not bot.get_state(message.from_user.id, message.chat.id) == States.my_prompt):
    #     bot.edit_message_reply_markup(message.chat.id,
    #                                   data.globals.users_dict[message.from_user.id]['message_id'],
    #                                   reply_markup="")

    # query: str = (
    #     f"SELECT {User.name} "
    #     f"FROM {User.table_name} "
    #     f"WHERE {User.bot_user_id}={message.from_user.id}"
    # )

    get_users_location = read_data_row(
        User.get_user_location_info(bot_user_id=message.from_user.id)
    )

    if get_users_location[0]["name"] is None:
        bot.send_message(chat_id, "You haven't /set your favorite location yet!")
    else:
        States.my_prompt.user_id = message.from_user.id
        States.my_prompt.loc_name = get_users_location[0]["name"]
        States.my_prompt.loc_id = get_users_location[0]["id"]
        my_prompt_msg(message)


@bot.message_handler(state=States.my_prompt)
def my_prompt_msg(message) -> None:
    """
    Function. Display weather of chosen location prompt with inline keyboard menu.
    :param message:
    :return:
    """
    user_id: int = States.my_prompt.user_id
    chat_id: int = message.chat.id

    bot.set_state(message.from_user.id, States.my_prompt, message.chat.id)

    markup = types.InlineKeyboardMarkup()
    markup.add(inline_current_weather_btn())
    markup.add(inline_hourly_weather_btn())
    markup.add(inline_daily_weather_btn())
    markup.add(inline_cancel_btn())
    delete_msg(chat_id, user_id)
    msg: Message = bot.send_message(
        message.chat.id,
        f"Display weather at - <b>{States.my_prompt.loc_name}</b>",
        reply_markup=markup,
        parse_mode="HTML",
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


@bot.message_handler(state=States.weather_display_hourly)
def weather_output_hourly(message) -> None:
    """
    Function. Display hour forecast with 1 to 12 hour inline button keyboard.
    :param message:
    :return:
    """
    chat_id: int = message.chat.id
    user_id: int = States.weather_display_hourly.user_id

    weather_keyboard = types.InlineKeyboardMarkup()

    for hour in range(1, 13, 2):
        weather_keyboard.add(
            types.InlineKeyboardButton(
                f"{hour}-hour", callback_data=f"{Hourly.table_name}|hour|{hour}"
            ),
            types.InlineKeyboardButton(
                f"{hour + 1}-hour", callback_data=f"{Hourly.table_name}|hour|{hour + 1}"
            ),
        )

    weather_keyboard.add(
        types.InlineKeyboardButton(
            "\U00002B05 Back", callback_data="back_to_weather_prompt"
        )
    )

    delete_msg(chat_id, user_id)
    msg: Message = bot.send_message(
        chat_id,
        f"Tap to show weather at - <b>{States.my_prompt.loc_name}</b>",
        reply_markup=weather_keyboard,
        parse_mode="HTML",
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


@bot.message_handler(state=States.weather_display_daily)
def weather_output_daily(message) -> None:
    """
    Function. Display day forecast with 1 to 3 day inline button keyboard.
    :param message:
    :return:
    """
    chat_id: int = message.chat.id
    user_id: int = States.weather_display_daily.user_id

    weather_keyboard = types.InlineKeyboardMarkup()

    for day in range(1, 4):
        weather_keyboard.add(
            types.InlineKeyboardButton(
                f"{day}-day", callback_data=f"{Daily.table_name}|day|{day}"
            )
        )

    weather_keyboard.add(
        types.InlineKeyboardButton(
            "\U00002B05 Back", callback_data="back_to_weather_prompt"
        )
    )

    delete_msg(chat_id, user_id)
    msg: Message = bot.send_message(
        chat_id, "Tap to show weather:", reply_markup=weather_keyboard
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id
