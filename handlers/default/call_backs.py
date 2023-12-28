from telebot import types

from keyboards.inline.inline_buttons import inline_cancel_btn
from loader import bot
from midwares.db_conn_center import write_data
from midwares.sql_lib import Users
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    parse_call_data = call.data.split("|")
    if call.data == "Cancel":
        bot.delete_state(call.from_user.id, call.message.chat.id)
        bot.send_message(call.message.chat.id, "\U0000274C Canceled!")
    if call.data == "Set prompt":
        bot.set_state(call.from_user.id, States.search_location, call.message.chat.id)
        markup = types.InlineKeyboardMarkup()
        cancel_keyboard = markup.row(inline_cancel_btn())
        bot.send_message(
            call.message.chat.id, "Type in city name:", reply_markup=cancel_keyboard
        )
    if parse_call_data[0] == "Add":
        if parse_call_data[1] == "favorite":
            bot.send_message(call.message.chat.id, "Location set!")
            query = (
                f"UPDATE {Users.table_name} "
                f"SET {Users.user_city}='{parse_call_data[2]}' "
                f"WHERE {Users.user_id}={call.from_user.id}"
            )
            write_data(query)
        elif parse_call_data[1] == "wishlist":
            pass
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id - 2, reply_markup=""
        )
        bot.set_state(call.message.from_user.id, States.cancel, call.message.chat.id)

    bot.edit_message_reply_markup(
        call.message.chat.id, message_id=call.message.message_id, reply_markup=""
    )
