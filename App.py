import streamlit as st
import base64

st.set_page_config(page_title="Smart AI Travel App", layout="centered")

# === Glowing splash logo (Base64 PNG) ===
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAAAZAAAADICAYAAAA8tURZAAAABmJLR0QA/wD/AP+gvaeTAAABUUlE
QVR4nO3QsQ0AIAwDQPf/p7dIQ1VGjG5rSTL2ODoAAAAAAAAAAAAAAAAAAAAAAABwu13Mbb0AAAD/
7PUAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7Y
AwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgD
AAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMA
AQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwAB
AAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEA
AAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAP7YAwABAAAA/tgDAAEAAAD+2AMAAQAA
AP7YAwABAAAA/tgDAAEAAAD+2AMAAQAAAAAAAAAAAAAAAAAAAAAAAPjrA8K+jBShpQAAAABJRU5E
rkJggg==
"""

# === Real whoosh sound (Base64 WAV snippet) ===
whoosh_base64 = """
UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAIA+AAACABAAZGF0YRAAAAAAgICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI
CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
"""

# === Show glowing logo using HTML to avoid image decoding errors ===
def show_logo_html():
    html = f"""
    <div style='text-align: center; margin-top: 50px;'>
        <img src="data:image/png;base64,{logo_base64}" width="360" />
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# === Play whoosh sound via HTML audio autoplay ===
def play_whoosh_html():
    html = f"""
    <audio autoplay>
        <source src="data:audio/wav;base64,{whoosh_base64}" type="audio/wav">
    </audio>
    """
    st.markdown(html, unsafe_allow_html=True)

# === Tap to Activate Button Styling ===
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
