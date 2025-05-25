import streamlit as st
import base64

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# === Base64 Logo Image (1x1 transparent pixel for testing) ===
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAF/gL+OlPaJgAAAABJRU5ErkJggg==
"""

# === Base64 Whoosh Sound (short WAV snippet for testing) ===
whoosh_base64 = """
UklGRjQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YRAAAACAgICAgICAgICAgICAgICAgICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI
"""

# === Show logo image using HTML to bypass PIL ===
def show_logo_html():
    html = f"""
    <div style='text-align: center; margin-top: 50px;'>
        <img src="data:image/png;base64,{logo_base64}" width="250" />
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# === Play whoosh sound using HTML audio autoplay ===
def play_whoosh_html():
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{whoosh_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

# === Stylish Tap Button HTML ===
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
    show_logo_html()
else:
    st.markdown(button_html, unsafe_allow_html=True)
