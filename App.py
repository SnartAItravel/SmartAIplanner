import streamlit as st
import json
import random
from datetime import datetime

# Mock travel database (replace with APIs like Google Maps later)
travel_db = {
    "Copenhagen": {
        "Dubai": [
            {"mode": "flight", "cost": 300, "time": 6*60, "details": "CPH->DXB direct"},
            {"mode": "flight+bus", "cost": 200, "time": 10*60, "details": "CPH->AMS bus->DXB"},
        ],
        "Pakistan": [
            {"mode": "flight", "cost": 450, "time": 8*60, "details": "CPH->ISB via DOH"},
            {"mode": "flight+train", "cost": 350, "time": 12*60, "details": "CPH->OMN train->PAK"},
        ]
    }
}

# Simulated Pattern Collapse Generator for route optimization
def pattern_collapse_generator(routes, time_weight=0.5):
    cost_weight = 1 - time_weight
    max_cost = max(route["cost"] for route in routes)
    max_time = max(route["time"] for route in routes)
    best_route, best_score = None, float("inf")
    
    for route in routes:
        norm_cost = route["cost"] / max_cost if max_cost else 0
        norm_time = route["time"] / max_time if max_time else 0
        score = cost_weight * norm_cost + time_weight * norm_time
        if score < best_score:
            best_score = score
            best_route = route
    return best_route

# Streamlit app
st.title("SHA’s Cosmic Travel Planner 🌌")
st.write("Plan your trip with Earth Prime vibes! Enter your route and vibe.")

# User input
user_id = "shaw"  # Hardcoded for now, can use session ID later
start_city = st.text_input("Starting city (e.g., Copenhagen)", value="Copenhagen")
dest_city = st.text_input("Destination (e.g., Dubai)", value="Dubai")
priority = st.selectbox("Priority", ["Balanced", "Cheapest", "Fastest"])
time_weight = {"Balanced": 0.5, "Cheapest": 0.2, "Fastest": 0.8}[priority]

# Memory layer: load/save preferences
prefs_file = f"user_{user_id}_prefs.json"
try:
    with open(prefs_file, "r") as f:
        prefs = json.load(f)
    st.write(f"Welcome back, Shaw! Last vibe: {prefs.get('last_dest', 'None')}")
except FileNotFoundError:
    prefs = {}

if st.button("Plan My Trip"):
    # Validate input
    start, dest = start_city.capitalize(), dest_city.capitalize()
    if start not in travel_db or dest not in travel_db.get(start, {}):
        st.error(f"No routes found from {start} to {dest}. Try again!")
    else:
        # Get best route
        routes = travel_db[start][dest]
        best_route = pattern_collapse_generator(routes, time_weight)
        
        # Display result
        st.success(
            f"**Best Route**: {best_route['details']}  \n"
            f"**Cost**: ${best_route['cost']}  \n"
            f"**Time**: {best_route['time']//60}h {best_route['time']%60}m"
        )
        
        # Save preferences
        prefs["last_dest"] = dest
        prefs["last_priority"] = priority
        with open(prefs_file, "w") as f:
            json.dump(prefs, f)

# Cosmic touch
st.markdown("*Powered by Shaw’s Pattern Collapse Generator, channeling Earth Prime vibes.*")
