from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_daily_weather_btn, inline_cancel_btn, \
    inline_current_weather_btn, inline_hourly_weather_btn
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import User, Default
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.message_handler(commands=['my'])
@bot.message_handler(state=States.my_prompt)
def my(message) -> None:
    """
    Function. Executes 'my' command. Display weather user's favorite location.
    :param message:
    :return:
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    # if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0 and
    #         not bot.get_state(message.from_user.id, message.chat.id) == States.my_prompt):
    #     bot.edit_message_reply_markup(message.chat.id,
    #                                   data.globals.users_dict[message.from_user.id]['message_id'],
    #                                   reply_markup="")

    query = (f"SELECT {User.user_city} "
             f"FROM {User.table_name} "
             f"WHERE {User.bot_user}={message.from_user.id}")

    get_users_location = read_data_row(query)

    if get_users_location[0]['user_city'] is None:
        # TODO go to add location state
        bot.send_message(chat_id, "You haven\'t /set your favorite location yet!")
    else:
        bot.set_state(message.from_user.id, States.my_prompt, message.chat.id)
        data.globals.users_dict[user_id]['state'] = bot.get_state(user_id, chat_id)

        get_default_setting = read_data_row(Default.get_default_settings(user_id))

        markup = types.InlineKeyboardMarkup()
        if get_default_setting[0]['current_weather']:
            markup.add(inline_current_weather_btn())
        markup.add(inline_hourly_weather_btn(f" ({get_default_setting[0]['hourly_weather']}-hour forecast)"))
        markup.add(inline_daily_weather_btn(f" ({get_default_setting[0]['daily_weather']}-day forecast)"))
        markup.add(inline_cancel_btn())
        delete_msg(chat_id, user_id)
        msg = bot.send_message(message.chat.id,
                               f"Your favorite location - <b>{get_users_location[0]['user_city']}</b>",
                               reply_markup=markup, parse_mode='HTML')
        data.globals.users_dict[user_id]['message_id'] = msg.message_id
        # TODO weather display
