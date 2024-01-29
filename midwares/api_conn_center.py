import dataclasses
import json
from htmlwebshot import WebShot, Config

import requests
from requests import Response

from data.config import API_TOKEN
from midwares.api_lib import CurrentAmerican, CurrentMetric
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Current, User
import imgkit


def get_current_weather(loc_id, bot_user_id) -> str:
    get_user_settings = read_data_row(Current.get_user_current_weather_settings(bot_user_id=bot_user_id))[0]
    get_user_units = read_data_row(User.get_user_config(bot_user_id))[0]
    current_weather: dict = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={API_TOKEN}&q=id:{loc_id}&aqi=no"
    ).json()
    if get_user_units['metric'] == 'metric':
        parse_current_weather = CurrentMetric(
            name=current_weather['location']['name'],
            region=current_weather['location']['region'],
            country=current_weather['location']['country'],
            lat=current_weather['location']['lat'],
            lon=current_weather['location']['lon'],
            localtime=current_weather['location']['localtime'],
            last_updated=current_weather['current']['last_updated'],
            temp_c=current_weather['current']['temp_c'],
            condition=current_weather['current']['condition']['text'],
            wind_kph=current_weather['current']['wind_kph'],
            wind_dir=current_weather['current']['wind_dir'] if bool(get_user_settings['wind_extended']) else None,
            pressure_mb=current_weather['current']['pressure_mb'] if bool(get_user_settings['pressure']) else None,
            precip_mm=current_weather['current']['precip_mm'],
            cloud=current_weather['current']['cloud'],
            humidity=current_weather['current']['humidity'] if bool(get_user_settings['humidity']) else None,
            feelslike_c=current_weather['current']['feelslike_c'],
            vis_km=current_weather['current']['vis_km'] if bool(get_user_settings['visibility']) else None,
            gust_kph=current_weather['current']['gust_kph'] if bool(get_user_settings['wind_extended']) else None
        )
    else:
        parse_current_weather = CurrentAmerican(
            name=current_weather['location']['name'],
            region=current_weather['location']['region'],
            country=current_weather['location']['country'],
            lat=current_weather['location']['lat'],
            lon=current_weather['location']['lon'],
            localtime=current_weather['location']['localtime'],
            last_updated=current_weather['current']['last_updated'],
            temp_f=current_weather['current']['temp_f'],
            condition=current_weather['current']['condition']['text'],
            wind_mph=current_weather['current']['wind_mph'],
            wind_dir=current_weather['current']['wind_dir'] if bool(get_user_settings['wind_extended']) else None,
            pressure_in=current_weather['current']['pressure_in'] if bool(get_user_settings['pressure']) else None,
            precip_in=current_weather['current']['precip_in'],
            cloud=current_weather['current']['cloud'],
            humidity=current_weather['current']['humidity'] if bool(get_user_settings['humidity']) else None,
            feelslike_f=current_weather['current']['feelslike_f'],
            vis_miles=current_weather['current']['vis_miles'] if bool(get_user_settings['visibility']) else None,
            gust_mph=current_weather['current']['gust_mph'] if bool(get_user_settings['wind_extended']) else None
        )

    text = dataclasses.asdict(parse_current_weather)

    html_file: str = create_html(text)
    with open('./html/current_weather_index.html', 'w') as current_weather_html:
        current_weather_html.write(html_file)

    shot = WebShot()
    shot.config = Config(wkhtmltopdf="/usr/local/bin/wkhtmltopdf", wkhtmltoimage="/usr/local/bin/wkhtmltoimage")
    shot.flags = ["--quiet", "--enable-javascript", "--no-stop-slow-scripts", "--javascript-delay: 500"]
    shot.params = {"--crop-w": 415}
    shot.delay = 5
    weather_pic = shot.create_pic(html="./html/current_weather_index.html", css="./html/current_weather_style.css",
                                  output="out.jpg")

    text_js = [dataclasses.asdict(parse_current_weather)]

    with open('./html/current_weather.json', 'w') as current_weather_info:
        json.dump(text_js, current_weather_info, indent=4)

    shot.create_pic(html="./html/current_weather_js_index.html", css="./html/current_weather_style.css",
                    output="out_js.jpg")

    # kitoptions = {
    #     "enable-local-file-access": None
    # }
    #
    # # imgkit.from_file('./html/current_weather_index.html', './out.jpg')
    # result = imgkit.from_file('./html/current_weather_index.html', 'out.jpg', options=kitoptions)

    return weather_pic


def get_forecast_weather(loc_name, days):
    return f"http://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q={loc_name}&days={days}&aqi=no&alerts=no"


def api_search_location(loc_name) -> Response:
    return requests.get(
        f"http://api.weatherapi.com/v1/search.json?key={API_TOKEN}&q={loc_name}&aqi=no"
    )


def create_html(parse_current_weather) -> str:
    # TODO rewrite with Airium
    header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="current_weather_style.css">
        <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
        <title>Current weather</title>
    </head>
    <body>
        """

    table_head = f"""
        <thead>
          <tr>
            <th colspan="2" class="header">Last updated:  <span>{parse_current_weather["last_updated"]}</span></th>
          </tr>
        </thead>
    """

    table_body = f"""
    <tbody class="table_body">
"""
    for k, v in parse_current_weather.items():
        if not k == 'last_updated':
            table_body += f"\t\t\t<tr><td>{k}</td>"
            table_body += f"<td>{v}</td></tr>\n"

    table_body += """
        </tbody>
    """

    return (f"{header}\n"
            f"<table>\n"
            f"{table_head}\n"
            f"{table_body}"
            f"</table>\n"
            f"</body>\n</html>")
