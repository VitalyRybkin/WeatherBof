from loader import bot
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Current, User, Hourly, Daily


@bot.message_handler(commands=["watch_custom"])
def watch_custom(message):
    query = (f'SELECT {Current.humidity}, {Current.pressure}, {Current.visibility}, {Current.wind_extended} '
             f'FROM {Current.table_name} '
             f'WHERE {Current.current_weather_user_id}='
             f'(SELECT {User.id} FROM {User.table_name} WHERE {User.user_id}={message.from_user.id})')
    get_settings = read_data_row(query)
    settings = ("<b>\U0001F4C2 Current weather settings:</b>\n\n"
                "\U0001F4C4 <u>Default output:</u>\n"
                "       - temperature;\n"
                "       - 'feels like' temperature;\n"
                "       - wind;\n"
                "       - clouds; \n"
                "       - precipitations;\n\n"
                "\U0001F4C3  <u>Advanced settings:</u>\n")

    settings = create_output_msg(get_settings, settings)
    bot.send_message(message.chat.id, settings, parse_mode='HTML')

    query = (f'SELECT {Hourly.humidity}, {Hourly.pressure}, {Hourly.visibility}, {Hourly.wind_extended} '
             f'FROM {Hourly.table_name} '
             f'WHERE {Hourly.hourly_weather_user_id}='
             f'(SELECT {User.id} FROM {User.table_name} WHERE {User.user_id}={message.from_user.id})')
    get_settings = read_data_row(query)

    settings = ("<b>\U0001F4C2 Hourly weather settings:</b>\n\n"
                "\U0001F4C4 <u>Default output:</u>\n"
                "       - temperature;\n"
                "       - 'feels like' temperature;\n"
                "       - wind;\n"
                "       - clouds; \n"
                "       - chance of rain;\n"
                "       - chance of snow;\n"
                "       - precipitations;\n\n"
                "\U0001F4C3  <u>Advanced settings:</u>\n")

    settings = create_output_msg(get_settings, settings)
    bot.send_message(message.chat.id, settings, parse_mode='HTML')

    query = (f'SELECT {Daily.humidity}, {Daily.visibility}, {Daily.astro} '
             f'FROM {Daily.table_name} '
             f'WHERE {Daily.daily_weather_user_id}='
             f'(SELECT {User.id} FROM {User.table_name} WHERE {User.user_id}={message.from_user.id})')
    get_settings = read_data_row(query)

    settings = ("<b>\U0001F4C2 Daily weather settings:</b>\n\n"
                "\U0001F4C4 <u>Default output:</u>\n"
                "       - max temperature;\n"
                "       - min temperature;\n"
                "       - average temperature;\n"
                "       - max wind;\n"
                "       - total precipitations;\n"
                "       - chance of rain;\n"
                "       - chance of snow;\n\n"
                "\U0001F4C3  <u>Advanced settings:</u>\n")

    settings = create_output_msg(get_settings, settings)
    bot.send_message(message.chat.id, settings, parse_mode='HTML')


# def create_output_msg(get_settings, settings):
#     for row in get_settings:
#         for k, v in row.items():
#             if v == 0:
#                 settings += f"      - {k}: <b>no</b>\n"
#             else:
#                 settings += f"      - {k}: <b>yes</b>\n"
#     return settings
