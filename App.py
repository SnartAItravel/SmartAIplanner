import streamlit as st
import base64
from io import BytesIO

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# Base64-encoded image and audio (your actual base64 strings go here)
logo_base64 = """YOUR_LOGO_BASE64_HERE"""
whoosh_base64 = """YOUR_WHOOSH_BASE64_HERE"""

def show_logo():
    image_data = base64.b64decode(logo_base64)
    st.image(BytesIO(image_data), caption="", use_container_width=True)

def play_whoosh_html():
    audio_data = base64.b64decode(whoosh_base64)
    audio_base64 = base64.b64encode(audio_data).decode()
    audio_html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

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

if "activate" in st.query_params:
    play_whoosh_html()
    show_logo()
else:
    st.markdown(button_html, unsafe_allow_html=True)
