import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherAgent:
    def __init__(self):
        if not OPENWEATHER_API_KEY:
            raise ValueError("OpenWeather API key not found. Please set it in the .env file.")

    def get_weather(self, destination):
        """Fetch current weather for a given destination using OpenWeatherMap."""
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": destination,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                weather_info = {
                    "destination": destination,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
                return weather_info
            else:
                return {"destination": destination, "error": data.get("message", "Weather data not found")}
        except Exception as e:
            return {"destination": destination, "error": str(e)}

    def get_weather_for_all(self, destinations):
        """Fetch weather for multiple destinations."""
        results = []
        for place in destinations:
            dest_name = place.get("destination")
            if dest_name:
                weather = self.get_weather(dest_name)
                results.append(weather)
        return results
