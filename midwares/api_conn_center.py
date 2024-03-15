import calendar
from collections import namedtuple

from airium import Airium
from datetime import datetime
from icecream import ic
from data import globals

import requests
from htmlwebshot import WebShot, Config
from requests import Response
from typing_extensions import Union

from data.config import API_TOKEN
from midwares.api_lib import (
    MetricForecastWeather,
    AmericanForecastWeather,
    loc_params,
    current_weather_metric,
    current_weather_am,
    row_text,
    metric_units, am_units, LocationInfo
)
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Current, User, Daily, Hourly


def api_search_location(loc_name) -> Response:
    return requests.get(
        f"https://api.weatherapi.com/v1/search.json?key={API_TOKEN}&q={loc_name}&aqi=no"
    )


def get_current_weather(loc_id, bot_user_id) -> str:
    get_user_settings = read_data_row(
        Current.get_user_current_weather_settings(bot_user_id=bot_user_id)
    )[0]
    get_user_units = read_data_row(User.get_user_config(bot_user_id))[0]
    current_weather: dict = requests.get(
        f"https://api.weatherapi.com/v1/current.json?key={API_TOKEN}&q=id:{loc_id}&aqi=no"
    ).json()

    for (key, val) in get_user_settings.items():
        if key == 'humidity' and val == 0:
            current_weather["current"]["humidity"] = None
        if key == 'pressure' and val == 0:
            current_weather["current"]["pressure_in"] = None
            current_weather["current"]["pressure_mb"] = None
        if key == 'visibility' and val == 0:
            current_weather["current"]["vis_km"] = None
            current_weather["current"]["vis_miles"] = None
        if key == 'wind_extended' and val == 0:
            current_weather["current"]["gust_kph"] = None
            current_weather["current"]["gust_mph"] = None

    html_file: str = create_html(current_weather, get_user_units["metric"], weather_type="current")
    with open("./html/weather.html", "w") as weather:
        weather.write(html_file)

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
    # get_hourly_settings: dict = read_data_row(
    #     Hourly.get_hourly_settings(bot_user_id=bot_user_id)
    # )[0]
    get_user_units: dict = read_data_row(User.get_user_config(bot_user_id))[0]
    forecast_weather: dict = requests.get(
        f"https://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q=id:{loc_id}&days={days}&aqi=no&alerts=no"
    ).json()
    ic(forecast_weather)

    loc_info = LocationInfo(
        name=forecast_weather["location"]["name"],
        region=forecast_weather["location"]["region"],
        country=forecast_weather["location"]["country"],
        lat=forecast_weather["location"]["lat"],
        lon=forecast_weather["location"]["lon"],
        localtime=forecast_weather["location"]["localtime"],
    )

    day_forecast_list: list[MetricForecastWeather | AmericanForecastWeather] = []
    for date in forecast_weather["forecast"]["forecastday"]:
        if get_user_units["metric"] == "metric":
            parse_loc_weather = MetricForecastWeather(
                date=date["date"],
                avghumidity=(
                    date["day"]["avghumidity"]
                    if bool(get_daily_settings["humidity"])
                    else None
                ),
                daily_chance_of_rain=date["day"]["daily_chance_of_rain"],
                daily_chance_of_snow=date["day"]["daily_chance_of_snow"],
                condition=date["day"]["condition"]["text"],
                icon=date["day"]["condition"]["icon"],
                sunrise=(
                    date["astro"]["sunrise"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                sunset=(
                    date["astro"]["sunset"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moonrise=(
                    date["astro"]["moonrise"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moonset=(
                    date["astro"]["moonset"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moon_phase=(
                    date["astro"]["moon_phase"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                maxtemp_c=f'{date["day"]["maxtemp_c"]}{globals.metric_units["degrees"] if get_user_units["metric"] == "metric" else globals.am_units["degrees"]}',
                mintemp_c=date["day"]["mintemp_c"],
                avgtemp_c=date["day"]["avgtemp_c"],
                maxwind_kph=date["day"]["maxwind_kph"],
                totalprecip_mm=date["day"]["totalprecip_mm"],
                avgvis_km=(
                    date["day"]["avgvis_km"]
                    if bool(get_daily_settings["visibility"])
                    else None
                ),
            )
        else:
            parse_loc_weather = AmericanForecastWeather(
                date=date["date"],
                avghumidity=(
                    date["day"]["avghumidity"]
                    if bool(get_daily_settings["humidity"])
                    else None
                ),
                daily_chance_of_rain=date["day"]["daily_chance_of_rain"],
                daily_chance_of_snow=date["day"]["daily_chance_of_snow"],
                condition=date["day"]["condition"]["text"],
                icon=date["day"]["condition"]["icon"],
                sunrise=(
                    date["astro"]["sunrise"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                sunset=(
                    date["astro"]["sunset"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moonrise=(
                    date["astro"]["moonrise"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moonset=(
                    date["astro"]["moonset"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                moon_phase=(
                    date["astro"]["moon_phase"]
                    if bool(get_daily_settings["astro"])
                    else None
                ),
                maxtemp_f=date["day"]["maxtemp_f"],
                mintemp_f=date["day"]["mintemp_f"],
                avgtemp_f=date["day"]["avgtemp_f"],
                maxwind_mph=date["day"]["maxwind_mph"],
                totalprecip_in=date["day"]["totalprecip_in"],
                avgvis_miles=(
                    date["day"]["avgvis_miles"]
                    if bool(get_daily_settings["visibility"])
                    else None
                ),
            )
        day_forecast_list.append(parse_loc_weather)

    html_file: str = create_html(day_forecast_list, loc_info, weather_type="forecast")

    with open("./html/weather.html", "w") as weather:
        weather.write(html_file)

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
    shot.params = {"--crop-w": 315 * len(day_forecast_list)}
    shot.delay = 3
    weather_pic = shot.create_pic(
        html="./html/weather.html",
        css="./html/current_weather_style.css",
        output="./html/weather_pic.jpg",
    )

    return weather_pic


def create_html(
        weather_data,
        user_units,
        weather_type: str,
) -> str:
    weather = weather_data['current']
    location = weather_data['location']

    html_doc = Airium()

    html_doc('<!DOCTYPE html>')
    with html_doc.html(lang="en"):
        with html_doc.head():
            html_doc.meta(content='text/html', charset='utf-8')
            html_doc.meta(content='width=device-width, initial-scale=1', name='viewport')
            html_doc.link(href='https://fonts.googleapis.com/css2?family=Protest'
                               '+Riot&display=swap', rel="stylesheet")
            html_doc.link(href='./current_weather_style.css', rel='stylesheet')
            html_doc.title(_t="Current weather")

        with html_doc.body():
            table_width = "300px" if weather_type == "current" else f"{300}px"
            with html_doc.table(style=f"width:{table_width};"):
                if weather_type == "current":
                    with html_doc.thead():
                        with html_doc.tr():
                            html_doc.th(klass="header header_loc",
                                        colspan=2,
                                        _t=f'{location["name"].upper()}, '
                                           f'{location["country"].upper()}')
                        with html_doc.tr():
                            with html_doc.th(klass="header header_date", colspan=2):
                                html_doc.span(_t=f'{parse_date(weather["last_updated"]).week_day}, '
                                                 f'{parse_date(weather["last_updated"]).month_date},'
                                                 f' {parse_date(weather["last_updated"]).time}')
                        with html_doc.tr():
                            with html_doc.th(klass="img", colspan=2):
                                html_doc.img(src=f'https:{weather["condition"]["icon"]}',
                                             alt='Current weather')
                        with html_doc.tr():
                            with html_doc.th(klass="condition", colspan=2):
                                html_doc.span(_t=f'{weather["condition"]["text"]}')
                        with html_doc.tr():
                            with html_doc.th(klass="temp", colspan=2, _t="Temperature: "):
                                if user_units == "metric":
                                    param = f'{weather["temp_c"]}{metric_units["temp_c"]}'
                                else:
                                    param = f'{weather["temp_f"]}{metric_units["temp_f"]}'
                                html_doc.span(_t=param)
                        with html_doc.tr():
                            with html_doc.th(klass="feelslike", colspan=2, _t="Feels like: "):
                                if user_units == "metric":
                                    param = f'{weather["feelslike_c"]}{metric_units["feelslike_c"]}'
                                else:
                                    param = f'{weather["feelslike_f"]}{metric_units["feelslike_f"]}'
                                html_doc.span(_t=param)

                elif weather_type == "forecast":
                    # with html_doc.thead():
                    #     with html_doc.tr():
                    #         html_doc.th(klass="header header_loc",
                    #                     colspan=2 * len(parse_loc_weather),
                    #                     _t=f"{loc_info.name.upper()}, {loc_info.country.upper()}")
                    #     with html_doc.tr():
                    #         for day in parse_loc_weather:
                    #             with html_doc.th(klass="header header_date", colspan=2):
                    #                 week_day = calendar.day_name[
                    #                     datetime.strptime(day.date.split()[0],
                    #                                       "%Y-%m-%d").weekday()]
                    #                 month_date = datetime.strptime(day.date.split()[0],
                    #                                                "%Y-%m-%d").day
                    #                 html_doc.span(_t=f"{parse_date(day.date).week_day}, "
                    #                                  f"{parse_date(day.date).month_date},")
                    #     with html_doc.tr():
                    #         for day in parse_loc_weather:
                    #             with html_doc.th(klass="img", colspan=2):
                    #                 html_doc.img(src=f"https:{day.icon}",
                    #                              alt="Forecast weather")
                    #     with html_doc.tr():
                    #         for day in parse_loc_weather:
                    #             with html_doc.th(klass="condition", colspan=2):
                    #                 html_doc.span(_t=f"{day.condition}")
                    #     with html_doc.tr():
                    #         for day in parse_loc_weather:
                    #             with html_doc.th(klass="temp", colspan=2, _t=f"Max temp."):
                    #                 html_doc.span(_t=f"{day.maxtemp_c}")
                    ...

                    # table_rows = "<th class ='header'> </th>"
                    #
                    # for week_day, month_date in weekdays:
                    #     table_rows += f"<th class ='header'> {week_day}, {month_date} </th>"
                    #
                    # table_head = (
                    #     f"\t<thead>\n"
                    #     f"\t\t<tr>\n"
                    #     f'\t\t\t<th colspan="{len(weekdays) + 1}" class="header">{loc_info.name}, {loc_info.country}</th>\n'
                    #     f"\t\t</tr>\n"
                    #     f"\t\t<tr>\n"
                    #     f'\t\t\t<th colspan="{len(weekdays) + 1}" class="header"><span>{week_day}, {month_date}, {time}</span></th>\n'
                    #     f"\t\t</tr>\n"
                    #     f"\t\t<tr>\n"
                    #     f"\t\t\t{table_rows}\n"
                    #     f"\t\t</tr>\n"
                    #     f"\t</thead>\n"
                    # )
                    pass

                if isinstance(None, list):
                    # counter = 0
                    # while counter < len(parse_loc_weather[0].get_rows):
                    #     table_body += "\n\t\t<tr>"
                    #     for i in range(len(parse_loc_weather)):
                    #         if parse_loc_weather[i].get_data[counter] == "":
                    #             continue
                    #         if i == 0:
                    #             table_body += f"\n\t\t\t<td>{parse_loc_weather[i].get_rows[counter]}</td><td>{parse_loc_weather[i].get_data[counter]}</td>"
                    #         else:
                    #             table_body += f"<td>{parse_loc_weather[i].get_data[counter]}</td>"
                    #     counter += 1
                    #     table_body += "\n\t\t</tr>"
                    # table_body += f"\t</tbody>\n"
                    pass
                else:
                    with html_doc.tbody(klass="table_body"):
                        for param in current_weather_metric if user_units == 'metric' else current_weather_am:
                            with html_doc.tr():
                                if weather[param] is not None:
                                    html_doc.td(_t=f"{row_text.get(param)}")
                                    html_doc.td(_t=f"{weather[param]}"
                                                   f"{metric_units.get(param, '') if user_units == 'metric' else am_units.get(param, '')}")

    return str(html_doc)


def parse_date(date):
    DateParams: namedtuple = namedtuple('date', ['month_date', 'week_day', 'time'])
    date_params = DateParams(
        week_day=calendar.day_name[
            datetime.strptime(
                date.split()[0], "%Y-%m-%d"
            ).weekday()
        ],
        month_date=datetime.strptime(
            date.split()[0], "%Y-%m-%d"
        ).day,
        time=date.split()[1]
    )
    return date_params
