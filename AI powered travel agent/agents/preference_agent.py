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

class PreferenceAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        """Initialize PreferenceAgent with Gemini model"""
        self.model = genai.GenerativeModel(model_name)
        self.preferences = {}

    def collect_preferences(self, name, budget, duration, interests, climate):
        """Store user preferences"""
        self.preferences = {
            "name": name,
            "budget": budget,
            "duration": duration,
            "interests": interests,
            "climate": climate
        }
        console.print(f"[bold green]Preferences saved for {name}![/bold green]")

    def summarize_preferences(self):
        """Return a human-readable summary of preferences"""
        summary = (
            f"Traveler: {self.preferences.get('name', 'N/A')}\n"
            f"Budget: {self.preferences.get('budget', 'N/A')}\n"
            f"Duration: {self.preferences.get('duration', 'N/A')}\n"
            f"Interests: {', '.join(self.preferences.get('interests', []))}\n"
            f"Preferred climate: {self.preferences.get('climate', 'N/A')}"
        )
        return summary

    def generate_travel_plan(self):
        """Generate personalized travel recommendations using Gemini"""
        if not self.preferences:
            console.print("[red]Please collect preferences first![/red]")
            return None

        prompt = (
            f"You are an AI travel planner. Based on the following traveler preferences, "
            f"suggest 3 personalized travel destinations in India with reasons, activities, "
            f"and best visiting times.\n\n"
            f"Traveler Details:\n"
            f"{self.summarize_preferences()}\n\n"
            f"Format your answer with bullet points and clear headings."
        )

        try:
            response = self.model.generate_content(prompt)
            if response and hasattr(response, "text"):
                return response.text
            else:
                return "Sorry, I couldn't generate a travel plan."
        except Exception as e:
            console.print(f"[red]Gemini API Error:[/red] {e}")
            return None
