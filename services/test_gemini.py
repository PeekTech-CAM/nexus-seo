"""
Test Gemini API Connection
Run this to check if Gemini is working
"""

import streamlit as st

st.title("🤖 Test Gemini API")

# Check if key exists
gemini_key = st.secrets.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("❌ GEMINI_API_KEY not found in secrets.toml")
    st.stop()

st.success(f"✅ API Key found: {gemini_key[:10]}...{gemini_key[-5:]}")

# Test import
try:
    import google.generativeai as genai
    st.success("✅ google.generativeai imported successfully")
except ImportError as e:
    st.error(f"❌ Failed to import: {e}")
    st.info("Run: pip install google-generativeai")
    st.stop()

# Test configuration
try:
    genai.configure(api_key=gemini_key)
    st.success("✅ Gemini configured successfully")
except Exception as e:
    st.error(f"❌ Configuration failed: {e}")
    st.stop()

# Test model creation
try:
    model = genai.GenerativeModel('gemini-pro')
    st.success("✅ Model created successfully")
except Exception as e:
    st.error(f"❌ Model creation failed: {e}")
    st.stop()

# Test simple generation
if st.button("Test Generate Content"):
    with st.spinner("Generating..."):
        try:
            response = model.generate_content("Say 'Hello, Nexus SEO!' in one sentence.")
            st.success("✅ Generation successful!")
            st.write("**Response:**")
            st.write(response.text)
        except Exception as e:
            st.error(f"❌ Generation failed: {e}")
            st.code(str(e))

# Test with SEO prompt
if st.button("Test SEO Analysis"):
    with st.spinner("Analyzing..."):
        try:
            prompt = """
You are an SEO expert. Analyze this data:

Website: https://example.com
Title: "Example Domain"
Description: Missing
Word Count: 50

Provide 3 quick recommendations in JSON format:
{
  "recommendations": [
    {"title": "Fix 1", "description": "Details..."}
  ]
}
"""
            response = model.generate_content(prompt)
            st.success("✅ SEO Analysis successful!")
            st.write("**Response:**")
            st.code(response.text)
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")
            st.code(str(e))