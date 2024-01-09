from loader import bot
from midwares.db_conn_center import read_data
from midwares.sql_lib import Current, Users, Hourly, Daily


@bot.message_handler(commands=["watch_custom"])
def watch_custom(message):
    query = (f'SELECT {Current.humidity}, {Current.pressure}, {Current.visibility}, {Current.wind_extended} '
             f'FROM {Current.table_name} '
             f'WHERE {Current.current_weather_user_id}='
             f'(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id})')
    get_settings = read_data(query)
    print(get_settings)
    query = (f'SELECT {Hourly.humidity}, {Hourly.pressure}, {Hourly.visibility}, {Hourly.wind_extended} '
             f'FROM {Hourly.table_name} '
             f'WHERE {Hourly.hourly_weather_user_id}='
             f'(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id})')
    get_settings = read_data(query)
    print(get_settings)
    query = (f'SELECT {Daily.humidity}, {Daily.visibility}, {Daily.astro} '
             f'FROM {Daily.table_name} '
             f'WHERE {Daily.daily_weather_user_id}='
             f'(SELECT {Users.id} FROM {Users.table_name} WHERE {Users.user_id}={message.from_user.id})')
    get_settings = read_data(query)
    print(get_settings)
