from dataclasses import dataclass


@dataclass(frozen=True)
class LocationInfo:
    name: str
    region: str
    country: str
    lat: str
    lon: str
    localtime: str


# TODO detach LocationInfo

@dataclass(frozen=True)
class BasicWeather(LocationInfo):
    last_updated: str
    condition: str
    cloud: str
    humidity: str
    wind_dir: str


@dataclass(frozen=True)
class CurrentMetric(BasicWeather):
    temp_c: str
    feelslike_c: str
    wind_kph: str
    precip_mm: str
    pressure_mb: str
    vis_km: str
    gust_kph: str

    def __repr__(self):
        weather_text = (f"{'Last updated:':>18} - \U0001F5D3 {self.last_updated}\n"
                        f"{'Condition:':>18} - {self.condition}\n"
                        f"{'Cloud:': >18} - {self.cloud}%\n")

        if self.humidity is not None:
            weather_text += f"{'Humidity:':>18} - {self.humidity}%\n"

        weather_text += (f"{'Temperature:':>18} - {self.temp_c}\U00002103\n"
                         f"{'Feels like:':>18} - {self.feelslike_c}\U00002103\n"
                         f"{'Precipitations:':>18} - {self.precip_mm} mm\n"
                         f"{'Wind:':>18} - {self.wind_kph} kph\n")

        if self.wind_dir is not None:
            weather_text += f"{'Wind direction:':>18} - {self.wind_dir}\n"
        if self.gust_kph is not None:
            weather_text += f"{'Wind gust:':>18} - {self.gust_kph} kph\n"
        if self.pressure_mb is not None:
            weather_text += f"{'Pressure:':>18} - {self.pressure_mb} mb\n"
        if self.vis_km is not None:
            weather_text += f"{'Visibility:':>18} - {self.vis_km} km\n"

        return f"<pre>{weather_text}</pre>"


@dataclass(frozen=True)
class CurrentAmerican(BasicWeather):
    temp_f: str
    feelslike_f: str
    wind_mph: str
    cloud: str
    precip_in: str
    pressure_in: str
    vis_miles: str
    gust_mph: str
