import os
import requests
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables
load_dotenv()
console = Console()

# Get API keys
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

# -------- API Helper Functions -------- #

def search_places(query):
    """Search destinations using Serper API."""
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        results = [r["title"] for r in data.get("organic", [])[:5]]
        return results
    except Exception as e:
        console.print(f"[red]Serper API Error:[/red] {e}")
        return []

def get_weather(city):
    """Fetch weather details for a city."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200 or "main" not in data:
            console.print(f"[red]Weather not found for {city}[/red]")
            return None

        return {
            "temp": data["main"]["temp"],
            "desc": data["weather"][0]["description"].capitalize(),
        }

    except Exception as e:
        console.print(f"[red]Weather API Error:[/red] {e}")
        return None


def get_image_url(destination):
    """Fetch a beautiful image for the destination."""
    try:
        url = f"https://api.unsplash.com/search/photos?page=1&query={destination}&client_id={UNSPLASH_ACCESS_KEY}"
        response = requests.get(url)
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]
        return None
    except Exception as e:
        console.print(f"[red]Unsplash API Error:[/red] {e}")
        return None
    
def query_gemini(prompt):
    """Query Gemini model for AI-generated text."""
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-2.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        console.print(f"[red]Gemini API Error:[/red] {e}")
        return "Sorry, I couldn't generate a response."

