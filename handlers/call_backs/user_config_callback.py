from handlers.users.user_config import user_config, configuring_settings
from loader import bot
from states.bot_states import States


@bot.callback_query_handler(func=lambda call: call.data == 'metric')
def set_metric(call):
    States.config_settings.user_id = call.from_user.id
    bot.set_state(call.from_user.id, States.config_settings, call.message.chat.id)
    if States.user_config_setting.settings_dict['metric'] == 'metric':
        States.user_config_setting.settings_dict['metric'] = 'american'
    else:
        States.user_config_setting.settings_dict['metric'] = 'metric'
    configuring_settings(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'reply_menu')
def set_reply_menu(call):
    print("ku")