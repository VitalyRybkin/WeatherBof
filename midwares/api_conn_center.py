import calendar
from datetime import datetime

import requests
from htmlwebshot import WebShot, Config
import imgkit
from requests import Response

from data.config import API_TOKEN
from midwares.api_lib import CurrentAmerican, CurrentMetric, LocationInfo
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Current, User


def get_current_weather(loc_id, bot_user_id) -> str:
    get_user_settings = read_data_row(
        Current.get_user_current_weather_settings(bot_user_id=bot_user_id)
    )[0]
    get_user_units = read_data_row(User.get_user_config(bot_user_id))[0]
    current_weather: dict = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={API_TOKEN}&q=id:{loc_id}&aqi=no"
    ).json()

    loc_info = LocationInfo(
        name=current_weather["location"]["name"],
        region=current_weather["location"]["region"],
        country=current_weather["location"]["country"],
        lat=current_weather["location"]["lat"],
        lon=current_weather["location"]["lon"],
        localtime=current_weather["location"]["localtime"],
    )

    if get_user_units["metric"] == "metric":
        parse_loc_weather = CurrentMetric(
            last_updated=current_weather["current"]["last_updated"],
            temp_c=current_weather["current"]["temp_c"],
            condition=current_weather["current"]["condition"]["text"],
            wind_kph=current_weather["current"]["wind_kph"],
            wind_dir=current_weather["current"]["wind_dir"]
            if bool(get_user_settings["wind_extended"])
            else None,
            pressure_mb=current_weather["current"]["pressure_mb"]
            if bool(get_user_settings["pressure"])
            else None,
            precip_mm=current_weather["current"]["precip_mm"],
            cloud=current_weather["current"]["cloud"],
            humidity=current_weather["current"]["humidity"]
            if bool(get_user_settings["humidity"])
            else None,
            feelslike_c=current_weather["current"]["feelslike_c"],
            vis_km=current_weather["current"]["vis_km"]
            if bool(get_user_settings["visibility"])
            else None,
            gust_kph=current_weather["current"]["gust_kph"]
            if bool(get_user_settings["wind_extended"])
            else None,
        )
    else:
        parse_loc_weather = CurrentAmerican(
            last_updated=current_weather["current"]["last_updated"],
            temp_f=current_weather["current"]["temp_f"],
            condition=current_weather["current"]["condition"]["text"],
            wind_mph=current_weather["current"]["wind_mph"],
            wind_dir=current_weather["current"]["wind_dir"]
            if bool(get_user_settings["wind_extended"])
            else None,
            pressure_in=current_weather["current"]["pressure_in"]
            if bool(get_user_settings["pressure"])
            else None,
            precip_in=current_weather["current"]["precip_in"],
            cloud=current_weather["current"]["cloud"],
            humidity=current_weather["current"]["humidity"]
            if bool(get_user_settings["humidity"])
            else None,
            feelslike_f=current_weather["current"]["feelslike_f"],
            vis_miles=current_weather["current"]["vis_miles"]
            if bool(get_user_settings["visibility"])
            else None,
            gust_mph=current_weather["current"]["gust_mph"]
            if bool(get_user_settings["wind_extended"])
            else None,
        )

    # text = dataclasses.asdict(parse_loc_weather)
    # text = parse_loc_weather.__repr__()

    html_file: str = create_html(parse_loc_weather, loc_info)
    with open("./html/current_weather_index.html", "w") as current_weather_html:
        current_weather_html.write(html_file)

    shot = WebShot()
    shot.config = Config(
        wkhtmltopdf="/usr/local/bin/wkhtmltopdf",
        wkhtmltoimage="/usr/local/bin/wkhtmltoimage",
    )
    shot.flags = [
        "--quiet",
        "--enable-javascript",
        "--no-stop-slow-scripts",
        "--encoding 'UTF-8'",
        "--images",
    ]
    shot.params = {"--crop-w": 315}
    #  shot.delay = 5
    weather_pic = shot.create_pic(
        html="./html/current_weather_index.html",
        css="./html/current_weather_style.css",
        output="out.jpg",
    )

    options = {
        "format": "png",
        "crop-w": "315",
        "encoding": "UTF-8",
        "enable-javascript": None,
        "enable-local-file-access": None,
    }

    css = "./html/current_weather_style.css"
    with open("./html/current_weather_js_index.html", "r"):
        imgkit.from_file(
            "./html/current_weather_js_index.html", "out3.png", options=options, css=css
        )

    return weather_pic


def get_forecast_weather(loc_name, days):
    return f"http://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q={loc_name}&days={days}&aqi=no&alerts=no"


def api_search_location(loc_name) -> Response:
    return requests.get(
        f"http://api.weatherapi.com/v1/search.json?key={API_TOKEN}&q={loc_name}&aqi=no"
    )


def create_html(parse_loc_weather, loc_info) -> str:
    # TODO rewrite with Airium
    parsed_weather = parse_loc_weather.__repr__()

    week_day = calendar.day_name[
        datetime.strptime(
            parse_loc_weather.last_updated.split()[0], "%Y-%m-%d"
        ).weekday()
    ]
    month_date = datetime.strptime(
        parse_loc_weather.last_updated.split()[0], "%Y-%m-%d"
    ).day
    time = parse_loc_weather.last_updated.split()[1]

    header = (
        f"<!DOCTYPE html>\n"
        f'<html lang="en">\n'
        f"<head>\n"
        f'<meta http-equiv="Content-Type" content="text/html" charset="utf-8" />\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<link rel="stylesheet" href="current_weather_style.css">\n'
        '<link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">\n'
        f"<title>Current weather</title>\n"
        f"</head>\n"
        f"<body>\n"
    )

    table_head = (
        f"\t<thead>\n"
        f"\t\t<tr>\n"
        f'\t\t\t<th colspan="2" class="header">{loc_info.name}, {loc_info.country}</th>\n'
        f"\t\t</tr>\n"
        f"\t\t<tr>\n"
        f'\t\t\t<th colspan="2" class="header"><span>{week_day}, {month_date}, {time}</span></th>\n'
        f"\t\t</tr>\n"
        f"\t</thead>\n"
    )

    table_body = f'\t<tbody class="table_body">\n' f"{parsed_weather}" f"\t</tbody>\n"

    return (
        f"{header}\n"
        f"<table>\n"
        f"{table_head}\n"
        f"{table_body}"
        f"</table>\n"
        f"</body>\n</html>"
    )
