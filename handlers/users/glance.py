import copy
import re

from icecream import ic
from requests import Response
from telebot import types
from telebot.types import InlineKeyboardMarkup, Message

from handlers.users.set_location import type_location
from keyboards.inline.inline_buttons import inline_cancel_btn, inline_display_btn
from loader import bot
from midwares.api_conn_center import api_search_location
from states.bot_states import States
import data.globals
from utils.global_functions import delete_msg


@bot.message_handler(commands=["takealook"])
def glance_prompt(message) -> None:
    """
    Function. Type location name to be forecasted.
    """
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id

    markup = types.InlineKeyboardMarkup()
    cancel = inline_cancel_btn()
    glance_keyboard = markup.add(cancel)
    msg = bot.send_message(
        chat_id,
        "Type location name you interested in:",
        reply_markup=glance_keyboard,
    )
    bot.set_state(user_id, States.glance_prompt, chat_id)
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


@bot.message_handler(state=States.glance_prompt)
def glance_handler(message) -> None:
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id

    bot_answer_formatting: list = [
        _.lower().capitalize() for _ in re.split("\\s+|-", message.text.strip())
    ]
    city_name: str = "%20".join(bot_answer_formatting)

    response: Response = api_search_location(city_name)

    delete_msg(chat_id, user_id)

    if not response.json():
        ic(response.json())
        bot.send_message(chat_id, "\U0001F937 Location not found!")
        msg = type_location(chat_id)
        data.globals.users_dict[user_id]["message_id"] = msg.message_id
    else:
        States.glance_prompt.loc_dict = copy.deepcopy(response.json())
        for row in States.glance_prompt.loc_dict:
            markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
            markup.add(inline_display_btn(f"{row['id']}", f"{row['name']}"))
            msg: Message = bot.send_message(
                chat_id,
                f"Location found: \n"
                f"{'name:':<10} {row['name']}\n"
                f"{'region:':<10}  {row['region']}\n"
                f"{'country:':<10} {row['country']}",
                reply_markup=markup,
            )
            data.globals.users_dict[user_id]["message_list"].append(msg.message_id)

        markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        markup.add(inline_cancel_btn())
        msg = bot.send_message(
            chat_id,
            "Cancel or send me new location to search for!",
            reply_markup=markup,
        )

        data.globals.users_dict[user_id]["message_id"] = msg.message_id
