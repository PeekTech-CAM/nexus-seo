"""
Streamlit Secrets Diagnostic Tool
Add this to test your secrets configuration
"""

import streamlit as st
import os
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
st.title("🔍 Secrets Diagnostic Tool")
st.markdown("This will help us find why GEMINI_API_KEY isn't working")

st.markdown("---")

# Test 1: Check if secrets exist
st.markdown("### Test 1: Streamlit Secrets Object")
if hasattr(st, 'secrets'):
    st.success("✅ st.secrets exists")
    
    # Show all available keys (without values)
    st.markdown("**Available secret keys:**")
    try:
        keys = list(st.secrets.keys())
        for key in keys:
            st.write(f"- `{key}`")
    except Exception as e:
        st.error(f"Error reading keys: {str(e)}")
else:
    st.error("❌ st.secrets not found")

st.markdown("---")

# Test 2: Check specific key
st.markdown("### Test 2: GEMINI_API_KEY Check")
try:
    if 'GEMINI_API_KEY' in st.secrets:
        st.success("✅ GEMINI_API_KEY found in secrets")
        
        key_value = st.secrets["GEMINI_API_KEY"]
        
        if key_value:
            st.info(f"Key length: {len(key_value)} characters")
            st.info(f"Starts with: `{key_value[:10]}...`")
            st.info(f"Has whitespace: {key_value != key_value.strip()}")
            
            # Test if it's a valid format
            if key_value.startswith('AIza'):
                st.success("✅ Key format looks correct (starts with AIza)")
            else:
                st.warning(f"⚠️ Key doesn't start with 'AIza', starts with: {key_value[:4]}")
        else:
            st.error("❌ GEMINI_API_KEY exists but is empty")
    else:
        st.error("❌ GEMINI_API_KEY not found in secrets")
        st.info("Available keys: " + ", ".join(list(st.secrets.keys())))
except Exception as e:
    st.error(f"❌ Error accessing GEMINI_API_KEY: {str(e)}")

st.markdown("---")

# Test 3: Try to import and configure Gemini
st.markdown("### Test 3: Gemini Library Test")
try:
    import google.generativeai as genai
    st.success("✅ google.generativeai library imported")
    
    # Try to configure
    if 'GEMINI_API_KEY' in st.secrets:
        try:
            api_key = st.secrets["GEMINI_API_KEY"].strip()
            genai.configure(api_key=api_key)
            st.success("✅ Gemini configured successfully!")
            
            # Try to create model
            try:
                model = genai.GenerativeModel('gemini-1.5-pro')
                st.success("✅ Gemini model created successfully!")
                
                # Try a simple generation
                if st.button("Test AI Generation"):
                    with st.spinner("Testing..."):
                        response = model.generate_content("Say 'Hello, SEO!'")
                        st.success("✅ AI is working!")
                        st.write("Response:", response.text)
            except Exception as e:
                st.error(f"❌ Error creating model: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error configuring Gemini: {str(e)}")
    else:
        st.warning("⚠️ Skipping test - no API key found")
        
except ImportError:
    st.error("❌ google.generativeai not installed")
    st.code("pip install google-generativeai")

st.markdown("---")

# Test 4: Environment variables
st.markdown("### Test 4: Environment Variables")
env_key = os.getenv('GEMINI_API_KEY')
if env_key:
    st.success(f"✅ GEMINI_API_KEY found in environment (length: {len(env_key)})")
else:
    st.info("ℹ️ GEMINI_API_KEY not in environment variables (this is normal for Streamlit Cloud)")

st.markdown("---")

# Instructions
st.markdown("### 🛠️ How to Fix")

st.markdown("""
**If GEMINI_API_KEY is not found:**

1. Go to your Streamlit Cloud dashboard
2. Click on your app → Settings (⚙️ icon)
3. Go to "Secrets" tab
4. Make sure you have this EXACT format:

```toml
GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXX"
```

**Important:**
- Use double quotes `"`, not single quotes `'`
- Include the equals sign with spaces: ` = `
- No extra spaces at start or end of the key
- Make sure it starts with `AIza`

5. Click "Save"
6. Wait 30 seconds
7. Click "Reboot app" from the menu
8. Refresh this page
""")

st.markdown("---")

# Show secrets.toml example
with st.expander("📄 Example secrets.toml format"):
    st.code("""
GEMINI_API_KEY = "AIzaSyC-xxxxxxxxxxxxxxxxxxxxxxxxxxx"
SUPABASE_URL = "https://xxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxx"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxx"
""", language="toml")