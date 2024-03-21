from icecream import ic

from handlers.call_backs.my_callback import (
    display_current_weather,
    current_weather,
    daily_weather,
    hourly_weather,
)
from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Default, Current, User
from states.bot_states import States


@bot.message_handler(commands=["onetouch"])
def onetouch(message) -> None:
    """
    Function. Executes one touch command. Displays weather upon user's default settings
    """

    get_user_settings = read_data_row(
        Default.get_default_settings(bot_user_id=message.from_user.id)
    )

    if get_user_settings[0]["current_weather"]:
        bot.set_state(message.from_user.id, States.my_prompt, message.chat.id)
        get_users_location = read_data_row(
            User.get_user_location_info(bot_user_id=message.from_user.id)
        )
        States.my_prompt.loc_id = get_users_location[0]["id"]
        current_weather(message.from_user.id, message.chat.id)

    if get_user_settings[0]["daily_weather"] != 0:
        daily_weather(
            message.from_user.id, message.chat.id, get_user_settings[0]["daily_weather"]
        )

    if get_user_settings[0]["hourly_weather"] != 0:
        hourly_weather(
            message.from_user.id,
            message.chat.id,
            get_user_settings[0]["hourly_weather"],
        )
