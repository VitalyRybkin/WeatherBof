import calendar
import logging
from collections import namedtuple
from datetime import datetime, timedelta

import requests
from airium import Airium
from htmlwebshot import WebShot
from requests import Response

from data.config import API_TOKEN
from midwares.api_lib import (
    current_weather_metric,
    current_weather_am,
    row_text,
    metric_units,
    am_units,
    daily_weather_metric,
    daily_weather_am,
    astro,
    hourly_weather_metric,
    hourly_weather_am,
)
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Current, User, Daily, Hourly

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s | %(message)s")
file_handler = logging.FileHandler("./logs/api_conn_center.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def api_search_location(loc_name) -> Response:
    try:
        return requests.get(
            f"https://api.weatherapi.com/v1/search.json?key={API_TOKEN}&q={loc_name}&aqi=no"
        )
    except requests.exceptions.RequestException as re:
        logger.warning("Search location error: ", re)


def get_current_weather(loc_id, bot_user_id) -> str:
    """
    Function. Create current weather pic
    """
    get_user_settings = read_data_row(
        Current.get_user_current_weather_settings(bot_user_id=bot_user_id)
    )[0]
    get_user_units = read_data_row(User.get_user_config(bot_user_id))[0]

    current_weather: dict = {}
    try:
        current_weather = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={API_TOKEN}&q=id:{loc_id}&aqi=no"
        ).json()
    except requests.exceptions.RequestException as re:
        logger.warning("Current weather request error: ", re)

    for key, val in get_user_settings.items():
        if key == "humidity" and val == 0:
            current_weather["current"]["humidity"] = None
        if key == "pressure" and val == 0:
            current_weather["current"]["pressure_in"] = None
            current_weather["current"]["pressure_mb"] = None
        if key == "visibility" and val == 0:
            current_weather["current"]["vis_km"] = None
            current_weather["current"]["vis_miles"] = None
        if key == "wind_extended" and val == 0:
            current_weather["current"]["gust_kph"] = None
            current_weather["current"]["gust_mph"] = None

    html_file: str = create_html(
        current_weather, get_user_units["metric"], weather_type="current"
    )
    with open("./html/weather.html", "w") as weather:
        weather.write(html_file)

    shot = WebShot()
    shot.flags = [
        "--quiet",
        "--enable-javascript",
        "--no-stop-slow-scripts",
        "--encoding 'UTF-8'",
        "--images",
    ]
    shot.params = {"--crop-w": 315}
    shot.delay = 3
    weather_pic = shot.create_pic(
        html="./html/weather.html",
        css="./html/current_weather_style.css",
        output="./html/weather_pic.jpg",
    )

    return weather_pic


def get_daily_forecast_weather(loc_id, bot_user_id, days):
    get_daily_settings: dict = read_data_row(
        Daily.get_daily_settings(bot_user_id=bot_user_id)
    )[0]
    get_user_units: dict = read_data_row(User.get_user_config(bot_user_id))[0]

    forecast_weather: dict = {}
    try:
        forecast_weather = requests.get(
            f"https://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q=id:{loc_id}&days={days}&aqi=no&alerts=no"
        ).json()
    except requests.exceptions.RequestException as re:
        logger.warning("Current weather request error: ", re)

    for key, val in get_daily_settings.items():
        if key == "astro" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                for k, v in day["astro"].items():
                    day["astro"][k] = None
        if key == "humidity" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                day["day"]["avghumidity"] = None
        if key == "visibility" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                day["day"]["avgvis_km"], day["day"]["avgvis_miles"] = None, None

    html_file: str = create_html(
        forecast_weather, get_user_units["metric"], weather_type="forecast_daily"
    )

    with open("./html/weather.html", "w") as weather:
        weather.write(html_file)

    shot = WebShot()
    shot.flags = [
        "--quiet",
        "--enable-javascript",
        "--no-stop-slow-scripts",
        "--encoding 'UTF-8'",
        "--images",
    ]
    shot.params = {
        "--crop-w": 210 * len(forecast_weather["forecast"]["forecastday"])
                    - 7 * (len(forecast_weather["forecast"]["forecastday"]) - 1)
    }
    shot.delay = 3
    weather_pic = shot.create_pic(
        html="./html/weather.html",
        css="./html/current_weather_style.css",
        output="./html/weather_pic.jpg",
    )

    return weather_pic


def get_hourly_forecast_weather(loc_id, bot_user_id, hours):
    get_hourly_settings: dict = read_data_row(
        Hourly.get_hourly_settings(bot_user_id=bot_user_id)
    )[0]
    get_user_units: dict = read_data_row(User.get_user_config(bot_user_id))[0]
    days = (
        2
        if datetime.date(datetime.now() + timedelta(hours=int(hours)))
           > datetime.date(datetime.now())
        else 1
    )

    forecast_weather: dict = {}
    try:
        forecast_weather: dict = requests.get(
            f"https://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q=id:{loc_id}&days={days}&aqi=no&alerts=no"
        ).json()
    except requests.exceptions.RequestException as re:
        logger.warning("Current weather request error: ", re)

    for key, val in get_hourly_settings.items():
        if key == "pressure" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                for hour in day["hour"]:
                    hour["pressure_in"], hour["pressure_mb"] = None, None
        if key == "humidity" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                for hour in day["hour"]:
                    hour["humidity"] = None
        if key == "visibility" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                for hour in day["hour"]:
                    hour["vis_km"], hour["vis_miles"] = None, None
        if key == "wind_extended" and val == 0:
            for day in forecast_weather["forecast"]["forecastday"]:
                for hour in day["hour"]:
                    (
                        hour["gust_kph"],
                        hour["gust_mph"],
                        hour["windchill_c"],
                        hour["windchill_f"],
                    ) = (None, None, None, None)

    hourly_weather = []
    counter = int(hours)
    day_num = 0
    flag = False
    for day in forecast_weather["forecast"]["forecastday"]:
        for time in day["hour"]:
            forecast_hour = (
                datetime.strptime(time["time"], "%Y-%m-%d %H:%M").time().hour
            )
            if day_num == 0 and datetime.now().hour <= forecast_hour:
                flag = True
            if flag and counter > 0:
                hourly_weather.append(time)
                counter -= 1
        day_num += 1

    pic_array: list = []
    for counter in range(0, len(hourly_weather), 4):
        hourly_weather_slice = hourly_weather[counter:counter + 4] \
            if counter + 4 <= len(hourly_weather) \
            else hourly_weather[counter:]

        html_file: str = create_html(
            forecast_weather,
            get_user_units["metric"],
            weather_type="forecast_hourly",
            hours=hours,
            hourly_weather=hourly_weather_slice,
        )

        with open("./html/weather.html", "w") as weather:
            weather.write(html_file)

        shot = WebShot()
        shot.flags = [
            "--quiet",
            "--enable-javascript",
            "--no-stop-slow-scripts",
            "--encoding 'UTF-8'",
            "--images",
        ]

        shot.params = {"--crop-w": 225 * len(hourly_weather)}
        shot.delay = 1
        weather_pic = shot.create_pic(
            html="./html/weather.html",
            css="./html/current_weather_style.css",
            output=f"./html/weather_pic_{counter}-{counter + 4}.jpg",
        )
        pic_array.append(weather_pic)

    return pic_array


def create_html(
        weather_data: dict, user_units: dict[str, int], weather_type: str, **kwargs
) -> str:
    """
    Function. Creates the HTML string
    :param weather_data: dictionary with weather data
    :param user_units: dictionary with user units
    :param weather_type: weather type output
    :return: HTML string
    """
    weather: dict[str, dict | str] = weather_data["current"]
    location: dict[str, str] = weather_data["location"]
    hourly_weather: list | None = kwargs.get("hourly_weather", None)

    html_doc: Airium = Airium()

    html_doc("<!DOCTYPE html>")
    with html_doc.html(lang="en"):
        with html_doc.head():
            html_doc.meta(content="text/html", charset="utf-8")
            html_doc.meta(
                content="width=device-width, initial-scale=1", name="viewport"
            )
            html_doc.link(
                href="https://fonts.googleapis.com/css2?family=Protest"
                     "+Riot&display=swap",
                rel="stylesheet",
            )
            html_doc.link(href="./current_weather_style.css", rel="stylesheet")
            html_doc.title(_t="Current weather")

        with html_doc.body():
            table_width: str = (
                "300px"
                if weather_type == "current"
                else f"{200 * len(weather_data['forecast']['forecastday'])}px"
                if weather_type == "forecast_daily"
                else f"{225 * len(hourly_weather)}px"
            )
            with html_doc.table(style=f"width:{table_width};"):
                if weather_type == "current":
                    with html_doc.thead():
                        with html_doc.tr():
                            html_doc.th(
                                klass="header header_loc",
                                colspan=2,
                                _t=f'{location["name"].upper()}, '
                                   f'{location["country"].upper()}',
                            )
                        with html_doc.tr():
                            with html_doc.th(klass="header header_date", colspan=2):
                                html_doc.span(
                                    _t=f'{parse_date(weather["last_updated"]).week_day}, '
                                       f'{parse_date(weather["last_updated"]).month_date},'
                                       f' {parse_date(weather["last_updated"]).time}'
                                )
                        with html_doc.tr():
                            with html_doc.th(klass="img", colspan=2):
                                html_doc.img(
                                    src=f'https:{weather["condition"]["icon"]}',
                                    alt="Current weather",
                                )
                        with html_doc.tr():
                            with html_doc.th(klass="condition", colspan=2):
                                html_doc.span(_t=f'{weather["condition"]["text"]}')
                        with html_doc.tr():
                            with html_doc.th(
                                    klass="temp", colspan=2, _t="Temperature: "
                            ):
                                if user_units == "metric":
                                    param = (
                                        f'{weather["temp_c"]}{metric_units["temp_c"]}'
                                    )
                                else:
                                    param = (
                                        f'{weather["temp_f"]}{metric_units["temp_f"]}'
                                    )
                                html_doc.span(_t=param)
                        with html_doc.tr():
                            with html_doc.th(
                                    klass="feelslike", colspan=2, _t="Feels like: "
                            ):
                                if user_units == "metric":
                                    param = f'{weather["feelslike_c"]}{metric_units["feelslike_c"]}'
                                else:
                                    param = f'{weather["feelslike_f"]}{metric_units["feelslike_f"]}'
                                html_doc.span(_t=param)

                elif weather_type == "forecast_daily":
                    with html_doc.thead():
                        with html_doc.tr():
                            html_doc.th(
                                klass="header header_loc",
                                colspan=2
                                        * len(weather_data["forecast"]["forecastday"]),
                                _t=f"{weather_data['location']['name'].upper()}, "
                                   f"{weather_data['location']['country'].upper()}",
                            )
                        with html_doc.tr():
                            for day in weather_data["forecast"]["forecastday"]:
                                with html_doc.th(klass="header header_date", colspan=2):
                                    html_doc.span(
                                        _t=f"{parse_date(day['date']).week_day}, "
                                           f"{parse_date(day['date']).month_date},"
                                    )
                        with html_doc.tr():
                            for day in weather_data["forecast"]["forecastday"]:
                                with html_doc.th(klass="img", colspan=2):
                                    html_doc.img(
                                        src=f"https:{day['day']['condition']['icon']}",
                                        alt="Forecast weather",
                                    )
                        with html_doc.tr():
                            for day in weather_data["forecast"]["forecastday"]:
                                with html_doc.th(klass="condition", colspan=2):
                                    html_doc.span(
                                        _t=f"{day['day']['condition']['text']}"
                                    )
                        with html_doc.tr():
                            for day in weather_data["forecast"]["forecastday"]:
                                with html_doc.th(klass="temp", colspan=2, _t=f"Max"):
                                    if user_units == "metric":
                                        param = f'{day["day"]["maxtemp_c"]}{metric_units["temp_c"]}'
                                    else:
                                        param = f'{day["day"]["maxtemp_f"]}{metric_units["temp_f"]}'
                                    html_doc.span(_t=param)
                        with html_doc.tr():
                            for day in weather_data["forecast"]["forecastday"]:
                                with html_doc.th(
                                        klass="feelslike", colspan=2, _t=f"Min"
                                ):
                                    if user_units == "metric":
                                        param = f'{day["day"]["mintemp_c"]}{metric_units["temp_c"]}'
                                    else:
                                        param = f'{day["day"]["mintemp_f"]}{metric_units["temp_f"]}'
                                    html_doc.span(_t=param)

                elif weather_type == "forecast_hourly":
                    with html_doc.thead():
                        with html_doc.tr():
                            html_doc.th(
                                klass="header header_loc",
                                colspan=2 * len(hourly_weather),
                                _t=f"{weather_data['location']['name'].upper()}, "
                                   f"{weather_data['location']['country'].upper()}",
                            )
                        with html_doc.tr():
                            for hour in hourly_weather:
                                with html_doc.th(klass="header header_date", colspan=2):
                                    html_doc.span(
                                        _t=f"{datetime.strptime(hour['time'], '%Y-%m-%d %H:%M').time()}"
                                    )
                        with html_doc.tr():
                            for hour in hourly_weather:
                                with html_doc.th(klass="img", colspan=2):
                                    html_doc.img(
                                        src=f"https:{hour['condition']['icon']}",
                                        alt="Forecast weather",
                                    )
                        with html_doc.tr():
                            for hour in hourly_weather:
                                with html_doc.th(klass="condition", colspan=2):
                                    html_doc.span(_t=f"{hour['condition']['text']}")
                        with html_doc.tr():
                            for hour in hourly_weather:
                                with html_doc.th(klass="temp", colspan=2, _t=f"Temp. "):
                                    if user_units == "metric":
                                        param = (
                                            f'{hour["temp_c"]}{metric_units["temp_c"]}'
                                        )
                                    else:
                                        param = (
                                            f'{hour["temp_f"]}{metric_units["temp_f"]}'
                                        )
                                    html_doc.span(_t=param)
                        with html_doc.tr():
                            for hour in hourly_weather:
                                with html_doc.th(
                                        klass="feelslike", colspan=2, _t=f"Min. "
                                ):
                                    if user_units == "metric":
                                        param = f'{hour["feelslike_c"]}{metric_units["temp_c"]}'
                                    else:
                                        param = f'{hour["feelslike_f"]}{metric_units["temp_f"]}'
                                    html_doc.span(_t=param)

                with html_doc.tbody(klass="table_body"):
                    if weather_type == "current":
                        for param in (
                                current_weather_metric
                                if user_units == "metric"
                                else current_weather_am
                        ):
                            with html_doc.tr():
                                if weather[param] is not None:
                                    html_doc.td(_t=f"{row_text.get(param)}")
                                    html_doc.td(
                                        _t=f"{weather[param]}"
                                           f"{metric_units.get(param, '') if user_units == 'metric' else am_units.get(param, '')}"
                                    )
                    elif weather_type == "forecast_daily":
                        for param in (
                                daily_weather_metric
                                if user_units == "metric"
                                else daily_weather_am
                        ):
                            with html_doc.tr():
                                for day in weather_data["forecast"]["forecastday"]:
                                    if day["day"][param] is not None:
                                        html_doc.td(_t=f"{row_text.get(param)}")
                                        html_doc.td(
                                            _t=f"{day['day'][param]}"
                                               f"{metric_units.get(param, '') if user_units == 'metric' else am_units.get(param, '')}"
                                        )
                        for param in astro:
                            with html_doc.tr():
                                for day in weather_data["forecast"]["forecastday"]:
                                    if day["astro"][param] is not None:
                                        html_doc.td(_t=f"{row_text.get(param)}")
                                        html_doc.td(_t=f"{day['astro'][param]}")

                    elif weather_type == "forecast_hourly":
                        for param in (
                                hourly_weather_metric
                                if user_units == "metric"
                                else hourly_weather_am
                        ):
                            with html_doc.tr():
                                for hour in hourly_weather:
                                    if hour[param] is not None:
                                        html_doc.td(_t=f"{row_text.get(param)}")
                                        html_doc.td(
                                            _t=f"{hour[param]}"
                                               f"{metric_units.get(param, '') if user_units == 'metric' else am_units.get(param, '')}"
                                        )

    return str(html_doc)


def parse_date(date: str) -> namedtuple:
    """
    Function. parse date to datetime object
    :param date: date string
    :return: datetime object
    """
    DateParams: namedtuple = namedtuple("date", ["month_date", "week_day", "time"])
    time: str | None = None if len(date.split()) < 2 else date.split()[1]
    date_params: DateParams = DateParams(
        week_day=calendar.day_name[
            datetime.strptime(date.split()[0], "%Y-%m-%d").weekday()
        ],
        month_date=datetime.strptime(date.split()[0], "%Y-%m-%d").day,
        time=time,
    )
    return date_params
