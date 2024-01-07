from dataclasses import dataclass


@dataclass
class Users:
    table_name: str = 'users'
    id: str = 'id'
    user_id: str = 'user_id'
    user_city: str = 'user_city'
    metric: str = 'metric'


@dataclass
class Favorites:
    table_name: str = 'favorites'
    favorites_user_id: str = 'favorites_user_id'
    user_favorite_city_name: str = 'user_favorite_city_name'


@dataclass
class Current:
    current_weather_user_id: str = 'current_weather_user_id'
    table_name: str = 'current_weather'
    wind_extended: str = 'wind_extended'
    pressure: str = 'pressure'
    visibility: str = 'visibility'
    humidity: str = 'humidity'


@dataclass
class Hourly:
    hourly_weather_user_id: str = 'hourly_weather_user_id'
    table_name: str = 'hourly_weather'
    wind_extended: str = 'wind_extended'
    pressure: str = 'pressure'
    visibility: str = 'visibility'
    humidity: str = 'humidity'


@dataclass
class Daily:
    daily_weather_user_id: str = 'daily_weather_user_id'
    astro: str = 'astro'
    visibility: str = 'visibility'
    humidity: str = 'humidity'

