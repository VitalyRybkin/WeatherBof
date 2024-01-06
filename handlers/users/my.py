from telebot import types

import data.globals
from keyboards.inline.inline_buttons import inline_forecast_btn, inline_cancel_btn, inline_current_weather_btn
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Users
from states.bot_states import States


@bot.message_handler(commands=['my'])
@bot.message_handler(state=States.my)
def my(message):
    if (not data.globals.users_dict[message.from_user.id]['message_id'] == 0 and
            not bot.get_state(message.from_user.id, message.chat.id) == States.my):
        bot.edit_message_reply_markup(message.chat.id,
                                      data.globals.users_dict[message.from_user.id]['message_id'],
                                      reply_markup="")

    query = (f"SELECT {Users.user_city} "
             f"FROM {Users.table_name} "
             f"WHERE {Users.user_id}={message.from_user.id}")

    get_users_location = read_data(query)
    print(get_users_location)

    if not get_users_location:
        bot.send_message(message.chat.id, "You haven\'t set your favorite location yet!")
    else:
        bot.set_state(message.from_user.id, States.my, message.chat.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(inline_current_weather_btn())
        markup.add(inline_forecast_btn())
        markup.add(inline_cancel_btn())
        bot.send_message(message.chat.id, f"Your favorite location - <b><u>{get_users_location[0][0]}</u></b>",
                         reply_markup=markup,
                         parse_mode='HTML')
