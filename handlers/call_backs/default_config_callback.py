from handlers.users.default_config import default_config_setting, set_duration
from loader import bot
from midwares.sql_lib import Hourly, Daily, Current
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: call.data == Current.table_name)
def set_metric(call) -> None:
    """
    Function. Changing default settings (current weather display on/off) in a setting dict.
    :param call:
    :return:
    """
    States.default_setting.user_id = call.from_user.id
    bot.set_state(call.from_user.id, States.default_setting, call.message.chat.id)
    if States.default_setting.settings_dict[call.data] == 0:
        States.default_setting.settings_dict[call.data] = 1
    else:
        States.default_setting.settings_dict[call.data] = 0

    default_config_setting(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data in [Hourly.table_name, Daily.table_name]
)
def change_forecast_duration(call) -> None:
    """
    Function. Setting hour (1 to 12) or day (1 to 3) forecast duration.
    :param call:
    :return:
    """
    States.default_setting.user_id = call.from_user.id
    States.set_duration_prompt.duration = call.data
    bot.set_state(call.from_user.id, States.set_duration_prompt, call.message.chat.id)
    set_duration(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call) -> None:
    """
    Function. Setting back previous state.
    :param call:
    :return:
    """
    bot.set_state(call.from_user.id, States.default_setting, call.message.chat.id)

    default_config_setting(call.message)
