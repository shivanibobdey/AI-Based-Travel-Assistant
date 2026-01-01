# app.py
import streamlit as st
from coordinator import Coordinator
import re

st.set_page_config(page_title="AI Travel Assistant", page_icon="🌍", layout="wide")

# ---- PAGE TITLE ----
st.title("🌍 AI-Powered Travel Assistant")
st.markdown("Welcome! Get personalized travel recommendations powered by AI agents 🤖")

# ---- USER INPUT FORM ----
with st.form("travel_form"):
    name = st.text_input("Enter your name:")
    budget = st.number_input("Enter your budget (in USD):", min_value=100, max_value=10000, step=100)
    duration = st.number_input("Enter trip duration (in days):", min_value=1, max_value=30, step=1)
    interests = st.text_input("Enter your interests (comma separated):", placeholder="hiking, swimming, culture")
    climate = st.text_input("Preferred climate (e.g., tropical, cold, pleasant):", placeholder="cold")

    submit = st.form_submit_button("✨ Generate My Trip Plan")

# ---- MAIN LOGIC ----
if submit:
    if not all([name, budget, duration, interests, climate]):
        st.warning("Please fill in all the details before submitting.")
    else:
        with st.spinner("🤖 Coordinating AI agents... please wait ⏳"):
            coordinator = Coordinator()
            result = coordinator.coordinate(name, budget, duration, interests, climate)

        st.success("🎉 Your personalized trip plan is ready!")
        st.markdown("### 🧳 Your AI Trip Plan:")

        # ---- ITINERARY + MAIN DECISION ----
        if isinstance(result, dict):
            final_decision = result.get("final_decision")

            if isinstance(final_decision, str) and final_decision.strip():
                # ✅ Clean markdown formatting issues
                cleaned_decision = re.sub(r'([0-9])([A-Za-z])', r'\1 \2', final_decision)  # space between digits and letters
                cleaned_decision = cleaned_decision.replace("*", "").replace("_", "")  # remove stray markdown chars

                if "Day 1" in cleaned_decision or "Day 2" in cleaned_decision:
                    formatted_itinerary = cleaned_decision.replace("Day ", "\n\n**Day ")
                    st.markdown(formatted_itinerary, unsafe_allow_html=True)
                else:
                    st.markdown(cleaned_decision, unsafe_allow_html=True)
            else:
                st.warning("Itinerary could not be generated due to an internal Gemini error. Please try again later.")

        else:
            st.markdown(result, unsafe_allow_html=True)

        # ---- DESTINATION RECOMMENDATIONS ----
        st.markdown("---")
        st.markdown("### 📸 Top Destination Recommendations")

        research_data = result.get("research_data", []) if isinstance(result, dict) else []
        if research_data:
            cols = st.columns(2)
            for i, dest in enumerate(research_data):
                col = cols[i % 2]

                dest_name = dest.get("destination", "Unknown")
                image_url = dest.get("image_url")
                highlights = dest.get("highlights", [])
                best_season = dest.get("best_season", "N/A")
                hotel_cost = dest.get("hotel_cost_usd", "N/A")

                with col:
                    st.markdown(f"#### 📍 {dest_name}")

                    if image_url and isinstance(image_url, str) and image_url.startswith("http"):
                        st.image(image_url, caption=dest_name, use_container_width=True)
                    else:
                        st.info("No image available for this destination.")

                    st.markdown(f"**🏨 Avg Hotel Cost:** ${hotel_cost} per night")
                    st.markdown(f"**🌤 Best Season:** {best_season}")

                    # ✅ Highlights cleaned and formatted
                    if isinstance(highlights, list):
                        highlight_text = ", ".join(highlights)
                    elif isinstance(highlights, str):
                        highlight_text = highlights.replace(",", ", ")
                    else:
                        highlight_text = "Not available"

                    st.markdown(f"**✨ Highlights:** {highlight_text}")
                    st.markdown("---")
        else:
            st.warning("No destination data available.")
