# from keyboards.reply.reply_buttons import add_button
# from telebot import types

from keyboards.inline.inline_buttons import show_weather
from keyboards.reply.reply_buttons import reply_set_button
from loader import bot
from midwares.db_conn_center import read_data, write_data
from midwares.sql_lib import Users

# from states.bot_states import States
from utils.reply_center import Reply


@bot.message_handler(commands=["start"])
# @bot.message_handler(state=States.start)
def start_command(message):
    # bot.set_state(message.from_user.id, States.start, message.chat.id)
    query = f"SELECT {Users.user_id}, {Users.user_city} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id}"
    get_user_info = read_data(query)
    if not get_user_info:
        write_data(
            f'INSERT INTO {Users.table_name} ("{Users.user_id}") VALUES ({message.from_user.id})'
        )
        bot.send_message(
            message.chat.id,
            f"Hello, {message.from_user.first_name}!\n"
            f"Welcome to our weather forecasting community! \U0001F91D \n\n"
            f"From now on, I'm your weather forecasting partner!  \U0001F324 \U000026C8 \U0001F328 \n"
            f"Look, what I can do for you:",
        )
        reply_from = Reply(message)
        res = "\n".join("{} - {}".format(k, v) for k, v in reply_from.help.items())
        bot.send_message(message.chat.id, res)
        bot.send_message(message.chat.id, "Enjoy!")
        if bot.get_state(message.from_user.id, message.chat.id):
            bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            f"Hello, {message.from_user.first_name}!\n" f"Welcome back!",
        )
        if get_user_info[0][1] is None:
            set_city_keyboard = reply_set_button()
            bot.send_message(
                message.chat.id,
                "You haven't set your favorite city, yet!",
                reply_markup=set_city_keyboard,
            )
        else:
            check_weather_keyboard = show_weather()
            bot.send_message(
                message.chat.id,
                f"Your favorite city: \n{get_user_info[0][1]}",
                reply_markup=check_weather_keyboard,
            )
