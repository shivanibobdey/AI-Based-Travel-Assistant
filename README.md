🌍 AI-Powered Travel Assistant using Agentic AI
🧠 Overview

The AI-Powered Travel Assistant is an intelligent Agentic AI system that autonomously plans personalized trips based on user preferences such as budget, duration, interests, and preferred climate.
It leverages multi-agent collaboration, LLM reasoning (Gemini API), and real-time APIs (Serper, Unsplash, Weather) to deliver detailed, optimized travel itineraries with images and weather insights.

This project showcases how modular AI agents can communicate, reason, and coordinate through a central control system to achieve complex, real-world goals.

✨ Key Features

🧠 Multi-Agent Architecture: Each agent performs a specialized task — from preference gathering to itinerary design and final decision-making.

🌐 Real-Time Web Search (Serper API): Retrieves up-to-date travel data, attractions, and local highlights.

🌤️ Weather Forecasting: Integrates weather data to ensure trip suitability based on user’s preferred climate.

🖼️ Dynamic Images (Unsplash API): Displays high-quality destination visuals for better user experience.

🤖 Gemini API Integration: Powers reasoning, summarization, and intelligent decision-making using Google’s LLMs.

💬 Streamlit Interface: Provides a simple, interactive frontend for users to input preferences and view results instantly.

🧩 Coordinator Module: Manages workflow among all agents, ensuring seamless data flow and consistent logic.

🧩 Architecture Overview
Agents Used

Preference Agent: Captures user input (name, budget, duration, interests, preferred climate).

Research Agent: Searches for destinations based on preferences using Serper API and Gemini reasoning.

Weather Agent: Retrieves live or simulated weather data for shortlisted destinations.

Itinerary Agent: Designs personalized, day-wise itineraries considering weather and interests.

Decision Agent: Compares destinations based on weather, budget, and activity diversity, selecting the best option.

Coordinator: Controls agent workflow, error handling, and final report generation.

⚙️ Technologies Used

Language: Python

Frontend: Streamlit

APIs:

🧭 Serper API – for real-time destination research

🌤️ Weather API – for live weather forecasting

🧠 Gemini API – for AI reasoning and summarization

🖼️ Unsplash API – for relevant destination imagery

Libraries: dotenv, rich, requests, streamlit, google-generativeai

🧭 Workflow

User enters travel preferences on the Streamlit app.

Agents communicate sequentially:

PreferenceAgent → ResearchAgent → WeatherAgent → ItineraryAgent → DecisionAgent.

The Coordinator manages data transfer among agents and compiles the final output.

Gemini API processes and refines the final recommendation.

The user receives a detailed personalized travel plan with reasoning, itinerary, weather, and visuals.

🌟 Example Use Case

User Query: “Plan a 5-day budget-friendly beach trip in tropical weather.”

✅ The AI Assistant outputs:

Best destinations matching budget & climate

Daily itinerary (activities, attractions, rest days)

Weather forecast for each day

Destination images & summary

🧠 Agentic AI Concepts Demonstrated

Autonomy: Agents act independently to perform specific subtasks.

Reasoning: LLM (Gemini) interprets data and justifies recommendations.

Collaboration: Agents coordinate through the central controller to achieve a shared goal.

Adaptability: Dynamic itinerary generation based on changing inputs.
