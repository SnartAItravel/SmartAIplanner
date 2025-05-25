import streamlit as st
import base64
from io import BytesIO

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# === EMBEDDED BASE64 LOGO IMAGE (PNG) ===
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAACuvh3PAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz
AAALEwAACxMBAJqcGAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAADlSURB
VHic7cEBAQAAAIIg/69uNDhAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPAf
AAGc8wABkCWLWwAAAABJRU5ErkJggg==
"""

# === EMBEDDED BASE64 WHOOSH AUDIO (WAV) ===
whoosh_base64 = """
UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YYQAAACAgICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC
...
"""  # (truncated here for brevity; use full base64 from your WAV file)

# === Display logo image from base64 ===
def show_logo():
    image_data = base64.b64decode(logo_base64)
    st.image(BytesIO(image_data), caption="", use_container_width=True)

# === Play whoosh audio automatically using HTML ===
def play_whoosh_html():
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{whoosh_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

# === HTML + CSS for the "Tap to Activate" button ===
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

# === Main App Logic ===
if "activate" in st.query_params:
    play_whoosh_html()
    show_logo()
else:
    st.markdown(button_html, unsafe_allow_html=True)
