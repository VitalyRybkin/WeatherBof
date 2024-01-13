import copy

from telebot import types

import data
from keyboards.inline.inline_buttons import inline_save_settings_btn, inline_exit_btn
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=['userconfig'])
@bot.message_handler(state=States.user_config_setting)
def user_config(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0
    #         and not bot.get_state(message.from_user.id, message.chat.id) == States.user_config):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[message.from_user.id]['message_id'],
    #         reply_markup="")

    bot.set_state(message.from_user.id, States.user_config_setting, message.chat.id)
    data.globals.users_dict[user_id]['state'] = bot.get_state(user_id, chat_id)

    query = (f"SELECT {User.metric}, {User.reply_menu} "
             f"FROM {User.table_name} "
             f"WHERE (({User.get_user_id(message.from_user.id)}))")

    get_users_settings = read_data_row(query)
    States.user_config_setting.settings_dict = copy.deepcopy(get_users_settings[0])

    settings_change_output(chat_id, message, user_id)
    # TODO continue


@bot.message_handler(state=States.config_settings)
def configuring_settings(message):
    user_id = States.config_settings.user_id
    chat_id = message.chat.id

    settings_change_output(chat_id, message, user_id)


def settings_change_output(chat_id, message, user_id):
    markup = types.InlineKeyboardMarkup()
    metric = f"units: {States.user_config_setting.settings_dict['metric']}"
    reply_menu = f'bottom menu: {"yes" if States.user_config_setting.settings_dict["reply_menu"] else "no"}'
    markup.add(types.InlineKeyboardButton(metric, callback_data="metric"))
    markup.add(types.InlineKeyboardButton(reply_menu, callback_data="reply_menu"))
    delete_msg(chat_id, user_id)
    markup.add(inline_save_settings_btn(User.table_name))
    markup.add(inline_exit_btn())
    msg = bot.send_message(message.chat.id, "Tap to change setting:", reply_markup=markup)
    data.globals.users_dict[user_id]['message_id'] = msg.message_id
