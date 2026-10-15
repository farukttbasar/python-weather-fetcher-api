import requests
from cli import parse_cli, get_input

ICONS = {
    "☀️": {0},
    "🌤️": {1},
    "⛅": {2},
    "☁️": {3},
    "🌫️": {45, 48},
    "🌦️": {51, 53, 80},
    "🌧️": {55, 61, 63, 65, 81},
    "🌨️": {71},
    "❄️": {73, 75},
    "⛈️": {82, 95, 96}
}

def get_location(city):
    url = 'https://geocoding-api.open-meteo.com/v1/search'
    params = {
        "name": city,
        "count": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return None


    if data and "results" in data and data["results"]:
        result = data["results"][0]
        return {
            "name": result.get("name"),
            "country": result.get("country", ""),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude")
        }
    return None

def get_weather(lat, lon):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        current = response.json().get("current_weather", {})
        return {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "wmo_code": current.get("weathercode")
        }
    except requests.RequestException:
        return None

def get_weather_icon(wmo_code):
    for icon, codes in ICONS.items():
        if wmo_code in codes:
            return icon
    return "❓"

def main():
    args = parse_cli()

    if not args.city:
        args=get_input()
        
    location_data = get_location(args.city)
    if not location_data:
        print("City could not be found")
        return

    weather = get_weather(location_data["latitude"], location_data["longitude"])
    if not weather:
        print("Failed to get the weather data.")
        return

    wmo_code = weather.get("wmo_code")
    icon = get_weather_icon(wmo_code)

    print("=" * 50)
    print(f"📍 Location     : {location_data["name"]}, {location_data["country"]}")
    print(f"ℹ️  Condition    : {icon}")
    print(f"🌡️  Temperature  : {weather["temperature"]} °C")
    print(f"💨 Wind Speed   : {weather["windspeed"]} km/h")
    print("=" * 50)

if __name__ == "__main__":
    main()
    

