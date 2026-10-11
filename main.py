import requests

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

    response = requests.get(url, params=params).json()


    if "results" in response:
        result = response["results"][0]
        return {
            "name": result["name"],
            "country": result["country"],
            "latitude": result["latitude"],
            "longitude": result["longitude"]
        }
    return None

def get_weather(lat, lon):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    response = requests.get(url, params=params).json()
    current_weather = response["current_weather"]
    return {
       "temperature": current_weather["temperature"],
       "windspeed": current_weather["windspeed"],
       "wmo_code": current_weather["weathercode"]
    }

def get_weather_icon(wmo_code):
    for icon, codes in ICONS.items():
        if wmo_code in codes:
            return icon
    return "❓"

def main():
    while True:
        city = input("Enter a city / district name > ").strip().capitalize()
        if city:
           break
        print("Enter a vald location!")
        

    location_data = get_location(city)
    if not location_data:
        print("City could not ne found")
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
    

