"""
Quick Secrets Test - Debug Tool
"""

import streamlit as st

# ============================================================================
# PAGE CONFIG - MUST BE FIRST (only once!)
# ============================================================================
st.set_page_config(
    page_title="Secrets Test - Nexus SEO",
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
# NAVIGATION COMPONENT (Optional - remove if causes errors)
# ============================================================================
try:
    from nav_component import add_page_navigation
    add_page_navigation("Secrets Test", "🔍")
except:
    pass  # Skip if nav component has issues

# ============================================================================
# SECRETS TEST
# ============================================================================
st.title("🔍 Quick Secrets Test")
st.markdown("Testing secrets access and configuration")
st.markdown("---")

# Test basic secrets access
try:
    all_keys = list(st.secrets.keys())
    st.success(f"✅ Secrets file found with {len(all_keys)} keys")
    
    # Show all available keys (safe to display)
    with st.expander("📋 Available Secret Keys", expanded=True):
        for key in sorted(all_keys):
            st.write(f"- `{key}`")
    
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")
    st.stop()

st.markdown("---")

# ============================================================================
# TEST SPECIFIC SECRETS
# ============================================================================
st.markdown("### 🔑 Testing Specific Secrets")

secrets_to_test = {
    "GEMINI_API_KEY": "Google Gemini API",
    "STRIPE_SECRET_KEY": "Stripe Secret Key",
    "STRIPE_WEBHOOK_SECRET": "Stripe Webhook Secret",
    "SUPABASE_URL": "Supabase URL",
    "SUPABASE_KEY": "Supabase Key",
    "SUPABASE_SERVICE_ROLE_KEY": "Supabase Service Role Key",
    "APP_URL": "Application URL"
}

col1, col2 = st.columns(2)

for idx, (key, description) in enumerate(secrets_to_test.items()):
    target_col = col1 if idx % 2 == 0 else col2
    
    with target_col:
        try:
            if key in st.secrets:
                value = st.secrets[key]
                
                # Mask sensitive data
                if "SECRET" in key or "KEY" in key.upper():
                    if len(value) > 12:
                        masked = f"{value[:8]}...{value[-4:]}"
                    else:
                        masked = "***"
                    st.success(f"✅ **{description}**")
                    st.code(masked, language=None)
                else:
                    # Safe to show URLs
                    st.success(f"✅ **{description}**")
                    st.code(value[:50] + "..." if len(value) > 50 else value, language=None)
            else:
                st.warning(f"⚠️ **{description}**")
                st.caption(f"Missing: `{key}`")
                
        except Exception as e:
            st.error(f"❌ **{description}**")
            st.caption(f"Error: {str(e)}")

st.markdown("---")

# ============================================================================
# GEMINI API KEY DETAILED TEST
# ============================================================================
st.markdown("### 🤖 Gemini API Key Detailed Check")

try:
    if 'GEMINI_API_KEY' in st.secrets:
        key = st.secrets["GEMINI_API_KEY"]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Length", len(key))
        
        with col2:
            st.metric("Starts with", key[:10] + "...")
        
        with col3:
            st.metric("Ends with", "..." + key[-10:])
        
        # Check format
        if key.startswith("AIza"):
            st.success("✅ Format looks correct (starts with 'AIza')")
        else:
            st.warning("⚠️ Unexpected format - Gemini keys usually start with 'AIza'")
            
        # Test connection (optional)
        if st.button("🧪 Test Gemini API Connection", type="primary"):
            with st.spinner("Testing API connection..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=key)
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content("Say 'API working' in exactly 2 words")
                    st.success(f"✅ API Response: {response.text}")
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
    else:
        st.error("❌ GEMINI_API_KEY not found in secrets")
        st.markdown("""
        **To fix:**
        1. Go to Streamlit Cloud → Your App → Settings → Secrets
        2. Add:
        ```toml
        GEMINI_API_KEY = "your-api-key-here"
        ```
        """)
        
except Exception as e:
    st.error(f"Error checking Gemini API key: {e}")

st.markdown("---")

# ============================================================================
# STRIPE PRICE IDS CHECK
# ============================================================================
st.markdown("### 💳 Stripe Price IDs Check")

price_ids = [
    "STRIPE_PRICE_PRO_MONTHLY",
    "STRIPE_PRICE_PRO_ANNUAL",
    "STRIPE_PRICE_AGENCY_MONTHLY",
    "STRIPE_PRICE_AGENCY_ANNUAL",
    "STRIPE_PRICE_ELITE_MONTHLY",
    "STRIPE_PRICE_ELITE_ANNUAL",
]

configured_prices = 0
for price_key in price_ids:
    if price_key in st.secrets and st.secrets[price_key]:
        configured_prices += 1

st.metric("Configured Price IDs", f"{configured_prices}/{len(price_ids)}")

if configured_prices < len(price_ids):
    if st.button("🔍 View Detailed Price ID Check"):
        st.switch_page("pages/check_prices.py")

st.markdown("---")

# ============================================================================
# ACTIONS
# ============================================================================
st.markdown("### 🔧 Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Refresh Test", use_container_width=True, type="primary"):
        st.rerun()

with col2:
    if st.button("📚 View Documentation", use_container_width=True):
        st.info("Add secrets in `.streamlit/secrets.toml` locally or in Streamlit Cloud settings")

with col3:
    if st.button("← Back to Dashboard", use_container_width=True):
        try:
            st.switch_page("pages/1_dashboard.py")
        except:
            st.switch_page("app.py")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("🔒 Sensitive values are masked for security")
st.caption("💡 This is a debug tool - remove in production")