import data
from handlers.users.preferences import (
    customize_current_setting,
    customize_daily_setting,
    customize_hourly_setting,
    change_settings,
)
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import read_data_row, write_data
from midwares.sql_lib import Current, User, Daily, Hourly, Default
from states.bot_states import States


@bot.callback_query_handler(
    func=lambda call: call.data
    in ["Current settings", "Daily settings", "Hourly settings"]
)
def user_settings_prompt(call) -> None:
    """
    Function. Change state, display user settings, call next step.
    :param call:
    :return: None
    """

    match call.data:
        case "Current settings":
            bot.set_state(
                call.from_user.id, States.customize_current, call.message.chat.id
            )
            States.customize_current.user_id = call.from_user.id
            settings = (
                "<b>\U0001F4C2 Current weather settings:</b>\n\n"
                "\U0001F4C4 <b>Default output:</b>\n"
                "       - temperature;\n"
                "       - 'feels like' temperature;\n"
                "       - wind;\n"
                "       - clouds; \n"
                "       - precipitations;"
            )

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Current.humidity}, {Current.pressure}, {Current.visibility}, {Current.wind_extended} "
                f"FROM {Current.table_name} "
                f"WHERE {Current.current_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_current.settings_dict = read_data_row(query)
            customize_current_setting(call.message)
        case "Daily settings":
            bot.set_state(
                call.from_user.id, States.customize_daily, call.message.chat.id
            )
            States.customize_daily.user_id = call.from_user.id

            settings = (
                "<b>\U0001F4C2 Daily weather settings:</b>\n\n"
                "\U0001F4C4 <b>Default output:</b>\n"
                "       - max temperature;\n"
                "       - min temperature;\n"
                "       - average temperature;\n"
                "       - max wind;\n"
                "       - total precipitations;\n"
                "       - chance of rain;\n"
                "       - chance of snow;\n"
            )

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Daily.humidity}, {Daily.visibility}, {Daily.astro} "
                f"FROM {Daily.table_name} "
                f"WHERE {Daily.daily_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_daily.settings_dict = read_data_row(query)
            customize_daily_setting(call.message)
        case "Hourly settings":
            bot.set_state(
                call.from_user.id, States.customize_hourly, call.message.chat.id
            )
            States.customize_hourly.user_id = call.from_user.id
            settings = (
                "<b>\U0001F4C2 Hourly weather settings:</b>\n\n"
                "\U0001F4C4 <b>Default output:</b>\n"
                "       - temperature;\n"
                "       - 'feels like' temperature;\n"
                "       - wind;\n"
                "       - clouds; \n"
                "       - chance of rain;\n"
                "       - chance of snow;\n"
                "       - precipitations;\n"
            )

            bot.send_message(call.message.chat.id, settings, parse_mode="HTML")
            query = (
                f"SELECT {Hourly.humidity}, {Hourly.pressure}, {Hourly.visibility}, {Hourly.wind_extended} "
                f"FROM {Hourly.table_name} "
                f"WHERE {Hourly.hourly_weather_user_id}="
                # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
                f"({User.get_user_id(call.from_user.id)})"
            )
            States.customize_hourly.settings_dict = read_data_row(query)
            customize_hourly_setting(call.message)


@bot.callback_query_handler(func=lambda call: "Change" in call.data)
def change_setting(call) -> None:
    """
    Function. Setting next state on changing location.
    :param call:
    :return: None
    """
    parse_call_data = call.data.split("|")
    bot.set_state(call.from_user.id, States.change_setting, call.message.chat.id)
    States.change_setting.user_id = call.from_user.id
    States.change_setting.setting = parse_call_data[1]

    change_settings(call.message)


@bot.callback_query_handler(func=lambda call: "Switch setting" in call.data)
def switch_setting(call) -> None:
    """
    Function. Switching user settings on user click button.
    :param call:
    :return: None
    """
    parse_call_data = call.data.split("|")
    match parse_call_data[1]:
        case Current.table_name:
            States.customize_current.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_current.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )
        case Hourly.table_name:
            States.customize_hourly.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_hourly.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )
        case Daily.table_name:
            States.customize_daily.settings_dict[0][parse_call_data[2]] = (
                1
                if States.customize_daily.settings_dict[0][parse_call_data[2]] == 0
                else 0
            )

    bot.delete_message(
        call.message.chat.id, data.globals.users_dict[call.from_user.id]["message_id"]
    )
    data.globals.users_dict[call.from_user.id]["message_id"] = 0
    change_settings(call.message)


@bot.callback_query_handler(func=lambda call: "Save" in call.data)
def save_settings(call) -> None:
    """
    Function. Save user settings.
    :param call:
    :return: None
    """
    parse_call_data = call.data.split("|")
    table_name = fields = condition = msg_text = ""
    match parse_call_data[1]:
        case Current.table_name:
            table_name = Current.table_name
            # condition = Current.table_name + '_user_id'
            condition = Current.current_weather_user_id
            for k, v in States.customize_current.settings_dict[0].items():
                fields += k + f"={v}, "
        case Hourly.table_name:
            table_name = Hourly.table_name
            # condition = Hourly.table_name + '_user_id'
            condition = Hourly.hourly_weather_user_id
            for k, v in States.customize_hourly.settings_dict[0].items():
                fields += k + f"={v}, "
        case Daily.table_name:
            table_name = Daily.table_name
            # condition = Daily.table_name + '_user_id'
            condition = Daily.daily_weather_user_id
            for k, v in States.customize_daily.settings_dict[0].items():
                fields += k + f"={v}, "
        case User.table_name:
            table_name = User.table_name
            condition = User.user_id
            for k, v in States.user_config_setting.settings_dict.items():
                v = v if isinstance(v, int) else f"'{v}'"
                fields += k + f"={v}, "
            if States.user_config_setting.settings_dict["reply_menu"] == 1:
                msg_text = "You can hide your bottom menu here /userconfig !"
            else:
                msg_text = "You can pop up your bottom menu here /userconfig !:"
        case Default.table_name:
            table_name = Default.table_name
            condition = Default.default_user_id
            for k, v in States.default_setting.settings_dict.items():
                v = v if isinstance(v, int) else f"'{v}'"
                fields += k + f"={v}, "
    fields = fields[:-2]
    query = (
        f"UPDATE {table_name} "
        f"SET {fields} "
        f"WHERE {condition}="
        # f"(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={call.from_user.id})"
        f"({User.get_user_id(call.from_user.id)})"
    )

    write_data(query)

    bot.send_message(call.message.chat.id, f"\U00002705 Saved!")

    if msg_text:
        keyboards = reply_bottom_menu_kb(call.from_user.id)
        bot.send_message(
            call.message.chat.id,
            msg_text,
            reply_markup=keyboards,
        )
