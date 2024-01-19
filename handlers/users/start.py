from telebot import types

from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_set_location_prompt_btn,
)
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import read_data, write_data
from midwares.sql_lib import User, Current, Daily, Hourly, Default
from states.bot_states import States
from utils.reply_center import Reply
import data.globals


@bot.message_handler(commands=["start"])
def start_command(message):
    """
    Function. Bot start workout. Check if user is new or old user back. Executes 'start' command. Writes settings in db.
    :param message:
    :return:
    """
    user_id = message.from_user.id
    chat_id = message.chat.id

    query = f"SELECT {User.bot_user}, {User.user_city} FROM {User.table_name} WHERE {User.bot_user}={user_id}"
    get_user_info = read_data(query)
    print(get_user_info)

    if not get_user_info:
        write_data(
            f'INSERT INTO {User.table_name} ("{User.bot_user}") VALUES ({user_id})'
        )
        write_data(
            f'INSERT INTO {Current.table_name} ("{Current.current_weather_user_id}") '
            f"VALUES (({User.get_user_id(user_id)}))"
        )
        write_data(
            f'INSERT INTO {Daily.table_name} ("{Daily.daily_weather_user_id}") '
            f"VALUES (({User.get_user_id(user_id)}))"
        )
        write_data(
            f'INSERT INTO {Hourly.table_name} ("{Hourly.hourly_weather_user_id}") '
            f"VALUES (({User.get_user_id(user_id)}))"
        )
        write_data(
            f'INSERT INTO {Default.table_name} ("{Default.default_user_id}") '
            f"VALUES (({User.get_user_id(user_id)}))"
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

        if user_id not in data.globals.users_dict:
            data.globals.users_dict.setdefault(user_id, dict())
            data.globals.users_dict[user_id]["count_not_defined"] = 0
            data.globals.users_dict[user_id]["message_id"] = 0
            # data.globals.users_dict[user_id]['user_id'] = user_id
            data.globals.users_dict[user_id]["chat_id"] = chat_id
            # data.globals.users_dict[user_id]['state'] = None
            # data.globals.users_dict[user_id]['city'] = None
            # TODO delete/edit messages

        if bot.get_state(user_id, chat_id):
            bot.delete_state(user_id, chat_id)
    else:
        # if not data.globals.users_dict[message.from_user.id]['message_id'] == 0:
        #     bot.edit_message_reply_markup(
        #         message.chat.id,
        #         message_id=data.globals.users_dict[message.from_user.id]['message_id'],
        #         reply_markup="")
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
            msg = bot.send_message(
                chat_id,
                "You haven't /set your favorite city, yet!",
                reply_markup=set_city_keyboard,
            )
            data.globals.users_dict[user_id]["message_id"] = msg.message_id
        else:
            # check_weather_keyboard = show_weather()
            # msg = bot.send_message(
            #     chat_id,
            #     f"\U0001F3D9 Your favorite city: \n{get_user_info[0][1]}",
            #     reply_markup=check_weather_keyboard,
            # )
            keyboards = reply_bottom_menu_kb(message.from_user.id)
            bot.send_message(
                chat_id,
                "You can hide bottom menu here /userconfig !",
                reply_markup=keyboards,
            )
