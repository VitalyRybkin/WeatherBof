import copy

from telebot import types

import data
from keyboards.inline.inline_buttons import inline_cancel_btn
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User
from states.bot_states import States


@bot.message_handler(commands=['userconfig'])
@bot.message_handler(state=States.user_config)
def user_config(message):
    # if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0
    #         and not bot.get_state(message.from_user.id, message.chat.id) == States.user_config):
    #     bot.edit_message_reply_markup(
    #         message.chat.id,
    #         message_id=data.globals.users_dict[message.from_user.id]['message_id'],
    #         reply_markup="")

    bot.set_state(message.from_user.id, States.user_config, message.chat.id)

    query = (f"SELECT {User.metric}, {User.reply_menu} "
             f"FROM {User.table_name} "
             f"WHERE (({User.get_user_id(message.from_user.id)}))")

    get_users_settings = read_data_row(query)
    States.user_config.settings_dict = copy.deepcopy(get_users_settings[0])
    print(States.user_config.settings_dict)
    markup = types.InlineKeyboardMarkup()

    metric = States.user_config.settings_dict['metric']
    reply_menu = f'bottom menu: {"yes" if States.user_config.settings_dict["reply_menu"] else "no"}'
    markup.row(types.InlineKeyboardButton(metric, callback_data="metric"))
    markup.row(types.InlineKeyboardButton(reply_menu, callback_data="reply_menu"))

    markup.row(inline_cancel_btn())
    msg = bot.send_message(message.chat.id, "Tap to change setting:", reply_markup=markup)

    if not data.globals.users_dict[message.from_user.id]['message_id'] == 0:
        bot.edit_message_reply_markup(
            message.chat.id,
            message_id=data.globals.users_dict[message.from_user.id]['message_id'],
            reply_markup="")

    data.globals.users_dict[message.from_user.id]['message_id'] = msg.message_id
     # TODO continue