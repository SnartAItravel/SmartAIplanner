import streamlit as st
import streamlit.components.v1 as components
import json
import requests
from datetime import datetime, timedelta
import base64
import os

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

# Fetch flight offers from Amadeus
def fetch_flights(origin, destination, departure_date, return_date=None):
    token = get_amadeus_token()
    if not token:
        return []
    
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
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        st.error(f"Error fetching flights: {response.status_code}")
        return []

# Simulated Pattern Collapse Generator (for now, picks best flight by price/time)
def pattern_collapse_generator(flights, time_weight=0.5):
    if not flights:
        return None
    cost_weight = 1 - time_weight
    best_flight, best_score = None, float("inf")
    
    for flight in flights:
        price = float(flight["price"]["total"])
        # Approximate duration in minutes (parse duration field)
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

# JavaScript for voice input and output
def add_voice_scripts():
    components.html(
        """
        <script>
            // Voice Output (Web Speech API)
            function speak(text) {
                var msg = new SpeechSynthesisUtterance(text);
                msg.lang = 'en-US';
                msg.rate = 1.0;
                window.speechSynthesis.speak(msg);
            }

            // Voice Input (WebRTC)
            let recognition = null;
            let isListening = false;
            let inputField = null;

            function startListening(fieldId) {
                inputField = document.getElementById(fieldId);
                if (!('webkitSpeechRecognition' in window)) {
                    alert('Speech recognition not supported in this browser. Try Chrome or Safari.');
                    return;
                }

                recognition = new webkitSpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'en-US';

                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    inputField.value = transcript;
                    inputField.dispatchEvent(new Event('input', { bubbles: true }));
                };

                recognition.onerror = function(event) {
                    console.error('Speech recognition error:', event.error);
                    alert('Error with speech recognition: ' + event.error);
                };

                recognition.onend = function() {
                    isListening = false;
                    document.getElementById('micButton_' + fieldId).style.backgroundColor = '';
                };

                if (!isListening) {
                    recognition.start();
                    isListening = true;
                    document.getElementById('micButton_' + fieldId).style.backgroundColor = '#ff4040';
                }
            }
        </script>
        """,
        height=0
    )

# CSS for glowing button and sliding calendar
st.markdown(
    """
    <style>
        .glowing-button {
            background-color: #1E90FF; /* Dodger Blue */
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 0 15px #1E90FF, 0 0 30px #1E90FF, 0 0 45px #1E90FF;
            animation: pulse 1.5s infinite;
            transition: all 0.3s ease;
        }
        .glowing-button:hover {
            box-shadow: 0 0 25px #1E90FF, 0 0 40px #1E90FF, 0 0 60px #1E90FF;
            background-color: #00BFFF; /* Lighter blue on hover */
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 15px #1E90FF, 0 0 30px #1E90FF, 0 0 45px #1E90FF; }
            50% { box-shadow: 0 0 20px #1E90FF, 0 0 40px #1E90FF, 0 0 60px #1E90FF; }
            100% { box-shadow: 0 0 15px #1E90FF, 0 0 30px #1E90FF, 0 0 45px #1E90FF; }
        }
        .calendar-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            padding: 20px;
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
            animation: slide-up 0.5s ease;
            z-index: 1000;
        }
        @keyframes slide-up {
            from { transform: translateY(100%); }
            to { transform: translateY(0); }
        }
        .stDateInput > div > input {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
        }
        .stSelectbox > div > div {
            background-color: #f0f2f6;
            border-radius: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app with slides
st.title("SHA’s Cosmic Travel Planner 🌌")
add_voice_scripts()  # Add voice scripts

# State management for slides
if "slide" not in st.session_state:
    st.session_state.slide = 1
if "trip_data" not in st.session_state:
    st.session_state.trip_data = {}

# Slide 1: Tap to Activate
if st.session_state.slide == 1:
    st.markdown("<h3>Welcome to the Eternal Now of Travel! ✨</h3>", unsafe_allow_html=True)
    st.write("Tap below to start your cosmic journey.")
    # Use Streamlit's button with custom CSS
    if st.markdown(
        '<button class="glowing-button">Tap to Activate</button>',
        unsafe_allow_html=True
    ):
        st.session_state.slide = 2
        st.rerun()  # Updated to st.rerun()

# Slide 2: Input Form
elif st.session_state.slide == 2:
    st.write("Plan your trip with Earth Prime vibes! Enter your route and vibe.")
    
    # Toggle for round trip
    is_round_trip = st.checkbox("Round Trip", value=False)
    
    # Input fields with voice input button
    col1, col2 = st.columns([3, 1])
    with col1:
        start_city = st.text_input("Starting city (e.g., CPH)", value="CPH", key="start_city")
    with col2:
        st.markdown(
            '<button id="micButton_start_city" onclick="startListening(\'start_city\')" style="padding: 10px; border-radius: 50%;">🎙️</button>',
            unsafe_allow_html=True
        )
    
    col3, col4 = st.columns([3, 1])
    with col3:
        dest_city = st.text_input("Destination (e.g., DXB)", value="DXB", key="dest_city")
    with col4:
        st.markdown(
            '<button id="micButton_dest_city" onclick="startListening(\'dest_city\')" style="padding: 10px; border-radius: 50%;">🎙️</button>',
            unsafe_allow_html=True
        )
    
    # Date pickers with sliding calendar
    today = datetime(2025, 5, 25)
    with st.container():
        departure_date = st.date_input(
            "Departure Date",
            min_value=today,
            value=today,
            format="YYYY-MM-DD"
        )
        return_date = None
        if is_round_trip:
            return_date = st.date_input(
                "Return Date",
                min_value=departure_date + timedelta(days=1),
                value=departure_date + timedelta(days=1),
                format="YYYY-MM-DD"
            )
    
    priority = st.selectbox("Priority", ["Balanced", "Cheapest", "Fastest"])
    time_weight = {"Balanced": 0.5, "Cheapest": 0.2, "Fastest": 0.8}[priority]
    
    if st.button("Search Flights"):
        st.session_state.trip_data = {
            "start": start_city.upper(),
            "dest": dest_city.upper(),
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d") if return_date else None,
            "time_weight": time_weight
        }
        st.session_state.slide = 3
        st.rerun()  # Updated to st.rerun()

# Slide 3: Flight Results
elif st.session_state.slide == 3:
    trip_data = st.session_state.trip_data
    start, dest = trip_data["start"], trip_data["dest"]
    departure_date = trip_data["departure_date"]
    return_date = trip_data["return_date"]
    time_weight = trip_data["time_weight"]
    
    st.write(f"Searching flights from {start} to {dest}...")
    flights = fetch_flights(start, dest, departure_date, return_date)
    
    if not flights:
        error_msg = "No flights found. Try different cities or dates."
        st.error(error_msg)
        components.html(f"<script>speak('{error_msg}');</script>", height=0)
    else:
        best_flight = pattern_collapse_generator(flights, time_weight)
        if best_flight:
            price = best_flight["price"]["total"]
            itinerary = best_flight["itineraries"][0]
            duration = itinerary["duration"].replace("PT", "").replace("H", "h ").replace("M", "m")
            segments = itinerary["segments"][0]
            departure = segments["departure"]["at"]
            arrival = segments["arrival"]["at"]
            
            result = (
                f"Best Flight: {segments['departure']['iataCode']} to {segments['arrival']['iataCode']}  \n"
                f"Departure: {departure}  \n"
                f"Arrival: {arrival}  \n"
                f"Duration: {duration}  \n"
                f"Price: ${price}"
            )
            st.success(result)
            components.html(f"<script>speak('{result.replace('\n', '. ')}');</script>", height=0)
        else:
            error_msg = "Couldn’t find a suitable flight."
            st.error(error_msg)
            components.html(f"<script>speak('{error_msg}');</script>", height=0)
    
    if st.button("New Search"):
        st.session_state.slide = 2
        st.rerun()  # Updated to st.rerun()

# Cosmic touch
st.markdown("*Powered by Shaw’s Pattern Collapse Generator, channeling Earth Prime vibes.*")
