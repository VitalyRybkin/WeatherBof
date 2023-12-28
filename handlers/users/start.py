from telebot import types

from keyboards.inline.inline_buttons import (
    show_weather,
    inline_cancel_btn,
    inline_set_location_prompt_btn,
)
from loader import bot
from midwares.db_conn_center import read_data, write_data
from midwares.sql_lib import Users
from states.bot_states import States
from utils.reply_center import Reply


@bot.message_handler(commands=["start"])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    query = f"SELECT {Users.user_id}, {Users.user_city} FROM {Users.table_name} WHERE {Users.user_id}={user_id}"
    get_user_info = read_data(query)

    if not get_user_info:
        write_data(
            f'INSERT INTO {Users.table_name} ("{Users.user_id}") VALUES ({user_id})'
        )
        bot.send_message(
            chat_id,
            f"Hello, {message.from_user.first_name}!\n"
            f"Welcome to our weather forecasting community! \U0001F91D \n\n"
            f"From now on, I'm your weather forecasting partner!  \U0001F324 \U000026C8 \U0001F328 \n"
            f"Look, what I can do for you:",
        )
        reply_from = Reply(message)
        res = "\n".join("{} - {}".format(k, v) for k, v in reply_from.help.items())
        bot.send_message(chat_id, res)
        bot.send_message(chat_id, "Enjoy!")
        if bot.get_state(user_id, chat_id):
            bot.delete_state(user_id, chat_id)
    else:
        bot.send_message(
            chat_id,
            f"Hello, {message.from_user.first_name}!\n" f"Welcome back!",
        )
        bot.set_state(user_id, States.start, chat_id)
        if get_user_info[0][1] is None:
            markup = types.InlineKeyboardMarkup()
            cancel = inline_cancel_btn()
            set_city = inline_set_location_prompt_btn()
            set_city_keyboard = markup.add(set_city, cancel)
            bot.send_message(
                chat_id,
                "You haven't /set your favorite city, yet!",
                reply_markup=set_city_keyboard,
            )
        else:
            check_weather_keyboard = show_weather()
            bot.send_message(
                chat_id,
                f"Your favorite city: \n{get_user_info[0][1]}",
                reply_markup=check_weather_keyboard,
            )
