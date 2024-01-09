from dataclasses import dataclass, field


@dataclass
class Users:
    from_user_id: int = field(init=True)
    table_name: str = 'users'
    id: str = 'id'
    user_id: str = 'user_id'
    user_city: str = 'user_city'
    metric: str = 'metric'


@dataclass(frozen=True)
class Favorites:
    table_name: str = 'favorites'
    favorites_user_id: str = 'favorites_user_id'
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

