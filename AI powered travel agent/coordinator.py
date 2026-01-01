import os
from rich.console import Console
from dotenv import load_dotenv

# Import all agents
from agents.preference_agent import PreferenceAgent
from agents.research_agent import ResearchAgent
from agents.weather_agent import WeatherAgent
from agents.itinerary_agent import ItineraryAgent
from agents.decision_agent import DecisionAgent

# Load environment variables
load_dotenv()
console = Console()


class Coordinator:
    def __init__(self):
        """Initialize all AI agents"""
        self.pref_agent = PreferenceAgent()
        self.research_agent = ResearchAgent()
        self.weather_agent = WeatherAgent()
        self.itinerary_agent = ItineraryAgent()
        self.decision_agent = DecisionAgent()

    def run(self):
        """Command-line workflow (for testing without Streamlit)"""
        console.print("\n[bold cyan]=== AI Travel Assistant Coordinator ===[/bold cyan]")

        # Step 1: Collect user input from console
        name = input("Enter your name: ")
        budget = input("Enter your budget (in USD): ")
        duration = input("Enter trip duration (in days): ")
        interests = input("Enter your interests (comma separated): ").split(",")
        climate = input("Preferred climate (e.g., tropical, cold, pleasant): ")

        result = self.coordinate(name, budget, duration, ",".join(interests), climate)

        if result:
            console.print("\n[bold cyan]=== Final Travel Recommendation ===[/bold cyan]")
            console.print(result["final_decision"])
        else:
            console.print("[red]Could not generate a final travel recommendation.[/red]")

    def coordinate(self, name, budget, duration, interests, climate):
        """
        Main workflow for Streamlit — runs all AI agents to generate a trip plan.
        Returns both the final decision and detailed research data (with images).
        """
        console.print("\n[bold cyan]=== AI Travel Assistant Coordinator ===[/bold cyan]")

        # Step 1: Collect preferences
        self.pref_agent.collect_preferences(
            name, budget, duration, [i.strip() for i in interests.split(",")], climate
        )
        console.print("[green]User preferences collected.[/green]")

        # Step 2: Research destinations
        console.print("[yellow]Researching best destinations...[/yellow]")
        research_data = self.research_agent.gather_research(self.pref_agent.preferences)
        console.print("[green]Research data ready.[/green]")

        # Step 3: Fetch weather data
        console.print("[yellow]Fetching weather information...[/yellow]")
        weather_data = self.weather_agent.get_weather_for_all(research_data)
        console.print("[green]Weather data fetched.[/green]")

        # Step 4: Create itineraries
        console.print("[yellow]Generating itineraries for destinations...[/yellow]")
        itineraries = {}
        for dest in research_data:
            dest_name = dest.get("destination")
            if dest_name:
                weather_info = next(
                    (w for w in weather_data if w.get("destination") == dest_name), {}
                )
                itinerary = self.itinerary_agent.create_itinerary(
                    dest, self.pref_agent.preferences, weather_info
                )
                itineraries[dest_name] = itinerary
        console.print("[green]Itineraries created successfully.[/green]")

        # Step 5: Make final decision
        console.print("[yellow]Making final travel recommendation...[/yellow]")
        final_decision = self.decision_agent.make_final_decision(
            self.pref_agent.preferences, research_data, weather_data, itineraries
        )

        # ✅ Return everything (for Streamlit display)
        return {
            "final_decision": final_decision,
            "research_data": research_data,
            "weather_data": weather_data,
            "itineraries": itineraries
        }


def main():
    """Allows command-line testing"""
    coordinator = Coordinator()
    coordinator.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user.[/yellow]")
