import streamlit as st
import streamlit.components.v1 as components

# Use a unique state key to isolate Slide 2's state
if "slide2_test_initialized" not in st.session_state:
    # Hard reset session state to avoid conflicts
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.slide2_test = 2  # Unique key for Slide 2
    st.session_state.welcome_spoken = False
    st.session_state.slide2_test_initialized = True

# JavaScript for button interactivity (placeholder for transition)
try:
    components.html(
        """
        <script>
        function activateSlide() {
            console.log('Button clicked'); // Placeholder for transition
        }
        </script>
        """,
        height=0
    )
except Exception as e:
    st.error(f"Failed to load JavaScript: {str(e)}")

# CSS Styling for the centered glowing button (matching Slide 1)
try:
    st.markdown("""
        <style>
        /* Ensure the app takes up the full viewport height */
        html, body, [data-testid="stAppViewContainer"] {
            height: 100vh !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }
        .center-container {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            height: 100vh !important;
            min-height: 100vh !important;
            width: 100vw !important;
            margin: 0 !important;
            padding: 0 !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            background: linear-gradient(to bottom, #f0f8ff, #e6f0fa) !important; /* Light gradient background */
        }
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
        </style>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load CSS: {str(e)}")

# Slide 2: Centered Tap to Activate Button (Design and Layout Focus)
if st.session_state.get("slide2_test", 2) == 2:
    with st.container():
        st.markdown('<div class="center-container">', unsafe_allow_html=True)
        st.markdown('<button id="tap-to-activate" class="tap-button" onclick="activateSlide()">Tap to Activate</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Slide state mismatch. Expected Slide 2, but current slide2_test is " + str(st.session_state.get("slide2_test")))p
