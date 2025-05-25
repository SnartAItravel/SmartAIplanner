import streamlit as st
import streamlit.components.v1 as components

# State management for slides (minimal setup for Slide 1)
if "slide" not in st.session_state:
    st.session_state.slide = 1
if "welcome_spoken" not in st.session_state:
    st.session_state.welcome_spoken = False

# JavaScript for button interactivity and slide transition
try:
    components.html(
        """
        <script>
        function activateSlide2() {
            // Hidden input to trigger Python-side action
            document.getElementById('hidden-activate-button').click();
        }
        </script>
        """,
        height=0
    )
except Exception as e:
    st.error(f"Failed to load JavaScript: {str(e)}")

# CSS Styling for the glowing button
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
        /* Hide the Streamlit button while keeping it functional */
        #hidden-activate-button {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
except Exception as e:
    st.error(f"Failed to load CSS: {str(e)}")

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
