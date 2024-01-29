
import weather from "/html/current_weather.json" assert {type: 'json'};
console.log(weather)
var weather_dict = weather[0]

const outputDict = {
    "name": "Location name:",
    "region": "Region:",
    "country": "Country:",
    "lat": "Latitude:",
    "lon": "Longitude:",
    "localtime": "Local time:",
    "last_updated": "Last updated:",
    "condition": "Conditions:",
    "cloud": "Clouds:",
    "humidity": "Humidity:",
    "wind_dir": "Wind direction:",
    "temp_c": "Temperature:",
    "feelslike_c": "Feels like temperature:",
    "wind_kph": "Wind:",
    "precip_mm": "Precipitations:",
    "pressure_mb": "Pressure:",
    "vis_km": "Visibility:",
    "gust_kph": "Wind gust:"
}

const headerAddText = document.querySelector(".header")
headerAddText.textContent = `Last updated: ${weather_dict["last_updated"]}`

const tableToAdd = document.querySelector(".table_body")
for (let [key, value] of Object.entries(weather_dict)) {
    // console.log(`${key}=${value}`);
    if (!value == null || !value == ""){
    var newRow = tableToAdd.insertRow()
    var newCell = newRow.insertCell()
    var newText = document.createTextNode(`${outputDict[key]}`);
    newCell.appendChild(newText);
    newCell = newRow.insertCell()
    newText = document.createTextNode(`${value}`);
    newCell.appendChild(newText);}
  }