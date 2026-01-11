"""
Debug Script: Test Your Stripe Price IDs
This will show you exactly what's wrong with each Price ID
"""

import streamlit as st
import stripe

# ============================================================================
# PAGE CONFIG - MUST BE FIRST (only once!)
# ============================================================================
st.set_page_config(
    page_title="Stripe Price Debugger - Nexus SEO",
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
    add_page_navigation("Stripe Debugger", "🔍")
except Exception as e:
    st.warning(f"⚠️ Navigation component error: {e}")

# ============================================================================
# HEADER
# ============================================================================
st.title("🔍 Stripe Price ID Debugger")
st.markdown("This will help identify configuration issues with your Stripe Price IDs")
st.markdown("---")

# ============================================================================
# INITIALIZE STRIPE
# ============================================================================
try:
    stripe_key = st.secrets.get("STRIPE_SECRET_KEY")
    if stripe_key:
        stripe.api_key = stripe_key
        st.success("✅ Stripe initialized successfully")
        
        # Show masked key
        masked_key = f"{stripe_key[:7]}...{stripe_key[-4:]}"
        st.caption(f"Using key: {masked_key}")
    else:
        st.error("❌ STRIPE_SECRET_KEY not found in secrets")
        st.info("Add STRIPE_SECRET_KEY to your Streamlit secrets")
        st.stop()
except Exception as e:
    st.error(f"❌ Error initializing Stripe: {e}")
    st.stop()

st.markdown("---")

# ============================================================================
# TEST EACH PRICE ID
# ============================================================================
st.markdown("## 📋 Testing Price IDs")

price_configs = {
    "Pro Monthly": {
        "secret_key": "STRIPE_PRICE_PRO_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month",
        "expected_amount": 4900  # €49 in cents
    },
    "Pro Annual": {
        "secret_key": "STRIPE_PRICE_PRO_ANNUAL",
        "expected_type": "recurring",
        "expected_interval": "year",
        "expected_amount": 47000  # €470 in cents
    },
    "Agency Monthly": {
        "secret_key": "STRIPE_PRICE_AGENCY_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month",
        "expected_amount": 14900  # €149 in cents
    },
    "Agency Annual": {
        "secret_key": "STRIPE_PRICE_AGENCY_ANNUAL",
        "expected_type": "recurring",
        "expected_interval": "year",
        "expected_amount": 143000  # €1,430 in cents
    },
    "Elite Monthly": {
        "secret_key": "STRIPE_PRICE_ELITE_MONTHLY",
        "expected_type": "recurring",
        "expected_interval": "month",
        "expected_amount": 39900  # €399 in cents
    },
    "Elite Annual": {
        "secret_key": "STRIPE_PRICE_ELITE_ANNUAL",
        "expected_type": "recurring",
        "expected_interval": "year",
        "expected_amount": 430000  # €4,300 in cents
    },
    "1,000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_1000",
        "expected_type": "one_time",
        "expected_interval": None,
        "expected_amount": 1000  # €10 in cents
    },
    "5,000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_5000",
        "expected_type": "one_time",
        "expected_interval": None,
        "expected_amount": 4000  # €40 in cents
    },
    "10,000 Credits": {
        "secret_key": "STRIPE_PRICE_CREDITS_10000",
        "expected_type": "one_time",
        "expected_interval": None,
        "expected_amount": 7500  # €75 in cents
    }
}

issues_found = []
success_count = 0

for plan_name, config in price_configs.items():
    with st.expander(f"🔍 {plan_name}", expanded=False):
        secret_key = config["secret_key"]
        expected_type = config["expected_type"]
        expected_interval = config["expected_interval"]
        expected_amount = config.get("expected_amount")
        
        # Get Price ID from secrets
        try:
            price_id = st.secrets.get(secret_key, "")
        except:
            price_id = ""
        
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
            issues_found.append(f"{plan_name}: Invalid format")
            continue
        
        # Try to retrieve the price from Stripe
        try:
            price = stripe.Price.retrieve(price_id)
            
            # Check if active
            if not price.active:
                st.warning("⚠️ Price is INACTIVE in Stripe")
            
            # Check price type
            actual_type = price.type
            if actual_type != expected_type:
                st.error(f"❌ WRONG TYPE")
                st.warning(f"Expected: `{expected_type}` but got: `{actual_type}`")
                issues_found.append(f"{plan_name}: Wrong type ({actual_type})")
                
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
                    issues_found.append(f"{plan_name}: Wrong interval ({actual_interval})")
                    st.info("💡 FIX: Create a NEW price with the correct billing interval")
                    continue
                
                # Show details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.success(f"✅ Type: {actual_type}")
                with col2:
                    st.success(f"✅ Interval: {actual_interval}")
                with col3:
                    amount_display = f"{price.currency.upper()} {price.unit_amount / 100:.2f}"
                    st.success(f"✅ Amount: {amount_display}")
                
                # Check amount if specified
                if expected_amount and price.unit_amount != expected_amount:
                    st.warning(f"⚠️ Amount mismatch: Expected {expected_amount/100:.2f}, got {price.unit_amount/100:.2f}")
                
                success_count += 1
            else:
                # One-time payment
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ Type: One-time")
                with col2:
                    amount_display = f"{price.currency.upper()} {price.unit_amount / 100:.2f}"
                    st.success(f"✅ Amount: {amount_display}")
                
                # Check amount if specified
                if expected_amount and price.unit_amount != expected_amount:
                    st.warning(f"⚠️ Amount mismatch: Expected {expected_amount/100:.2f}, got {price.unit_amount/100:.2f}")
                
                success_count += 1
                
        except stripe.error.InvalidRequestError as e:
            st.error(f"❌ INVALID PRICE ID")
            st.warning(f"Stripe error: {str(e)}")
            st.info("💡 This Price ID doesn't exist in Stripe. Check your Stripe Dashboard")
            issues_found.append(f"{plan_name}: Price ID doesn't exist")
        except stripe.error.AuthenticationError as e:
            st.error(f"❌ AUTHENTICATION ERROR")
            st.warning("Your Stripe API key is invalid")
            st.stop()
        except Exception as e:
            st.error(f"❌ ERROR")
            st.warning(f"Unexpected error: {str(e)}")
            issues_found.append(f"{plan_name}: Unexpected error")

st.markdown("---")

# ============================================================================
# SUMMARY
# ============================================================================
st.markdown("## 📊 Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("✅ Valid Prices", success_count)

with col2:
    st.metric("❌ Issues Found", len(issues_found))

with col3:
    total = len(price_configs)
    percentage = (success_count / total * 100) if total > 0 else 0
    st.metric("📊 Success Rate", f"{percentage:.0f}%")

if issues_found:
    st.markdown("---")
    st.markdown("### ❌ Issues to Fix:")
    for issue in issues_found:
        st.markdown(f"- {issue}")
    
    st.markdown("---")
    
    with st.expander("🔧 How to Fix Issues", expanded=True):
        st.markdown("""
        ### Step-by-Step Fix Guide:
        
        1. **Go to Stripe Dashboard**: 
           - Test mode: https://dashboard.stripe.com/test/products
           - Live mode: https://dashboard.stripe.com/products
        
        2. **For each product with issues:**
           - Click on the product name
           - Scroll to **"Pricing"** section
           - Click **"+ Add another price"**
        
        3. **Configure the price correctly:**
           
           **For Subscriptions (Pro, Agency, Elite):**
           - Set as **"Recurring"**
           - Choose correct interval: **Monthly** or **Yearly**
           - Enter the amount
           
           **For Credit Packs:**
           - Set as **"One-off"**
           - Enter the amount
        
        4. **Save and copy the Price ID:**
           - Click "Add price"
           - Copy the new **Price ID** (starts with `price_`)
        
        5. **Update Streamlit Secrets:**
           - Go to Streamlit Cloud → Settings → Secrets
           - Update the Price ID
           - Save and reboot app
        
        6. **Re-run this debugger** to verify
        """)
    
    with st.expander("💡 Pro Tips"):
        st.markdown("""
        - **Don't edit existing prices** - Create new ones instead
        - **Keep test and live prices separate**
        - **Document your Price IDs** in a spreadsheet
        - **Test checkout flow** before going live
        - **Use Stripe test cards**: 4242 4242 4242 4242
        """)
else:
    st.success("🎉 All prices are configured correctly!")
    st.balloons()
    
    st.info("💡 Your billing system is ready! Test the checkout flow next.")

# ============================================================================
# ACTIONS
# ============================================================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Re-run Test", use_container_width=True, type="primary"):
        st.rerun()

with col2:
    if st.button("📊 View Price Check", use_container_width=True):
        try:
            st.switch_page("pages/check_prices.py")
        except:
            st.info("Navigate to Price Check page")

with col3:
    if st.button("💳 Test Billing Page", use_container_width=True):
        try:
            st.switch_page("pages/4_billing.py")
        except:
            st.info("Navigate to Billing page")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("🔒 Running in test mode - no real charges")
st.caption("💡 This is a debug tool - remove before production")