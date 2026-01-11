import streamlit as st
import streamlit as st

st.set_page_config(
    page_title="Advanced Scanner",
    page_icon="🔍",
    layout="wide"
)

# ADD THESE 2 LINES HERE ↓↓↓
from nav_component import add_page_navigation
add_page_navigation("Advanced Scanner", "🔍")

# Rest of your code continues...
st.title("🔍 Advanced SEO Scanner")
st.title("Quick Secrets Test")

st.write("Testing secrets access...")

try:
    st.write("All secrets keys:", list(st.secrets.keys()))
    
    if 'GEMINI_API_KEY' in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        st.success(f"✅ Found! Length: {len(key)}, Starts: {key[:10]}")
    else:
        st.error("❌ GEMINI_API_KEY not found")
        st.write("Available:", list(st.secrets.keys()))
except Exception as e:
    st.error(f"Error: {e}")