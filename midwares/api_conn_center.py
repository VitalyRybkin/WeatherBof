import requests
from requests import Response

from data.config import API_TOKEN


def get_current_weather(city_name) -> Response:
    return requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={API_TOKEN}&q={city_name}&aqi=no"
    )


def get_forecast_weather(city_name, days):
    return f"http://api.weatherapi.com/v1/forecast.json?key={API_TOKEN}&q={city_name}&days={days}&aqi=no&alerts=no"
