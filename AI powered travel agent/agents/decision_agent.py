# agents/decision_agent.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console

# Load environment variables
load_dotenv()
console = Console()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


class DecisionAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        """Initialize DecisionAgent with Gemini model"""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        self.model = genai.GenerativeModel(model_name)

    def make_final_decision(self, preferences, research_summaries, weather_data, itineraries):
        """
        Combine data from all agents and recommend the best destination.
        Inputs:
          - preferences: dict from PreferenceAgent
          - research_summaries: list from ResearchAgent
          - weather_data: list of dicts from WeatherAgent
          - itineraries: dict from ItineraryAgent
        """
        # Ensure required data exists
        if not preferences or not research_summaries or not itineraries:
            console.print("[red]Insufficient data! Please run all agents before making a decision.[/red]")
            return None

        # 🧠 Enriched research section
        research_text = "\n".join([
            f"- {r.get('destination', 'N/A')}: {', '.join(r.get('highlights', []))}. "
            f"Best season: {r.get('best_season', 'N/A')}. "
            f"Search Insights: {', '.join(r.get('search_snippets', []))[:200]}... "
            f"Image: {r.get('image_url', 'N/A')}"
            for r in (research_summaries or [])
        ])

        # Build a detailed prompt for Gemini
        prompt = (
            f"You are an expert AI travel assistant. You have the following information:\n\n"
            f"Traveler Preferences:\n"
            f"- Name: {preferences.get('name', 'N/A')}\n"
            f"- Budget: {preferences.get('budget', 'N/A')}\n"
            f"- Duration: {preferences.get('duration', 'N/A')}\n"
            f"- Interests: {', '.join(preferences.get('interests', []))}\n"
            f"- Preferred Climate: {preferences.get('climate', 'N/A')}\n\n"
            
            f"Research Summary of Top Destinations:\n{research_text}\n\n"
            
            f"Weather Reports:\n"
            + "\n".join([
                f"- {w.get('destination', 'N/A')}: {w.get('description', 'N/A')}, "
                f"{w.get('temperature', 'N/A')}°C, humidity {w.get('humidity', 'N/A')}%"
                for w in (weather_data or [])
            ]) + "\n\n"
            
            f"Itineraries:\n"
            + "\n".join([
                f"Destination: {dest}\n{plan}\n"
                for dest, plan in (itineraries or {}).items()
            ]) + "\n\n"
            
            f"Now, based on all this information, recommend the SINGLE best destination for this traveler.\n"
            f"Provide a short reasoning (why it's the best fit), summarize the ideal itinerary, and end with an inspiring travel note."
        )

        try:
            response = self.model.generate_content(prompt)
            if response and hasattr(response, "text"):
                console.print("[bold green]✅ Final decision generated successfully![/bold green]")
                return response.text
            else:
                return "Sorry, I couldn't make a final travel decision."
        except Exception as e:
            console.print(f"[red]Gemini API Error in DecisionAgent:[/red] {e}")
            return None
