from handlers.users.default_config import default_config_setting, set_duration
from loader import bot
from midwares.sql_lib import Hourly, Daily
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: call.data == "current_weather")
def set_metric(call):
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
def change_forecast_duration(call):
    States.default_setting.user_id = call.from_user.id
    States.set_duration_prompt.duration = call.data
    bot.set_state(call.from_user.id, States.set_duration_prompt, call.message.chat.id)
    set_duration(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "back")
def back(call):
    bot.set_state(call.from_user.id, States.default_setting, call.message.chat.id)

    default_config_setting(call.message)
