# agents/research_agent.py
import os
import json
from dotenv import load_dotenv
from rich.console import Console
import google.generativeai as genai
from utils import search_places, get_image_url  # ✅ new imports

load_dotenv()
console = Console()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    console.print("[yellow]Warning: GEMINI_API_KEY not found — using fallback results.[/yellow]")


class ResearchAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        self.model_name = model_name
        self.fallback = [
            {"destination": "Goa, India", "highlights": ["Beaches", "Water sports", "Nightlife"], "hotel_cost_usd": 30, "best_season": "Nov-Feb"},
            {"destination": "Manali, India", "highlights": ["Himalayan views", "Trekking", "River rafting"], "hotel_cost_usd": 25, "best_season": "May-Jun, Sep-Oct"},
            {"destination": "Sikkim, India", "highlights": ["Monasteries", "Snow peaks", "Adventure"], "hotel_cost_usd": 35, "best_season": "Mar-May, Sep-Dec"}
        ]

    def _build_prompt(self, preferences: dict) -> str:
        return (
            "You are a travel researcher. Based on these preferences, "
            "suggest 3 suitable travel destinations in India. "
            "For each, return a JSON object with: destination, highlights, hotel_cost_usd, and best_season.\n\n"
            f"Preferences:\n{json.dumps(preferences, indent=2)}\n"
            "Return only JSON (a list of objects)."
        )

    def gather_research(self, preferences: dict, use_llm=True):
        if not GEMINI_API_KEY or not use_llm:
            console.print("[yellow]Using fallback data (no Gemini key or LLM disabled).[/yellow]")
            data = self.fallback
        else:
            prompt = self._build_prompt(preferences)
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                text = response.text.strip()

                # Parse JSON safely
                start, end = text.find("["), text.rfind("]") + 1
                snippet = text[start:end] if start != -1 and end > start else None
                data = json.loads(snippet) if snippet else self.fallback
            except Exception as e:
                console.print(f"[red]Gemini error in ResearchAgent:[/red] {e}")
                data = self.fallback

        # ✅ Enrich with real-world info (Serper + Unsplash)
        enriched = []
        for d in data:
            dest_name = d.get("destination", "Unknown")
            snippets = search_places(dest_name)
            img = get_image_url(dest_name)
            d["search_snippets"] = snippets[:3] if snippets else []
            d["image_url"] = img
            enriched.append(d)

        console.print(f"[green]Research enriched for {len(enriched)} destinations![/green]")
        return enriched
