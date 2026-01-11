"""
Price ID Checker - See what's configured
"""

import streamlit as st

# ============================================================================
# PAGE CONFIG - MUST BE FIRST (only once!)
# ============================================================================
st.set_page_config(
    page_title="Price ID Checker - Nexus SEO",
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
# NAVIGATION COMPONENT
# ============================================================================
from nav_component import add_page_navigation
add_page_navigation("Price Checker", "🔍")

# ============================================================================
# HEADER
# ============================================================================
st.title("🔍 Stripe Price ID Configuration Check")
st.markdown("This shows which Price IDs are configured in your secrets")
st.markdown("---")

# ============================================================================
# CHECK ALL PRICE IDS
# ============================================================================
price_ids = {
    "Pro Monthly": "STRIPE_PRICE_PRO_MONTHLY",
    "Pro Annual": "STRIPE_PRICE_PRO_ANNUAL",
    "Agency Monthly": "STRIPE_PRICE_AGENCY_MONTHLY",
    "Agency Annual": "STRIPE_PRICE_AGENCY_ANNUAL",
    "Elite Monthly": "STRIPE_PRICE_ELITE_MONTHLY",
    "Elite Annual": "STRIPE_PRICE_ELITE_ANNUAL",  # Fixed: was YEARLY
    "1000 Credits": "STRIPE_PRICE_CREDITS_1000",
    "5000 Credits": "STRIPE_PRICE_CREDITS_5000",
    "10000 Credits": "STRIPE_PRICE_CREDITS_10000",
}

configured = 0
missing = 0

st.markdown("### 📋 Configuration Status")

for name, secret_key in price_ids.items():
    try:
        price_id = st.secrets.get(secret_key, "")
    except:
        price_id = ""
    
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

# ============================================================================
# SUMMARY
# ============================================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("✅ Configured", configured)

with col2:
    st.metric("⚠️ Missing", missing)

with col3:
    total = len(price_ids)
    percentage = (configured / total * 100) if total > 0 else 0
    st.metric("📊 Progress", f"{percentage:.0f}%")

# ============================================================================
# INSTRUCTIONS IF MISSING
# ============================================================================
if missing > 0:
    st.markdown("---")
    st.markdown("### 🔧 How to Fix Missing Price IDs")
    
    st.warning(f"⚠️ You have {missing} Price ID(s) not configured. Follow these steps:")
    
    with st.expander("📖 Step-by-Step Instructions", expanded=True):
        st.markdown("""
        ### Step 1: Create Products in Stripe Dashboard
        
        1. Go to: https://dashboard.stripe.com/test/products (or /products for live mode)
        2. Click **"+ Add product"** for each plan
        3. Set up pricing:
           - **Subscriptions**: Set as "Recurring" with correct billing period
           - **Credit packs**: Set as "One time"
        
        ### Step 2: Get Price IDs
        
        1. Click on each product you created
        2. In the **"Pricing"** section, copy the Price ID (starts with `price_`)
        3. Make sure you copy the correct one (monthly vs annual)
        
        ### Step 3: Add to Streamlit Secrets
        
        1. Go to your Streamlit Cloud dashboard
        2. Click your app → **Settings** → **Secrets**
        3. Add the Price IDs in TOML format:
        """)
        
        st.code("""
# Subscription Plans (Recurring)
STRIPE_PRICE_PRO_MONTHLY = "price_1ABC..."
STRIPE_PRICE_PRO_ANNUAL = "price_1DEF..."
STRIPE_PRICE_AGENCY_MONTHLY = "price_1GHI..."
STRIPE_PRICE_AGENCY_ANNUAL = "price_1JKL..."
STRIPE_PRICE_ELITE_MONTHLY = "price_1MNO..."
STRIPE_PRICE_ELITE_ANNUAL = "price_1PQR..."

# Credit Packs (One-time payment)
STRIPE_PRICE_CREDITS_1000 = "price_1STU..."
STRIPE_PRICE_CREDITS_5000 = "price_1VWX..."
STRIPE_PRICE_CREDITS_10000 = "price_1YZ..."
        """, language="toml")
        
        st.markdown("""
        4. Click **Save**
        5. The app will restart automatically
        6. Refresh this page to verify
        """)
    
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        - **Use Test Mode first**: Create test Price IDs before going live
        - **Keep both modes**: Have separate Price IDs for test and live mode
        - **Document your IDs**: Keep a spreadsheet with all your Price IDs
        - **Check billing period**: Make sure monthly is "month" and annual is "year"
        - **Verify amounts**: Double-check the prices match your intended pricing
        """)
    
    with st.expander("🎯 Recommended Pricing Structure"):
        st.markdown("""
        ### Monthly Plans
        - **Pro Monthly**: €49/month
        - **Agency Monthly**: €149/month
        - **Elite Monthly**: €399/month
        
        ### Annual Plans (Save ~20%)
        - **Pro Annual**: €470/year (€39.17/month - Save €118)
        - **Agency Annual**: €1,430/year (€119.17/month - Save €358)
        - **Elite Annual**: €4,300/year (€358.33/month - Save €488)
        
        ### Credit Packs
        - **1,000 Credits**: €10 (€0.01 per credit)
        - **5,000 Credits**: €40 (€0.008 per credit - 20% off)
        - **10,000 Credits**: €75 (€0.0075 per credit - 25% off)
        """)

else:
    st.success("🎉 All Price IDs are configured correctly!")
    st.balloons()
    
    st.markdown("---")
    st.markdown("### ✅ You're ready to accept payments!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 Remember to test the checkout flow before going live")
    with col2:
        st.info("🔒 Use Stripe test cards: 4242 4242 4242 4242")

# ============================================================================
# ADDITIONAL CHECKS
# ============================================================================
st.markdown("---")
st.markdown("### 🔐 Additional Configuration Check")

additional_secrets = {
    "Stripe Secret Key": "STRIPE_SECRET_KEY",
    "Stripe Webhook Secret": "STRIPE_WEBHOOK_SECRET",
    "Supabase URL": "SUPABASE_URL",
    "Supabase Key": "SUPABASE_KEY",
    "App URL": "APP_URL"
}

col1, col2 = st.columns(2)

for idx, (name, key) in enumerate(additional_secrets.items()):
    target_col = col1 if idx % 2 == 0 else col2
    
    with target_col:
        try:
            value = st.secrets.get(key, "")
            if value:
                # Mask sensitive data
                if "SECRET" in key or "KEY" in key:
                    masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                    st.success(f"✅ **{name}**: {masked}")
                else:
                    st.success(f"✅ **{name}**: Configured")
            else:
                st.warning(f"⚠️ **{name}**: Not configured")
        except:
            st.warning(f"⚠️ **{name}**: Not configured")

# ============================================================================
# NAVIGATION
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Back to Billing", use_container_width=True):
        st.switch_page("pages/4_billing.py")

with col2:
    if st.button("🔄 Refresh Check", use_container_width=True, type="primary"):
        st.rerun()

with col3:
    if st.button("📚 Stripe Docs", use_container_width=True):
        st.markdown("[Open Stripe Documentation](https://stripe.com/docs/api/prices)")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("💡 Tip: Keep this page bookmarked for easy reference during setup")