import streamlit as st
import base64
from io import BytesIO

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# === EMBEDDED BASE64 CONTENT (REPLACE WITH YOUR ACTUAL STRINGS) ===
logo_base64 = """<INSERT_YOUR_LOGO_BASE64_HERE>"""
whoosh_base64 = """<INSERT_YOUR_WHOOSH_BASE64_HERE>"""

# === SHOW LOGO FUNCTION ===
def show_logo():
    image_data = base64.b64decode(logo_base64)
    st.image(BytesIO(image_data), caption="", use_container_width=True)

# === PLAY AUDIO USING HTML (AUTO-PLAY) ===
def play_whoosh_html():
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{whoosh_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

# === STYLED BUTTON HTML ===
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

# === MAIN APP LOGIC ===
if "activate" in st.query_params:
    play_whoosh_html()
    show_logo()
else:
    st.markdown(button_html, unsafe_allow_html=True)
