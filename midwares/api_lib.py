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
            "Condition:": f'{self.condition}',
            "Cloud:": f'{self.cloud}%',
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
            "Condition": f'{self.condition}',
            "Cloud:": f'{self.cloud}%',
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
            f"{self.maxtemp_c}°C",
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
            f"{self.maxtemp_f}°F",
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
