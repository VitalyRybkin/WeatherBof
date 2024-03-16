from collections import namedtuple
from dataclasses import dataclass


@dataclass(frozen=True)
class LocationInfo:
    name: str
    region: str
    country: str
    lat: str
    lon: str
    localtime: str


@dataclass(frozen=True)
class BasicCurrentWeather:
    last_updated: str
    condition: str
    cloud: str
    humidity: str
    wind_dir: str
    icon: str


@dataclass(frozen=True)
class CurrentMetric(BasicCurrentWeather):
    temp_c: str
    feelslike_c: str
    wind_kph: str
    precip_mm: str
    pressure_mb: str
    vis_km: str
    gust_kph: str

    @property
    def get_weather(self):
        """
        Function. Returns the current metric units weather
        """
        data_dict: dict[str, str] = {
            "Condition:": f"{self.condition}",
            "Cloud:": f"{self.cloud}%",
            "Humidity:": f"{self.humidity}%",
            "Temperature:": f" {self.temp_c} C",
            "Feels like:": f" {self.feelslike_c} C",
            "Precipitations:": f"{self.precip_mm} mm",
            "Wind:": f"{self.wind_kph} kph",
            "Wind direction:": f"{self.wind_dir}",
            "Wind gust:": f"{self.gust_kph} kph",
            "Pressure:": f"{self.pressure_mb} mb",
            "Visibility:": f"{self.vis_km} km",
            "Icon": f"{self.icon}",
        }
        return data_dict


@dataclass(frozen=True)
class CurrentAmerican(BasicCurrentWeather):
    """
    Function. Returns the current am units weather
    """

    temp_f: str
    feelslike_f: str
    wind_mph: str
    cloud: str
    precip_in: str
    pressure_in: str
    vis_miles: str
    gust_mph: str

    def get_weather(self):
        data_dict: dict[str, str] = {
            "Condition": f"{self.condition}",
            "Cloud:": f"{self.cloud}%",
            "Humidity:": f"{self.humidity}%",
            "Temperature": f" {self.temp_f} F",
            "Feels like": f" {self.feelslike_f} F",
            "Precipitations:": f"{self.precip_in} in",
            "Wind:": f"{self.wind_mph} mph",
            "Wind direction:": f"{self.wind_dir}",
            "Wind gust:": f"{self.gust_mph} mph",
            "Pressure:": f"{self.pressure_in} in",
            "Visibility:": f"{self.vis_miles} miles",
            "Icon": f"{self.icon}",
        }
        return data_dict


@dataclass(frozen=True)
class BasicForecastWeather:
    date: str
    avghumidity: str
    daily_chance_of_rain: str
    daily_chance_of_snow: str
    condition: str
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    icon: str


@dataclass(frozen=True)
class MetricForecastWeather(BasicForecastWeather):
    maxtemp_c: str
    mintemp_c: str
    avgtemp_c: str
    maxwind_kph: str
    totalprecip_mm: str
    avgvis_km: str

    @property
    def get_rows(self) -> list:
        return [
            "Max temp:",
            "Min temp:",
            "Average temp:",
            "Max wind:",
            "Total precipitations:",
            "Condition:",
            "Chance of rain:",
            "Chance of snow:",
            "Average humidity:",
            "Average visibility:",
        ]

    @property
    def get_data(self) -> list:
        return [
            f"Max temp: {self.maxtemp_c}°C",
            f"{self.mintemp_c}°C",
            f"{self.avgtemp_c}°C",
            f"{self.maxwind_kph} kph",
            f"{self.totalprecip_mm} mm",
            f"{self.condition}",
            f"{self.daily_chance_of_rain}%",
            f"{self.daily_chance_of_snow}%",
            f'{f"{self.avghumidity}%" if self.avghumidity is not None else ""}',
            f'{f"{self.avgvis_km} km" if self.avgvis_km is not None else ""}',
        ]


@dataclass(frozen=True)
class AmericanForecastWeather(BasicForecastWeather):
    maxtemp_f: str
    mintemp_f: str
    avgtemp_f: str
    maxwind_mph: str
    totalprecip_in: str
    avgvis_miles: str

    @property
    def get_rows(self) -> list:
        return [
            "Max temp:",
            "Min temp:",
            "Average temp:",
            "Max wind:",
            "Total precipitations:",
            "Condition:",
            "Chance of rain:",
            "Chance of snow:",
            "Average humidity:",
            "Average visibility:",
        ]

    @property
    def get_data(self) -> list:
        return [
            f"Max temp: {self.maxtemp_f}°F",
            f"{self.mintemp_f}°F",
            f"{self.avgtemp_f}°F",
            f"{self.maxwind_mph} mph",
            f"{self.totalprecip_in} in",
            f"{self.condition}",
            f"{self.daily_chance_of_rain}%",
            f"{self.daily_chance_of_snow}%",
            f'{f"{self.avghumidity}%" if self.avghumidity is not None else ""}',
            f'{f"{self.avgvis_miles} miles" if self.avgvis_miles is not None else ""}',
        ]


row_text: dict[str, str] = {
    "cloud": "Clouds: ",
    "humidity": "Humidity: ",
    "avghumidity": "Ave. humidity: ",
    "wind_dir": "Wind direction: ",
    "temp_c": "Temperature: ",
    "avgtemp_c": "Ave. temperature: ",
    "temp_f": "Temperature: ",
    "avgtemp_f": "Ave. temperature: ",
    "feelslike_c": "Feels like: ",
    "feelslike_f": "Feels like: ",
    "wind_kph": "Wind: ",
    "maxwind_kph": "Max. wind: ",
    "maxwind_mph": "Max. wind: ",
    "wind_mph": "Wind: ",
    "precip_mm": "Precipitation: ",
    "totalprecip_mm": "Total precipitation: ",
    "precip_in": "Precipitation: ",
    "totalprecip_in": "Total precipitation: ",
    "pressure_mb": "Pressure: ",
    "vis_km": "Visibility: ",
    "avgvis_km": "Ave. visibility: ",
    "vis_miles": "Visibility: ",
    "avgvis_miles": "Ave. vVisibility: ",
    "gust_kph": "Gust: ",
    "gust_mph": "Gust: ",
    "daily_chance_of_rain": "Chance of rain: ",
    "daily_chance_of_snow": "Chance of snow: ",
    "moon_phase": "Moon phase: ",
    "moonrise": "Moonrise: ",
    "moonset": "Moonset: ",
    "sunrise": "Sunrise: ",
    "sunset": "Sunset: ",
}

loc_params: list[str] = [
    "name",
    "region",
    "country",
    "lat",
    "lon",
    "localtime",
]

astro = [
    "moonrise",
    "moonset",
    "sunrise",
    "sunset",
    "moon_phase",
]

metric_units: dict[str, str] = {
    "feelslike_c": "C",
    "temp_c": "C",
    "avgtemp_c": "C",
    "gust_kph": " kph",
    "wind_kph": " kph",
    "maxwind_kph": " kph",
    "precip_mm": " mm",
    "totalprecip_mm": " mm",
    "pressure_mb": " mb",
    "vis_km": " km",
    "avgvis_km": " km",
    "humidity": "%",
    "avghumidity": "%",
    "cloud": "%",
    "daily_chance_of_rain": "%",
    "daily_chance_of_snow": "%",
}

am_units: dict[str, str] = {
    "feelslike_f": "F",
    "temp_f": "F",
    "gust_mph": " mph",
    "wind_mph": " mph",
    "precip_in": " in",
    "pressure_in": " in",
    "vis_miles": " miles",
    "humidity": "%",
    "cloud": "%",
}

current_weather_metric: list[str] = [
    "cloud",
    "humidity",
    "wind_dir",
    "wind_kph",
    "precip_mm",
    "pressure_mb",
    "vis_km",
    "gust_kph",
]

current_weather_am: list[str] = [
    "cloud",
    "humidity",
    "wind_dir",
    "wind_mph",
    "precip_in",
    "pressure_in",
    "vis_miles",
    "gust_mph",
]

daily_weather_metric: list[str] = [
    "avgtemp_c",
    "maxwind_kph",
    "totalprecip_mm",
    "avghumidity",
    "avgvis_km",
    "daily_chance_of_rain",
    "daily_chance_of_snow",
]

daily_weather_am: list[str] = [
    "avgtemp_f",
    "maxwind_mph",
    "totalprecip_in",
    "avghumidity",
    "avgvis_miles",
    "daily_chance_of_rain",
    "daily_chance_of_snow",
]
