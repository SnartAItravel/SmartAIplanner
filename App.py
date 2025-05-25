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
                    msg.rate = 0.9;
                    msg.pitch = 1.0;
                    window.speechSynthesis.speak(msg);
                    console.log('Speaking:', text);
                } else {
                    console.error('Speech synthesis not supported in this browser.');
                }
            }

            let recognition = null;
            let isListening = false;
            let inputField = null;

            function startListening(fieldId) {
                console.log('Starting speech recognition for field:', fieldId);
                setTimeout(() => {
                    inputField = document.querySelector(`input[name="${fieldId}"]`);
                    if (!inputField) {
                        console.error('Input field not found for ID:', fieldId);
                        return;
                    }
                    if (!('webkitSpeechRecognition' in window)) {
                        console.error('Speech recognition not supported in this browser.');
                        alert('Speech recognition not supported. Try Chrome or Safari.');
                        return;
                    }

                    recognition = new webkitSpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = 'en-US';

                    recognition.onresult = function(event) {
                        const transcript = event.results[0][0].transcript;
                        console.log('Speech recognized:', transcript);
                        inputField.value = transcript;
                        inputField.dispatchEvent(new Event('input', { bubbles: true }));
                    };

                    recognition.onerror = function(event) {
                        console.error('Speech recognition error:', event.error);
                        alert('Speech recognition error: ' + event.error);
                    };

                    recognition.onend = function() {
                        isListening = false;
                        const micButton = document.getElementById('micButton_' + fieldId);
                        if (micButton) micButton.style.backgroundColor = '';
                        console.log('Speech recognition ended.');
                    };

                    if (!isListening) {
                        recognition.start();
                        isListening = true;
                        const micButton = document.getElementById('micButton_' + fieldId);
                        if (micButton) micButton.style.backgroundColor = '#ff4040';
                    }
                }, 500);
            }

            function activateSlide2() {
                // Hidden input to trigger Python-side action
                document.getElementById('hidden-activate-button').click();
            }
            </script>
            """,
            height=0
        )
    except Exception as e:
        st.error(f"Voice script load failed: {str(e)}")

# CSS Styling for glowing button and other elements
try:
    st.markdown("""
        <style>
        .tap-button {
            background: linear-gradient(to right, #00c6ff, #0072ff) !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 20px 60px !important;
            font-size: 22px !important;
            font-family: 'Poppins', sans-serif !important;
            color: white !important;
            cursor: pointer !important;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            max-width: 300px !important;
            text-align: center !important;
            margin: 0 auto !important;
            display: block !important;
        }
        .tap-button:hover {
            transform: scale(1.05) !important;
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4) !important;
        }
        .tap-button:active {
            transform: scale(0.98) !important;
            box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2) !important;
        }
        .center-container {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            height: 100vh !important;
        }
        .stCheckbox > label {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        .stCheckbox > label > input {
            display: none;
        }
        .stCheckbox > label > span {
            position: relative;
            display: inline-block;
            width: 50px;
            height: 25px;
            background-color: #ccc;
            border-radius: 25px;
            transition: background-color 0.3s;
            margin-right: 10px;
        }
        .stCheckbox > label > span::after {
            content: '';
            position: absolute;
            width: 21px;
            height: 21px;
            left: 2px;
            top: 2px;
            background-color: white;
            border-radius: 50%;
            transition: transform 0.3s ease;
        }
        .stCheckbox > label > input:checked + span {
            background-color: #0072ff;
        }
        .stCheckbox > label > input:checked + span::after {
            transform: translateX(calc(100% - 23px));
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
        .mic-button {
            padding: 10px;
            border-radius: 50%;
            cursor: pointer;
            border: none;
            background-color: #f0f2f6;
        }
        .mic-button:hover {
            background-color: #e0e2e6;
        }
        /* Hide the Streamlit button while keeping it functional */
        #hidden-activate-button {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load CSS: {str(e)}")

# Streamlit app with slides (wrapped in global try-except)
try:
    # State management for slides
    if "slide" not in st.session_state:
        st.session_state.slide = 1
    if "trip_data" not in st.session_state:
        st.session_state.trip_data = {}
    if "welcome_spoken" not in st.session_state:
        st.session_state.welcome_spoken = False

    # Slide 1: Glowing Tap to Activate
    if st.session_state.slide == 1:
        with st.container():
            st.markdown('<div class="center-container">', unsafe_allow_html=True)
            # Display the styled HTML button
            st.markdown('<button id="tap-to-activate" class="tap-button" onclick="activateSlide2()">Tap to Activate</button>', unsafe_allow_html=True)
            # Hidden Streamlit button to handle the click event
            if st.button("Hidden Activate Button", key="hidden-activate-button"):
                st.session_state.slide = 2
                st.session_state.welcome_spoken = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Slide 2: Input
    elif st.session_state.slide == 2:
        try:
            add_voice_scripts()
            if not st.session_state.welcome_spoken:
                components.html("<script>speak('Welcome to the Smart AI Planner. Let’s begin.');</script>", height=0)
                st.session_state.welcome_spoken = True

            st.write("Plan your trip")

            is_round_trip = st.checkbox("Round Trip", value=False, key="round_trip")
            col1, col2 = st.columns([3, 1])
            with col1:
                start_input = st.text_input("Start City", "", key="start_city")
                start_suggestion, start_iata = get_city_suggestion(start_input)
                if start_iata:
                    st.write(f"Did you mean {start_suggestion} ({start_iata})?")
                    start_city = start_iata
                else:
                    start_city = start_input.upper()
            with col2:
                st.markdown(
                    '<button id="micButton_start_city" class="mic-button" onclick="startListening(\'start_city\')">🎙️</button>',
                    unsafe_allow_html=True
                )

            col3, col4 = st.columns([3, 1])
            with col3:
                dest_input = st.text_input("Destination City", "", key="dest_city")
                dest_suggestion, dest_iata = get_city_suggestion(dest_input)
                if dest_iata:
                    st.write(f"Did you mean {dest_suggestion} ({dest_iata})?")
                    dest_city = dest_iata
                else:
                    dest_city = dest_input.upper()
            with col4:
                st.markdown(
                    '<button id="micButton_dest_city" class="mic-button" onclick="startListening(\'dest_city\')">🎙️</button>',
                    unsafe_allow_html=True
                )

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
        except Exception as e:
            st.error(f"Error on Slide 2: {str(e)}")
            st.error(f"Traceback: {traceback.format_exc()}")

    # Slide 3: Flight Results
    elif st.session_state.slide == 3:
        try:
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
                    summary = f"{seg['departure']['iataCode']} to {seg['arrival']['iataCode']}, Price ${best['price']['total']}"
                    st.success(summary)
                    components.html(f"<script>speak('{summary}');</script>", height=0)
                else:
                    msg = "No suitable flight found."
                    st.error(msg)
                    components.html(f"<script>speak('{msg}');</script>", height=0)

            if st.button("New Search"):
                st.session_state.slide = 2
                st.rerun()
        except Exception as e:
            st.error(f"Error on Slide 3: {str(e)}")
            st.error(f"Traceback: {traceback.format_exc()}")

    # Footer
    try:
        st.markdown("*Powered by Shah’s Pattern Collapse Generator and Earth Prime*")
    except Exception as e:
        pass

except Exception as e:
    st.error(f"Failed to launch the app: {str(e)}")
    st.error("Please check the Streamlit Cloud logs for more details.")
    st.error(f"Traceback: {traceback.format_exc()}")
