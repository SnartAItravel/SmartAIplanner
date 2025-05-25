import streamlit as st
import streamlit.components.v1 as components
import json
import requests
from datetime import datetime, timedelta
import base64
import os
import re

# Amadeus API setup
AMADEUS_API_KEY = "BKarFHJJ1GGh0CVl0qhvmLL45jmeN4Uz"
AMADEUS_API_SECRET = "Tr9aaVLysU5LQSWF"
BASE_URL = "https://test.api.amadeus.com"

# Get Amadeus access token
@st.cache_data
def get_amadeus_token():
    url = f"{BASE_URL}/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Failed to authenticate with Amadeus API")
        return None

# Validate IATA codes (3-letter airport codes)
def is_valid_iata(code):
    return bool(re.match(r"^[A-Z]{3}$", code))

# Fetch flight offers from Amadeus with better error handling
def fetch_flights(origin, destination, departure_date, return_date=None):
    if not is_valid_iata(origin) or not is_valid_iata(destination):
        return None, "Invalid airport codes. Use 3-letter IATA codes (e.g., CPH for Copenhagen)."
    
    token = get_amadeus_token()
    if not token:
        return None, "Authentication failed with Amadeus API."
    
    url = f"{BASE_URL}/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
        "nonStop": False,
        "max": 5
    }
    if return_date:
        params["returnDate"] = return_date
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json().get("data", [])
            if not data:
                return None, "No flights found for this route."
            return data, None
        else:
            return None, f"Error fetching flights: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Error connecting to Amadeus API: {str(e)}"

# Simulated Pattern Collapse Generator (improved error handling)
def pattern_collapse_generator(flights, time_weight=0.5):
    if not flights:
        return None
    cost_weight = 1 - time_weight
    best_flight, best_score = None, float("inf")
    
    try:
        for flight in flights:
            price = float(flight["price"]["total"])
            # Parse duration
            duration = flight["itineraries"][0]["duration"].replace("PT", "").replace("H", "h").replace("M", "m")
            hours = 0
            minutes = 0
            if "h" in duration:
                hours = int(duration.split("h")[0])
                minutes = int(duration.split("h")[1].replace("m", "")) if "m" in duration else 0
            else:
                minutes = int(duration.replace("m", ""))
            total_minutes = hours * 60 + minutes
            
            # Normalize and score
            max_price = max(float(f["price"]["total"]) for f in flights)
            max_time = max(
                sum(int(s["duration"].replace("PT", "").replace("H", "h").replace("M", "m").split("h")[0]) * 60 +
                    (int(s["duration"].split("h")[1].replace("m", "")) if "m" in s["duration"] else 0))
                for f in flights for s in f["itineraries"]
            )
            norm_price = price / max_price if max_price else 0
            norm_time = total_minutes / max_time if max_time else 0
            score = cost_weight * norm_price + time_weight * norm_time
            if score < best_score:
                best_score = score
                best_flight = flight
        return best_flight
    except Exception as e:
        return None

# JavaScript for voice input and output
def add_voice_scripts():
    components.html(
        """
        <script>
            // Voice Output (Web Speech API)
            function speak(text) {
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = 'en-US';
                msg.rate = 0.9;  // Slightly slower for natural feel
                msg.pitch = 1.0; // Natural pitch
                window.speechSynthesis.speak(msg);
            }

            // Voice Input (WebRTC)
            let recognition = null;
            let isListening = false;
            let inputField = null;

            function startListening(fieldId) {
                inputField = document.querySelector(`input[name="${fieldId}"]`);
                if (!inputField) {
                    console.error('Input field not found for ID:', fieldId);
                    return ​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
