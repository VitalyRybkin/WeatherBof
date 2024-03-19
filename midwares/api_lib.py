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
