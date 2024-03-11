from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """
    Class. User table dataclass. User favorite location, units, bottom menu on/off.
    """

    table_name: str = "bot_user"
    user_id: str = "user_id"  # TODO change to city_id
    bot_user_id: str = "bot_user_id"
    id: str = "id"
    name: str = "name"
    region: str = "region"
    country: str = "country"
    metric: str = "metric"
    reply_menu: str = "reply_menu"

    @classmethod
    def get_user_id(cls, *args) -> str:
        return (
            f"SELECT {cls.user_id} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.bot_user_id}={args[0]}"
        )

    @classmethod
    def get_user_config(cls, *args):
        return (
            f"SELECT {cls.metric}, {cls.reply_menu} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.bot_user_id}={args[0]}"
        )

    @classmethod
    def get_user_location_info(cls, **kwargs):
        return (
            f"SELECT {cls.id}, {cls.name}, {cls.region}, {cls.country} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.bot_user_id}={kwargs['bot_user_id']}"
        )


@dataclass(frozen=True)
class Wishlist:
    """
    Class. Favorite table dataclass. User favorite locations wishlist.
    """

    table_name: str = "wishlist"
    wishlist_user_id: str = "wishlist_user_id"
    id: str = "id"
    name: str = "name"
    region: str = "region"
    country: str = "country"

    @classmethod
    def get_wishlist_loc(cls, **kwargs):
        return (
            f"SELECT {cls.id}, {cls.name}, {cls.region}, {cls.country} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.wishlist_user_id}=({User.get_user_id(kwargs['user_id'])}) "
            f"AND {cls.id}={kwargs['loc_id']}"
        )


@dataclass(frozen=True)
class Current:
    """
    Class. Current weather table dataclass. Current weather display settings.
    """

    current_weather_user_id: str = "current_weather_user_id"
    table_name: str = "current_weather"
    wind_extended: str = "wind_extended"
    pressure: str = "pressure"
    visibility: str = "visibility"
    humidity: str = "humidity"

    @classmethod
    def get_user_current_weather_settings(cls, **kwargs):
        return (
            f"SELECT {cls.wind_extended}, {cls.pressure}, {cls.visibility}, {cls.humidity} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.current_weather_user_id}=({User.get_user_id(kwargs['bot_user_id'])})"
        )


@dataclass(frozen=True)
class Hourly:
    """
    Class. Hourly weather table dataclass. Hourly weather display settings.
    """

    hourly_weather_user_id: str = "hourly_weather_user_id"
    table_name: str = "hourly_weather"
    wind_extended: str = "wind_extended"
    pressure: str = "pressure"
    visibility: str = "visibility"
    humidity: str = "humidity"

    @classmethod
    def get_hourly_settings(cls, **kwargs):
        return (
            f"SELECT {cls.wind_extended}, {cls.pressure}, {cls.visibility}, {cls.humidity} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.hourly_weather_user_id}=({User.get_user_id(kwargs['bot_user_id'])})"
        )


@dataclass(frozen=True)
class Daily:
    """
    Class. Daily weather table dataclass. Daily weather display settings.
    """

    table_name: str = "daily_weather"
    daily_weather_user_id: str = "daily_weather_user_id"
    astro: str = "astro"
    visibility: str = "visibility"
    humidity: str = "humidity"

    @classmethod
    def get_daily_settings(cls, **kwargs):
        return (
            f"SELECT {cls.astro}, {cls.visibility}, {cls.humidity} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.daily_weather_user_id}=({User.get_user_id(kwargs['bot_user_id'])})"
        )


@dataclass(frozen=True)
class Default:
    """
    Class. Default user settings table dataclass.
    Current weather display on/off.
    Hourly weather forecast (1 to 12 hours).
    Daily weather forecast (1 to 3 days).
    """

    table_name: str = "default_weather"
    default_user_id: str = "default_user_id"
    current_weather: str = "current_weather"
    hourly_weather: str = "hourly_weather"
    daily_weather: str = "daily_weather"

    @classmethod
    def get_default_settings(cls, *args):
        return (
            f"SELECT {cls.current_weather}, {cls.hourly_weather}, {cls.daily_weather} "
            f"FROM {cls.table_name} "
            f"WHERE {cls.default_user_id}={args[0]}"
        )
