import streamlit as st
import base64
from io import BytesIO
from PIL import Image
import tempfile

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# Base64-encoded assets
logo_base64 = "R0lGODlhAQABAIAAAAUEBAgAAAA7"
whoosh_base64 = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjUyLjYx"

# Decode base64 and display image
def show_logo():
    gif_data = base64.b64decode(logo_base64)
    st.image(BytesIO(gif_data), caption="Smart AI Travel Planner", use_container_width=True)

# Decode base64 and play audio
def play_whoosh():
    audio_data = base64.b64decode(whoosh_base64)
    st.audio(BytesIO(audio_data), format="audio/mp3", start_time=0)

# Custom CSS for the "Tap to Activate" button
button_html = """
<style>
    .tap-button {
        background: linear-gradient(to right, white, gold);
        border: none;
        border-radius: 50px;
        padding: 20px 60px;
        font-size: 22px;
        font-family: 'Poppins', sans-serif;
        color: #000;
        cursor: pointer;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
        background-color: #87CEFA;
    }

    .tap-button:hover {
        transform: scale(1.05);
        box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.3);
    }

    .tap-button:active {
        transform: scale(0.98);
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
    }
</style>

<div style='text-align: center; padding-top: 100px;'>
    <form action="/?activate=1" method="post">
        <button type="submit" class="tap-button">Tap to Activate</button>
    </form>
</div>
"""

if "activate" in st.query_params:
    play_whoosh()
    show_logo()
else:
    st.markdown(button_html, unsafe_allow_html=True)
