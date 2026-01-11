import streamlit as st

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