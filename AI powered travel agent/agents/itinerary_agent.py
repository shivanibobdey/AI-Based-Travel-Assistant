import google.generativeai as genai
from dotenv import load_dotenv
import os
from rich.console import Console

# Load environment variables
load_dotenv()
console = Console()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class ItineraryAgent:
    def __init__(self, model_name="models/gemini-2.0-flash"):
        """Initialize ItineraryAgent with Gemini model"""
        self.model = genai.GenerativeModel(model_name)

    def create_itinerary(self, destination, preferences, weather_data):
        """Generate a day-by-day itinerary based on destination, user preferences, and weather"""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in .env file.")

        prompt = (
            f"You are an AI travel itinerary planner. Based on the following details, "
            f"create a detailed day-by-day travel itinerary (5 days max) for the traveler.\n\n"
            f"Destination: {destination.get('destination', 'Unknown')}\n"
            f"Weather: {weather_data.get('description', 'N/A')}, {weather_data.get('temperature', 'N/A')}°C\n"
            f"Traveler Preferences:\n"
            f"- Budget: {preferences.get('budget', 'N/A')}\n"
            f"- Interests: {', '.join(preferences.get('interests', []))}\n"
            f"- Climate preference: {preferences.get('climate', 'N/A')}\n"
            f"- Duration: {preferences.get('duration', 'N/A')}\n\n"
            f"Format: Day-wise plan with key activities, food spots, and local tips."
        )

        try:
            response = self.model.generate_content(prompt)
            if response and hasattr(response, "text"):
                return response.text.strip()
            else:
                return "Sorry, I couldn't generate an itinerary."
        except Exception as e:
            console.print(f"[red]Gemini API Error:[/red] {e}")
            return None
