from telebot import types

from keyboards.inline.inline_buttons import inline_cancel_btn
from loader import bot
from midwares.db_conn_center import write_data, read_data
from midwares.sql_lib import Users, Favorites
from states.bot_states import States
import data.globals


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    parse_call_data = call.data.split("|")
    msg = call.message
    if call.data == "Cancel":
        bot.delete_state(call.from_user.id, call.message.chat.id)
        bot.send_message(call.message.chat.id, "\U0000274C Canceled!")
    elif call.data == "Set prompt" or call.data == "Add prompt" or call.data == "Change prompt":
        bot.set_state(call.from_user.id, States.search_location, call.message.chat.id)
        markup = types.InlineKeyboardMarkup()
        States.search_location.operation = call.data
        cancel_keyboard = markup.row(inline_cancel_btn())
        msg = bot.send_message(
            call.message.chat.id, "Type in city name:", reply_markup=cancel_keyboard
        )
    elif parse_call_data[0] == "Add":
        if parse_call_data[1] == "favorite":
            bot.send_message(call.message.chat.id, "Favorite location set!")
            query = (
                f"UPDATE {Users.table_name} "
                f"SET {Users.user_city}='{parse_call_data[2]}' "
                f"WHERE {Users.user_id}={call.from_user.id}"
            )
            write_data(query)
        elif parse_call_data[1] == "wishlist":
            query = (
                f"SELECT {Favorites.user_favorite_city_name} "
                f"FROM {Favorites.table_name} "
                f"WHERE {Favorites.favorites_user_id}={call.from_user.id}"
            )
            get_wishlist_info = read_data(query)

            if not get_wishlist_info:
                bot.send_message(call.message.chat.id, "Location added to wishlist!")
                query = (
                    f"INSERT INTO {Favorites.table_name} "
                    f"({Favorites.favorites_user_id}, {Favorites.user_favorite_city_name}) "
                    f"VALUES ({call.from_user.id}, '{parse_call_data[2]}')"
                )
                write_data(query)
            else:
                bot.send_message(call.message.chat.id, "Location is in your wishlist!")
                return
        bot.set_state(call.message.from_user.id, States.cancel, call.message.chat.id)

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]['message_id'],
        reply_markup="")
    data.globals.users_dict[call.from_user.id]['message_id'] = msg.message_id
