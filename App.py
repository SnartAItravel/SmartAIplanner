import streamlit as st
import base64
from io import BytesIO

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# --- Test Base64 Image (invisible 1x1 PNG — just for debugging) ---
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAF/gL+OlPaJgAAAABJRU5ErkJggg==
"""

# --- Real Base64 Whoosh Sound (short WAV) ---
whoosh_base64 = """
UklGRjQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YRAAAACAgICAgICAgICAgICAgICAgICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI
CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
"""  # This is short and valid; just for the audio test

# --- Function to Show Image ---
def show_logo():
    image_data = base64.b64decode(logo_base64)
    st.image(BytesIO(image_data), caption="", use_container_width=True)

# --- Function to Auto-Play Audio ---
def play_whoosh_html():
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{whoosh_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

# --- Glowing Tap Button ---
button_html = '''
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
</style>
<div style='text-align: center; padding-top: 100px;'>
    <form action="/?activate=1" method="post">
        <button type="submit" class="tap-button">Tap to Activate</button>
    </form>
</div>
'''

# --- Main Logic ---
if "activate" in st.query_params:
    play_whoosh_html()
    show_logo()
else:
    st.markdown(button_html, unsafe_allow_html=True)
