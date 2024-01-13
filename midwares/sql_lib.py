from dataclasses import dataclass


@dataclass
class User:
    table_name: str = 'bot_user'
    user_id: str = 'user_id'
    bot_user: str = 'bot_user'
    user_city: str = 'user_city'
    metric: str = 'metric'
    reply_menu: str = 'reply_menu'

    @classmethod
    def get_user_id(cls, *args) -> str:
        return f"SELECT {cls.bot_user} FROM {cls.table_name} WHERE {cls.bot_user}={args[0]}"


@dataclass(frozen=True)
class Favorite:
    table_name: str = 'favorite_city'
    favorite_user_id: str = 'favorite_user_id'
    user_favorite_city_name: str = 'user_favorite_city_name'


@dataclass(frozen=True)
class Current:
    current_weather_user_id: str = 'current_weather_user_id'
    table_name: str = 'current_weather'
    wind_extended: str = 'wind_extended'
    pressure: str = 'pressure'
    visibility: str = 'visibility'
    humidity: str = 'humidity'


@dataclass(frozen=True)
class Hourly:
    hourly_weather_user_id: str = 'hourly_weather_user_id'
    table_name: str = 'hourly_weather'
    wind_extended: str = 'wind_extended'
    pressure: str = 'pressure'
    visibility: str = 'visibility'
    humidity: str = 'humidity'


@dataclass(frozen=True)
class Daily:
    table_name: str = 'daily_weather'
    daily_weather_user_id: str = 'daily_weather_user_id'
    astro: str = 'astro'
    visibility: str = 'visibility'
    humidity: str = 'humidity'


@dataclass(frozen=True)
class Default:
    table_name: str = 'default_weather'
    default_user_id: str = 'default_user_id'
    current_weather: str = 'current_weather'
    hourly_weather: str = 'hourly_weather'
