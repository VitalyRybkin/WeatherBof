import copy

from telebot import types
from telebot.types import InlineKeyboardMarkup, Message

import data
from keyboards.inline.inline_buttons import (
    inline_save_settings_btn,
    inline_exit_btn,
    inline_cancel_btn,
)
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=["userconfig"])
@bot.message_handler(state=States.user_config_prompt)
def user_configuration_prompt(message) -> None:
    """
    Function. Execute userconfig command. Userconfig starting message.
    :param message:
    :return: None
    """
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id

    bot.set_state(message.from_user.id, States.user_config_prompt, message.chat.id)

    query: str = User.get_user_config(user_id)
    get_users_settings: list = read_data_row(query)
    States.user_config_prompt.settings_dict = copy.deepcopy(get_users_settings[0])

    settings_change_output(chat_id, message, user_id)


@bot.message_handler(state=States.config_settings)
def configuring_settings(message) -> None:
    """
    Function. User configuration display with inline keyboard menu.
    :param message:
    :return: None
    """
    user_id: int = States.config_settings.user_id
    chat_id: int = message.chat.id

    settings_change_output(chat_id, message, user_id)


def settings_change_output(chat_id, message, user_id) -> None:
    """
    Function. User config message form.
    :param chat_id:
    :param message:
    :param user_id:
    :return: None
    """
    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    metric: str = f"UNITS: {States.user_config_prompt.settings_dict['metric']}"
    reply_menu: str = f'BOTTOM MENU: {"yes" if States.user_config_prompt.settings_dict["reply_menu"] else "no"}'
    markup.add(types.InlineKeyboardButton(metric, callback_data="metric"))
    markup.add(types.InlineKeyboardButton(reply_menu, callback_data="reply_menu"))
    markup.add(inline_save_settings_btn(User.table_name))
    markup.add(inline_cancel_btn())

    delete_msg(chat_id, user_id)
    msg: Message = bot.send_message(
        message.chat.id, "Tap to change setting:", reply_markup=markup
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id
