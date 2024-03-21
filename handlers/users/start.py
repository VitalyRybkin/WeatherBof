import logging

from telebot import types
from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards.inline.inline_buttons import (
    inline_cancel_btn,
    inline_set_location_prompt_btn,
)
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import read_data, write_data
from midwares.sql_lib import User, Current, Daily, Hourly, Default
from states.bot_states import States
from utils.global_functions import delete_msg
from utils.reply_center import Reply
import data.globals

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(message)s")
file_handler = logging.FileHandler("./logs/users_log.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# logging.basicConfig(level=logging.INFO,
#                     filename="./logs/users_log.log",
#                     format="%(asctime)s | %(message)s")


@bot.message_handler(commands=["start"])
@bot.message_handler(state=States.start)
def start_command(message) -> None:
    """
    Function. Execute start command. Check if user is new or old user back. Executes 'start' command. Writes settings in db.
    :param message:
    :return: None
    """
    user_id: int = message.from_user.id
    chat_id: int = message.chat.id

    query: str = f"SELECT {User.bot_user_id}, {User.name} FROM {User.table_name} WHERE {User.bot_user_id}={user_id}"
    get_user_info: list = read_data(query)

    if not get_user_info:
        write_data(
            f'INSERT INTO {User.table_name} ("{User.bot_user_id}") VALUES ({user_id})'
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
        reply_from: Reply = Reply(message)
        res: str = "\n".join("{} - {}".format(k, v) for k, v in reply_from.help.items())
        bot.send_message(chat_id, res)
        bot.send_message(chat_id, "Enjoy!")

        if user_id not in data.globals.users_dict:
            data.globals.users_dict.setdefault(user_id, dict())
            data.globals.users_dict[user_id]["count_not_defined"] = 0
            data.globals.users_dict[user_id]["message_id"] = 0
            data.globals.users_dict[user_id]["message_list"] = []
            data.globals.users_dict[user_id]["chat_id"] = chat_id

        if bot.get_state(user_id, chat_id):
            bot.delete_state(user_id, chat_id)

        logging.info(f"User registered: {user_id} | {message.from_user.first_name}")

    else:
        bot.send_message(
            chat_id,
            f"Hello, {message.from_user.first_name}!\n" f"Welcome back!",
        )

        if get_user_info[0][1] is None:
            bot.set_state(user_id, States.start, chat_id)

            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            cancel: InlineKeyboardButton = inline_cancel_btn()
            set_city: InlineKeyboardButton = inline_set_location_prompt_btn()
            set_city_keyboard: InlineKeyboardMarkup = markup.add(set_city, cancel)

            if not data.globals.users_dict[user_id]["message_id"] == 0:
                delete_msg(chat_id, user_id)

            msg: Message = bot.send_message(
                chat_id,
                "You haven't /set your favorite location, yet!",
                reply_markup=set_city_keyboard,
            )
            data.globals.users_dict[user_id]["message_id"] = msg.message_id
        else:
            bot.send_message(
                chat_id,
                f"Your favorite location - <b>{get_user_info[0][1]}</b>",
                parse_mode="HTML",
            )
            keyboards: ReplyKeyboardMarkup = reply_bottom_menu_kb(message.from_user.id)
            bot.send_message(
                chat_id,
                "You can hide bottom menu here /userconfig !",
                reply_markup=keyboards,
            )
