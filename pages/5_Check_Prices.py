"""
Price ID Checker - See what's configured
"""

import streamlit as st
# Add sidebar
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.sidebar import setup_sidebar
setup_sidebar()
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
# Hide navigation - ADD THIS
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="New Scan - Nexus SEO",
    page_icon="🔍",
    layout="wide"
)
st.set_page_config(page_title="Price ID Checker", page_icon="🔍", layout="wide")

st.title("🔍 Stripe Price ID Configuration Check")
st.markdown("This shows which Price IDs are configured in your secrets")

st.markdown("---")

# Check all Price IDs
price_ids = {
    "Pro Monthly": "STRIPE_PRICE_PRO_MONTHLY",
    "Pro Annual": "STRIPE_PRICE_PRO_ANNUAL",
    "Agency Monthly": "STRIPE_PRICE_AGENCY_MONTHLY",
    "Agency Annual": "STRIPE_PRICE_AGENCY_ANNUAL",
    "Elite Monthly": "STRIPE_PRICE_ELITE_MONTHLY",
    "Elite Annual": "STRIPE_PRICE_ELITE_YEARLY",
    "1000 Credits": "STRIPE_PRICE_CREDITS_1000",
    "5000 Credits": "STRIPE_PRICE_CREDITS_5000",
    "10000 Credits": "STRIPE_PRICE_CREDITS_10000",
}

configured = 0
missing = 0

st.markdown("### 📋 Configuration Status")

for name, secret_key in price_ids.items():
    price_id = st.secrets.get(secret_key, "")
    
    col1, col2, col3 = st.columns([2, 3, 1])
    
    with col1:
        st.markdown(f"**{name}**")
    
    with col2:
        if price_id:
            st.code(price_id, language=None)
        else:
            st.markdown("*Not configured*")
    
    with col3:
        if price_id:
            if price_id.startswith("price_"):
                st.success("✅")
                configured += 1
            else:
                st.error("❌ Invalid")
        else:
            st.warning("⚠️")
            missing += 1

st.markdown("---")

# Summary
col1, col2 = st.columns(2)

with col1:
    st.metric("✅ Configured", configured)

with col2:
    st.metric("⚠️ Missing", missing)

if missing > 0:
    st.markdown("---")
    st.markdown("### 🔧 How to Fix")
    
    st.markdown("""
    **Missing Price IDs need to be added to Streamlit Secrets:**
    
    1. Go to your Streamlit Cloud dashboard
    2. Click **"Manage app"** → **Settings** → **Secrets**
    3. Add the missing Price IDs:
    
    ```toml
    # Get these from Stripe Dashboard → Products → [Your Product] → Pricing section
    
    # Subscriptions (must be RECURRING)
    STRIPE_PRICE_PRO_MONTHLY = "price_1SngZgGLbG2yglswvSpnbeNo"
    STRIPE_PRICE_PRO_YEARLY = "price_1SngyeGLbG2yglswI7A0HFOv"
    STRIPE_PRICE_AGENCY_MONTHLY = "price_1SngbXGLbG2yglswSghxhkrM"
    STRIPE_PRICE_AGENCY_ANNUAL = "price_1SngzGGLbG2yglswt1qAil9W"
    STRIPE_PRICE_ELITE_MONTHLY = "price_1SngdaGLbG2yglsw8IAyt9Cc"
    STRIPE_PRICE_ELITE_YEARLY = "price_1Snh0EGLbG2yglswMUTmB1HZ"
    
    # Credit Packs (must be ONE-TIME)
    STRIPE_PRICE_CREDITS_1000 = "price_1SngDNGLbG2yglswEsYrSaBN"
    STRIPE_PRICE_CREDITS_5000 = "price_1SngDrGLbG2yglswQhAtR5ZU"
    STRIPE_PRICE_CREDITS_10000 = "price_1SngEFGLbG2yglswbeIEyA1W"
    ```
    
    4. **Save** the secrets
    5. The app will automatically restart
    """)
    
    st.markdown("### 📍 Where to find Price IDs in Stripe:")
    st.markdown("""
    1. Go to: https://dashboard.stripe.com/test/products
    2. Click on a product (e.g., "Pro Mensual")
    3. Scroll to **"Pricing"** section
    4. Look for the price with the correct billing period
    5. Copy the **Price ID** (starts with `price_`)
    """)
else:
    st.success("🎉 All Price IDs are configured!")
    st.balloons()

st.markdown("---")

if st.button("← Back to Billing"):
    st.switch_page("pages/4_Billing.py")