from telebot import types

from keyboards.reply.reply_buttons import reply_cancel_button
from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Users
from states.bot_states import States
from utils.signs_text import ButtonSigns


@bot.message_handler(commands=["set"])
@bot.message_handler(state=States.set_city)
def set_city(message):
    """
    Function. Setting users favorite city.
    :return:
    """
    query = f"SELECT {Users.user_city} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id}"
    get_user_info = read_data(query)

    if get_user_info[0][0] is None:
        if bot.get_state(message.from_user.id, message.chat.id) is None:
            bot.set_state(message.from_user.id, States.set_city, message.chat.id)

        if message.text == ButtonSigns.cancel:
            bot.delete_state(message.from_user.id, message.chat.id)
            return

        if message.text.lower().strip() == "cancel":
            bot.delete_state(message.from_user.id, message.chat.id)
            remove_button = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, ButtonSigns.cancel, reply_markup=remove_button)
            return

        cancel_button = reply_cancel_button()
        bot.send_message(message.chat.id, "Type in city name:", reply_markup=cancel_button)

    else:
        bot.send_message(message.chat.id, f"Your favorite city name: {get_user_info[0][0]}")
        # TODO forecast message and buttons

