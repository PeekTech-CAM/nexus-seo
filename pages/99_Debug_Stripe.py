"""
Debug Script: Test Your Stripe Price IDs
This will show you exactly what's wrong with each Price ID
"""

import stripe
import streamlit as st
# Add sidebar
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.sidebar import setup_sidebar
setup_sidebar()

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
st.set_page_config(page_title="Stripe Price Debugger", page_icon="🔍")

st.title("🔍 Stripe Price ID Debugger")
st.markdown("This will help identify configuration issues")

# Initialize Stripe
try:
    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    if stripe_key:
        stripe.api_key = stripe_key
        st.success("✅ Stripe initialized successfully")
    else:
        st.error("❌ STRIPE_SECRET_KEY not found in secrets")
        st.stop()
except Exception as e:
    st.error(f"❌ Error initializing Stripe: {e}")
    st.stop()

st.markdown("---")

# Test each Price ID
st.markdown("## 📋 Testing Price IDs")

price_configs = {
    "Pro Mensual (Monthly)": {
        "secret_key": "STRIPE_PRICE_PRO_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month"
    },
    "Pro Anual (Yearly)": {
        "secret_key": "STRIPE_PRICE_PRO_ANNUAL",
        "expected_type": "recurring",
        "expected_interval": "year"
    },
    "Agency Mensual (Monthly)": {
        "secret_key": "STRIPE_PRICE_AGENCY_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month"
    },
    "Agency Anual (Yearly)": {
        "secret_key": "STRIPE_PRICE_AGENCY_ANNUAL",
        "expected_type": "recurring",
        "expected_interval": "year"
    },
    "Elite Mensual (Monthly)": {
        "secret_key": "STRIPE_PRICE_ELITE_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month"
    },
    "1000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_1000",
        "expected_type": "one_time",
        "expected_interval": None
    },
    "5000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_5000",
        "expected_type": "one_time",
        "expected_interval": None
    },
    "10000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_10000",
        "expected_type": "one_time",
        "expected_interval": None
    }
}

issues_found = []
success_count = 0

for plan_name, config in price_configs.items():
    with st.expander(f"🔍 {plan_name}", expanded=False):
        secret_key = config["secret_key"]
        expected_type = config["expected_type"]
        expected_interval = config["expected_interval"]
        
        # Get Price ID from secrets
        price_id = st.secrets.get(secret_key, "")
        
        if not price_id:
            st.error(f"❌ NOT CONFIGURED")
            st.info(f"Missing secret: `{secret_key}`")
            issues_found.append(f"{plan_name}: NOT CONFIGURED")
            continue
        
        st.info(f"Price ID: `{price_id}`")
        
        # Validate Price ID format
        if not price_id.startswith("price_"):
            st.error(f"❌ INVALID FORMAT")
            st.warning(f"Price ID must start with 'price_' but got: `{price_id}`")
            if price_id.startswith("prod_"):
                st.info("💡 This is a PRODUCT ID, not a PRICE ID. Go to Stripe → Product → Copy the PRICE ID from the Pricing section")
            issues_found.append(f"{plan_name}: Invalid format (doesn't start with 'price_')")
            continue
        
        # Try to retrieve the price from Stripe
        try:
            price = stripe.Price.retrieve(price_id)
            
            # Check price type
            actual_type = price.type
            if actual_type != expected_type:
                st.error(f"❌ WRONG TYPE")
                st.warning(f"Expected: `{expected_type}` but got: `{actual_type}`")
                issues_found.append(f"{plan_name}: Wrong type ({actual_type} instead of {expected_type})")
                
                if expected_type == "recurring" and actual_type == "one_time":
                    st.info("💡 FIX: Create a NEW price with 'Recurring' billing in Stripe Dashboard")
                elif expected_type == "one_time" and actual_type == "recurring":
                    st.info("💡 FIX: Create a NEW price with 'One-off' billing in Stripe Dashboard")
                continue
            
            # Check interval for recurring prices
            if expected_type == "recurring":
                actual_interval = price.recurring.get("interval")
                if actual_interval != expected_interval:
                    st.error(f"❌ WRONG INTERVAL")
                    st.warning(f"Expected: `{expected_interval}` but got: `{actual_interval}`")
                    issues_found.append(f"{plan_name}: Wrong interval ({actual_interval} instead of {expected_interval})")
                    st.info("💡 FIX: Create a NEW price with the correct billing interval")
                    continue
                
                st.success(f"✅ VALID - Recurring: {actual_interval}")
                st.markdown(f"**Amount:** {price.currency.upper()} {price.unit_amount / 100}")
                success_count += 1
            else:
                st.success(f"✅ VALID - One-time payment")
                st.markdown(f"**Amount:** {price.currency.upper()} {price.unit_amount / 100}")
                success_count += 1
                
        except stripe.error.InvalidRequestError as e:
            st.error(f"❌ INVALID PRICE ID")
            st.warning(f"Stripe error: {str(e)}")
            st.info("💡 This Price ID doesn't exist in Stripe. Check your Stripe Dashboard")
            issues_found.append(f"{plan_name}: Price ID doesn't exist in Stripe")
        except Exception as e:
            st.error(f"❌ ERROR")
            st.warning(f"Unexpected error: {str(e)}")
            issues_found.append(f"{plan_name}: Unexpected error")

st.markdown("---")

# Summary
st.markdown("## 📊 Summary")

col1, col2 = st.columns(2)
with col1:
    st.metric("✅ Valid Prices", success_count)
with col2:
    st.metric("❌ Issues Found", len(issues_found))

if issues_found:
    st.markdown("### ❌ Issues to Fix:")
    for issue in issues_found:
        st.markdown(f"- {issue}")
    
    st.markdown("---")
    st.markdown("### 🔧 How to Fix:")
    st.markdown("""
    1. Go to **Stripe Dashboard**: https://dashboard.stripe.com/test/products
    2. For each product with issues:
       - Click on the product
       - Scroll to **"Pricing"** section
       - Click **"+ Add another price"**
       - Configure correctly:
         - **Subscriptions**: Choose "Recurring" → Monthly or Yearly
         - **Credit Packs**: Choose "One-off"
       - Click "Add price"
       - **Copy the new Price ID**
    3. Update your **Streamlit Secrets** with the new Price IDs
    4. Redeploy your app
    """)
else:
    st.success("🎉 All prices are configured correctly!")
    st.balloons()