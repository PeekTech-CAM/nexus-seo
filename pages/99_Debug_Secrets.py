"""
Streamlit Secrets Diagnostic Tool
"""

import streamlit as st
import os

# ============================================================================
# PAGE CONFIG - MUST BE FIRST (only once!)
# ============================================================================
st.set_page_config(
    page_title="Secrets Diagnostic - Nexus SEO",
    page_icon="🔍",
    layout="wide"
)

# ============================================================================
# HIDE DEFAULT STREAMLIT NAV
# ============================================================================
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebarNav"] {display: none !important;}
    nav[aria-label="Pages"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION COMPONENT (with error handling)
# ============================================================================
try:
    from nav_component import add_page_navigation
    add_page_navigation("Diagnostic", "🔍")
except Exception as e:
    st.warning(f"⚠️ Navigation component error: {e}")

# ============================================================================
# HEADER
# ============================================================================
st.title("🔍 Secrets Diagnostic Tool")
st.markdown("This will help us find why GEMINI_API_KEY isn't working")
st.markdown("---")

# ============================================================================
# TEST 1: CHECK IF SECRETS EXIST
# ============================================================================
st.markdown("### Test 1: Streamlit Secrets Object")
if hasattr(st, 'secrets'):
    st.success("✅ st.secrets exists")
    
    # Show all available keys (without values)
    st.markdown("**Available secret keys:**")
    try:
        keys = list(st.secrets.keys())
        if keys:
            for key in sorted(keys):
                st.write(f"- `{key}`")
        else:
            st.warning("⚠️ No secrets found - secrets file might be empty")
    except Exception as e:
        st.error(f"Error reading keys: {str(e)}")
else:
    st.error("❌ st.secrets not found - this is very unusual!")

st.markdown("---")

# ============================================================================
# TEST 2: CHECK SPECIFIC KEY
# ============================================================================
st.markdown("### Test 2: GEMINI_API_KEY Check")
try:
    if 'GEMINI_API_KEY' in st.secrets:
        st.success("✅ GEMINI_API_KEY found in secrets")
        
        key_value = st.secrets["GEMINI_API_KEY"]
        
        if key_value:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Key Length", f"{len(key_value)} chars")
            
            with col2:
                st.metric("Starts With", f"{key_value[:10]}...")
            
            with col3:
                has_whitespace = key_value != key_value.strip()
                st.metric("Has Whitespace", "⚠️ YES" if has_whitespace else "✅ NO")
            
            # Test if it's a valid format
            if key_value.startswith('AIza'):
                st.success("✅ Key format looks correct (starts with AIza)")
            else:
                st.warning(f"⚠️ Key doesn't start with 'AIza', starts with: `{key_value[:4]}`")
            
            # Check for common issues
            issues = []
            if has_whitespace:
                issues.append("Contains leading/trailing whitespace")
            if len(key_value) < 30:
                issues.append("Key seems too short")
            if '"' in key_value or "'" in key_value:
                issues.append("Contains quote characters")
            
            if issues:
                st.warning("⚠️ Potential issues detected:")
                for issue in issues:
                    st.write(f"- {issue}")
        else:
            st.error("❌ GEMINI_API_KEY exists but is empty")
    else:
        st.error("❌ GEMINI_API_KEY not found in secrets")
        st.info("Available keys: " + ", ".join(list(st.secrets.keys())))
except Exception as e:
    st.error(f"❌ Error accessing GEMINI_API_KEY: {str(e)}")

st.markdown("---")

# ============================================================================
# TEST 3: TRY TO IMPORT AND CONFIGURE GEMINI
# ============================================================================
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
                if st.button("🧪 Test AI Generation", type="primary"):
                    with st.spinner("Testing API connection..."):
                        try:
                            response = model.generate_content("Say 'Hello, SEO!' in exactly 2 words")
                            st.success("✅ AI is working perfectly!")
                            st.info(f"**Response:** {response.text}")
                        except Exception as e:
                            st.error(f"❌ Generation failed: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error creating model: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error configuring Gemini: {str(e)}")
    else:
        st.warning("⚠️ Skipping test - no API key found")
        
except ImportError as e:
    st.error("❌ google.generativeai not installed")
    st.code("pip install google-generativeai", language="bash")
    st.info("Add this to requirements.txt")
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")

st.markdown("---")

# ============================================================================
# TEST 4: ENVIRONMENT VARIABLES
# ============================================================================
st.markdown("### Test 4: Environment Variables")
env_key = os.getenv('GEMINI_API_KEY')
if env_key:
    st.success(f"✅ GEMINI_API_KEY found in environment (length: {len(env_key)})")
    st.info("Note: Streamlit Cloud uses st.secrets, not environment variables")
else:
    st.info("ℹ️ GEMINI_API_KEY not in environment variables (this is normal for Streamlit Cloud)")

st.markdown("---")

# ============================================================================
# INSTRUCTIONS
# ============================================================================
st.markdown("### 🛠️ How to Fix")

tab1, tab2, tab3 = st.tabs(["📝 Streamlit Cloud", "💻 Local Development", "🔧 Common Issues"])

with tab1:
    st.markdown("""
    **For Streamlit Cloud:**
    
    1. Go to your Streamlit Cloud dashboard: https://share.streamlit.io
    2. Click on your app → **Settings** (⚙️ icon) → **Secrets**
    3. Make sure you have this EXACT format:
    
    ```toml
    GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXX"
    ```
    
    **Important:**
    - Use double quotes `"`, not single quotes `'`
    - Include the equals sign with spaces: ` = `
    - No extra spaces at start or end of the key
    - Make sure it starts with `AIza`
    - One key per line
    
    4. Click **Save**
    5. Wait 30 seconds for secrets to sync
    6. Click **Reboot app** (⋮ menu → Reboot app)
    7. Refresh this page
    """)

with tab2:
    st.markdown("""
    **For Local Development:**
    
    1. Create file: `.streamlit/secrets.toml` in your project root
    2. Add your secrets:
    
    ```toml
    GEMINI_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXX"
    ```
    
    3. Make sure `.streamlit/secrets.toml` is in `.gitignore`
    4. Restart your Streamlit app
    
    **Get your API key:**
    - Go to: https://aistudio.google.com/app/apikey
    - Click "Create API Key"
    - Copy the key (starts with `AIza`)
    """)

with tab3:
    st.markdown("""
    **Common Issues & Solutions:**
    
    ❌ **"Key not found"**
    - Make sure spelling is exact: `GEMINI_API_KEY` (all caps, underscores)
    - Check for typos in secrets file
    
    ❌ **"Invalid API key"**
    - Key should start with `AIza`
    - No quotes in the actual key value
    - No spaces before/after the key
    
    ❌ **"Permission denied"**
    - API key might be restricted
    - Check quota limits in Google Cloud Console
    
    ❌ **"Module not found"**
    - Install: `pip install google-generativeai`
    - Add to `requirements.txt`
    
    ❌ **Changes not taking effect**
    - Wait 30 seconds after saving secrets
    - Reboot app (don't just refresh)
    - Clear browser cache
    """)

st.markdown("---")

# ============================================================================
# EXAMPLE FORMAT
# ============================================================================
with st.expander("📄 Complete secrets.toml Example"):
    st.code("""# .streamlit/secrets.toml

# Google Gemini API
GEMINI_API_KEY = "AIzaSyC-xxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Supabase
SUPABASE_URL = "https://xxxxxxxxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxx"
SUPABASE_SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxx"

# Stripe
STRIPE_SECRET_KEY = "sk_test_xxxxxxxxxxxxxxxxxxxxx"
STRIPE_WEBHOOK_SECRET = "whsec_xxxxxxxxxxxxxxxxxxxxx"

# Stripe Price IDs
STRIPE_PRICE_PRO_MONTHLY = "price_xxxxxxxxxxxxx"
STRIPE_PRICE_PRO_ANNUAL = "price_xxxxxxxxxxxxx"

# App Configuration
APP_URL = "https://your-app.streamlit.app"
""", language="toml")

# ============================================================================
# ACTIONS
# ============================================================================
st.markdown("---")
st.markdown("### 🔧 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Re-run Diagnostic", use_container_width=True, type="primary"):
        st.rerun()

with col2:
    if st.button("📚 Gemini API Docs", use_container_width=True):
        st.markdown("[Open Google AI Studio](https://aistudio.google.com)")

with col3:
    if st.button("← Back to App", use_container_width=True):
        try:
            st.switch_page("app.py")
        except:
            st.info("Navigate manually to main app")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("🔒 API keys are masked for security")
st.caption("💡 This is a diagnostic tool - remove before production")