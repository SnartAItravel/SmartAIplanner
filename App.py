import streamlit as st
import streamlit.components.v1 as components
import json
import requests
from datetime import datetime, timedelta
import re
import traceback

# Try to import fuzzywuzzy
try:
    from fuzzywuzzy import process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    process = None

AMADEUS_API_KEY = "BKarFHJJ1GGh0CVl0qhvmLL45jmeN4Uz"
AMADEUS_API_SECRET = "Tr9aaVLysU5LQSWF"
BASE_URL = "https://test.api.amadeus.com"

CITY_TO_IATA = {
    "Copenhagen": "CPH",
    "Madrid": "MAD",
    "Dubai": "DXB",
    "Pakistan": "ISB",
    "Amsterdam": "AMS",
    "Dere": "DER",
}

@st.cache_data
def get_amadeus_token():
    url = f"{BASE_URL}/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_API_KEY,
        "client_secret": AMADEUS_API_SECRET
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            return None
    except Exception as e:
        st.error(f"Amadeus Auth Error: {str(e)}")
        return None

def is_valid_iata(code):
    return bool(re.match(r"^[A-Z]{3}$", code))

def fetch_flights(origin, destination, departure_date, return_date=None):
    if not is_valid_iata(origin) or not is_valid_iata(destination):
        return None, "Invalid airport codes."

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
                return None, "No flights found."
            return data, None
        else:
            return None, f"API error: {response.status_code}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"

def pattern_collapse_generator(flights, time_weight=0.5):
    if not flights:
        return None
    cost_weight = 1 - time_weight
    best_flight, best_score = None, float("inf")

    try:
        for flight in flights:
            price = float(flight["price"]["total"])
            duration = flight["itineraries"][0]["duration"].replace("PT", "").replace("H", "h").replace("M", "m")
            hours, minutes = 0, 0
            if "h" in duration:
                parts = duration.split("h")
                hours = int(parts[0])
                minutes = int(parts[1].replace("m", "")) if "m" in parts[1] else 0
            else:
                minutes = int(duration.replace("m", ""))
            total_minutes = hours * 60 + minutes

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
    except Exception:
        return None

def get_city_suggestion(user_input):
    if not user_input:
        return None, None
    cities = list(CITY_TO_IATA.keys())
    if FUZZY_AVAILABLE:
        best_match, score = process.extractOne(user_input, cities)
        if score > 80:
            return best_match, CITY_TO_IATA[best_match]
    user_input = user_input.lower()
    for city in cities:
        if user_input in city.lower():
            return city, CITY_TO_IATA[city]
    return None, None

def add_voice_scripts():
    try:
        components.html(
            """
            <script>
            function speak(text) {
                if ('speechSynthesis' in window) {
                    const msg = new SpeechSynthesisUtterance(text);
                    msg.lang = 'en-US';
                    window.speechSynthesis.speak(msg);
                }
            }
            </script>
            """,
            height=0
        )
    except:
        st.error("Voice script load failed.")

# === CSS Styling for glowing button (Slide 1) ===
st.markdown("""
    <style>
    .tap-button {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        border: none;
        border-radius: 50px;
        padding: 20px 60px;
        font-size: 22px;
        font-family: 'Poppins', sans-serif;
        color: white;
        cursor: pointer;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    .tap-button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4);
    }
    .tap-button:active {
        transform: scale(0.98);
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
    }
    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    </style>
""", unsafe_allow_html=True)

# === Slide Logic ===
if "slide" not in st.session_state:
    st.session_state.slide = 1
if "trip_data" not in st.session_state:
    st.session_state.trip_data = {}
if "welcome_spoken" not in st.session_state:
    st.session_state.welcome_spoken = False

# === Slide 1: Glowing Tap to Activate ===
if st.session_state.slide == 1:
    st.markdown("""
        <div class="center-container">
            <form action="?activate=1" method="post">
                <button type="submit" class="tap-button">Tap to Activate</button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    if "activate" in st.query_params:
        st.session_state.slide = 2
        st.session_state.welcome_spoken = False
        st.rerun()

# === Slide 2: Input ===
elif st.session_state.slide == 2:
    if not st.session_state.welcome_spoken:
        components.html("<script>speak('Welcome to the Smart AI Planner. Let’s begin.');</script>", height=0)
        st.session_state.welcome_spoken = True

    st.write("Plan your trip")

    is_round_trip = st.checkbox("Round Trip", value=False)
    start_input = st.text_input("Start City", "")
    start_suggestion, start_iata = get_city_suggestion(start_input)
    if start_iata:
        st.write(f"Did you mean {start_suggestion} ({start_iata})?")
        start_city = start_iata
    else:
        start_city = start_input.upper()

    dest_input = st.text_input("Destination City", "")
    dest_suggestion, dest_iata = get_city_suggestion(dest_input)
    if dest_iata:
        st.write(f"Did you mean {dest_suggestion} ({dest_iata})?")
        dest_city = dest_iata
    else:
        dest_city = dest_input.upper()

    today = datetime.now().date()
    departure_date = st.date_input("Departure Date", min_value=today, value=today)
    return_date = None
    if is_round_trip:
        return_date = st.date_input("Return Date", min_value=departure_date + timedelta(days=1))

    priority = st.selectbox("Priority", ["Balanced", "Cheapest", "Fastest"])
    time_weight = {"Balanced": 0.5, "Cheapest": 0.2, "Fastest": 0.8}[priority]

    if st.button("Search Flights"):
        st.session_state.trip_data = {
            "start": start_city,
            "dest": dest_city,
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d") if return_date else None,
            "time_weight": time_weight
        }
        st.session_state.slide = 3
        st.rerun()

# === Slide 3: Flight Results ===
elif st.session_state.slide == 3:
    trip = st.session_state.trip_data
    st.write(f"Finding flights from {trip['start']} to {trip['dest']}...")
    flights, error = fetch_flights(trip["start"], trip["dest"], trip["departure_date"], trip["return_date"])
    if error:
        st.error(error)
        components.html(f"<script>speak('{error}');</script>", height=0)
    elif flights:
        best = pattern_collapse_generator(flights, trip["time_weight"])
        if best:
            seg = best["itineraries"][0]["segments"][0]
            summary = f"{seg['departure']['iataCode']} → {seg['arrival']['iataCode']}, Price ${best['price']['total']}"
            st.success(summary)
            components.html(f"<script>speak('{summary}');</script>", height=0)
        else:
            msg = "No suitable flight found."
            st.error(msg)
            components.html(f"<script>speak('{msg}');</script>", height=0)

    if st.button("New Search"):
        st.session_state.slide = 2
        st.rerun()

# === Footer ===
st.markdown("*Powered by Shah’s Pattern Collapse Generator and Earth Prime*")
