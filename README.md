# 🌍 AI-Powered Travel Assistant using Agentic AI
🧠 Overview

The AI-Powered Travel Assistant is an intelligent Agentic AI system that autonomously plans personalized trips based on user preferences such as budget, trip duration, interests, and preferred climate.

It leverages multi-agent collaboration, Google’s Gemini API, and real-time APIs like Serper, Unsplash, and Weather Forecasting API to generate detailed, reasoning-based itineraries — complete with visuals and live weather updates, all within an interactive Streamlit interface.

✨ Key Features

🤖 Agentic AI Architecture: Multi-agent system where each agent performs specialized tasks (preference gathering, research, weather analysis, itinerary generation, decision-making).

🌐 Serper API Integration: Fetches real-time travel data, destinations, and tourist information.

🌤️ Weather Forecasting API: Provides accurate weather forecasts for suggested destinations.

🖼️ Unsplash API: Displays beautiful, contextually relevant destination images.

🧠 Gemini API (Google): Handles AI reasoning, summarization, and intelligent decision-making.

💬 Streamlit Interface: Simple and interactive web interface for real-time travel planning.

🧩 Coordinator Module: Manages agent communication, sequencing, and data consistency.

🧩 Multi-Agent System Architecture
Agent	Description
PreferenceAgent	Collects and validates user inputs like name, budget, trip duration, interests, and preferred climate.
ResearchAgent	Searches for destinations matching preferences using Serper API and Gemini reasoning.
WeatherAgent	Retrieves real-time weather data for shortlisted destinations.
ItineraryAgent	Creates personalized, day-wise itineraries based on user interests and weather.
DecisionAgent	Evaluates and selects the most suitable destination using a reasoning matrix.
Coordinator	Controls overall workflow, ensuring data flow and consistency among agents.
⚙️ Tech Stack

Language: Python

Frontend: Streamlit

APIs & Tools:

🧭 Serper API – Destination and attraction insights

🌤️ Weather API – Live weather forecasting

🧠 Gemini API – LLM reasoning and summarization

🖼️ Unsplash API – Destination image retrieval

Libraries: streamlit, google-generativeai, dotenv, requests, rich

🧭 Workflow

User enters travel preferences in the Streamlit app.

PreferenceAgent structures and validates input.

ResearchAgent finds matching destinations.

WeatherAgent fetches live climate data.

ItineraryAgent generates daily activity plans.

DecisionAgent selects the best itinerary.

Coordinator compiles all outputs into one detailed result.
