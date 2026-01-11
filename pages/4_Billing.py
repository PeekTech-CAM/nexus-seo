"""
Billing & Upgrade Page - Fixed Version
"""

import streamlit as st
import stripe
import os
from supabase import create_client

# ============================================================================
# PAGE CONFIG - MUST BE FIRST (only once!)
# ============================================================================
st.set_page_config(
    page_title="Billing - Nexus SEO",
    page_icon="💳",
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
add_page_navigation("Billing", "💳")

# ============================================================================
# INITIALIZE STRIPE
# ============================================================================
@st.cache_resource
def init_stripe():
    try:
        stripe_key = st.secrets.get("STRIPE_SECRET_KEY") or os.getenv('STRIPE_SECRET_KEY')
        if stripe_key:
            stripe.api_key = stripe_key
            return True
        return False
    except Exception as e:
        st.error(f"Stripe error: {e}")
        return False

# ============================================================================
# INITIALIZE SUPABASE
# ============================================================================
@st.cache_resource
def get_supabase():
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv('SUPABASE_URL')
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_KEY") or os.getenv('SUPABASE_KEY')
        if url and key:
            return create_client(url, key)
        return None
    except Exception as e:
        st.error(f"Supabase error: {e}")
        return None

# ============================================================================
# AUTHENTICATION CHECK
# ============================================================================
if 'user' not in st.session_state or not st.session_state.user:
    st.warning("⚠️ Please log in to access billing")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Initialize services
stripe_ready = init_stripe()
supabase = get_supabase()

if not stripe_ready:
    st.error("⚠️ Payment system not configured. Please add STRIPE_SECRET_KEY to secrets.")
    st.stop()

# ============================================================================
# GET USER INFO
# ============================================================================
user = st.session_state.user
if isinstance(user, dict):
    user_id = user.get('id')
    user_email = user.get('email')
else:
    user_id = user.id
    user_email = user.email

# Fetch user profile
user_profile = None
if supabase:
    try:
        response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        user_profile = response.data if response.data else None
    except Exception as e:
        st.error(f"Error loading profile: {e}")

# ============================================================================
# HEADER & CURRENT PLAN INFO
# ============================================================================
st.title("💳 Billing & Upgrades")
st.markdown("Choose your plan and manage your subscription")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    current_tier = user_profile.get('tier', 'FREE').upper() if user_profile else 'FREE'
    st.metric("Current Plan", current_tier)

with col2:
    credits = user_profile.get('credits_balance', 0) if user_profile else 0
    st.metric("Credits", f"{credits:,}")

with col3:
    scans_used = user_profile.get('monthly_scans_used', 0) if user_profile else 0
    scan_limit = user_profile.get('monthly_scan_limit', 10) if user_profile else 10
    st.metric("Scans Used", f"{scans_used}/{scan_limit}")

with col4:
    status = user_profile.get('subscription_status', 'inactive') if user_profile else 'inactive'
    status_emoji = "✅" if status == 'active' else "⏸️"
    st.metric("Status", f"{status_emoji} {status.title()}")

st.markdown("---")

# ============================================================================
# SUBSCRIPTION PLANS
# ============================================================================
st.markdown("### 🎯 Subscription Plans")

# Get app URL from secrets or use default
app_url = st.secrets.get("APP_URL", "https://nexus-seo-fobcg4apinvom9hzpjnfyb.streamlit.app")

plans = [
    {
        'name': 'Pro Monthly',
        'price': '€49',
        'period': 'month',
        'price_id': st.secrets.get("STRIPE_PRICE_PRO_MONTHLY", ""),
        'features': ['50 scans/month', '10,000 credits', 'PDF exports', 'Email reports', 'Priority support'],
        'tier': 'pro'
    },
    {
        'name': 'Pro Annual',
        'price': '€470',
        'period': 'year',
        'save': 'Save €118/year',
        'price_id': st.secrets.get("STRIPE_PRICE_PRO_ANNUAL", ""),
        'features': ['50 scans/month', '120,000 credits/year', 'PDF exports', 'Email reports', 'Priority support', '🎁 2 months FREE'],
        'recommended': True,
        'tier': 'pro'
    },
    {
        'name': 'Agency Monthly',
        'price': '€149',
        'period': 'month',
        'price_id': st.secrets.get("STRIPE_PRICE_AGENCY_MONTHLY", ""),
        'features': ['200 scans/month', '50,000 credits', 'White-label reports', 'Team collaboration', 'API access', 'Dedicated support'],
        'tier': 'agency'
    },
    {
        'name': 'Agency Annual',
        'price': '€1,430',
        'period': 'year',
        'save': 'Save €358/year',
        'price_id': st.secrets.get("STRIPE_PRICE_AGENCY_ANNUAL", ""),
        'features': ['200 scans/month', '600,000 credits/year', 'White-label reports', 'Team collaboration', 'API access', '🎁 2 months FREE'],
        'tier': 'agency'
    },
    {
        'name': 'Elite Monthly',
        'price': '€399',
        'period': 'month',
        'price_id': st.secrets.get("STRIPE_PRICE_ELITE_MONTHLY", ""),
        'features': ['Unlimited scans', '200,000 credits', 'Everything in Agency', 'Dedicated account manager', 'Custom SLA', 'Custom integrations'],
        'tier': 'elite'
    },
    {
        'name': 'Elite Annual',
        'price': '€4,300',
        'period': 'year',
        'save': 'Save €488/year',
        'price_id': st.secrets.get("STRIPE_PRICE_ELITE_ANNUAL", ""),
        'features': ['Unlimited scans', '2.4M credits/year', 'Everything in Agency', 'Dedicated account manager', 'Custom SLA', 'Custom integrations', '🎁 2 months FREE'],
        'tier': 'elite'
    }
]

# Display plans in rows - First row (3 plans)
row1_plans = plans[:3]
cols = st.columns(3)

for idx, plan in enumerate(row1_plans):
    with cols[idx]:
        if plan.get('recommended'):
            st.markdown("### ⭐ **MOST POPULAR**")
            st.markdown(f"## 🚀 {plan['name']}")
        else:
            st.markdown(f"## {plan['name']}")
        
        st.markdown(f"# {plan['price']}")
        st.markdown(f"*per {plan['period']}*")
        
        if plan.get('save'):
            st.success(plan['save'])
        
        st.markdown("---")
        
        for feature in plan['features']:
            st.markdown(f"✅ {feature}")
        
        st.markdown("---")
        
        button_key = f"btn_{idx}"
        button_type = "primary" if plan.get('recommended') else "secondary"
        
        if st.button(f"Select {plan['name']}", key=button_key, type=button_type, use_container_width=True):
            if not plan['price_id']:
                st.error(f"⚠️ {plan['name']} not configured yet. Please add STRIPE_PRICE_{plan['tier'].upper()}_{plan['period'].upper()} to secrets.")
            else:
                with st.spinner("Creating secure checkout session..."):
                    try:
                        checkout_session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price': plan['price_id'],
                                'quantity': 1
                            }],
                            mode='subscription',
                            success_url=f"{app_url}/?success=true&plan={plan['tier']}",
                            cancel_url=f"{app_url}/?cancelled=true",
                            client_reference_id=user_id,
                            customer_email=user_email,
                            metadata={
                                'plan_name': plan['name'],
                                'user_id': user_id,
                                'tier': plan['tier']
                            }
                        )
                        
                        st.success("✅ Checkout created! Redirecting...")
                        st.markdown(f"[Click here if not redirected automatically]({checkout_session.url})")
                        st.markdown(f'<meta http-equiv="refresh" content="1;url={checkout_session.url}">', unsafe_allow_html=True)
                        
                    except stripe.error.StripeError as e:
                        st.error(f"❌ Payment error: {str(e)}")
                    except Exception as e:
                        st.error(f"❌ Unexpected error: {str(e)}")

# Second row (remaining 3 plans)
row2_plans = plans[3:]
if row2_plans:
    cols = st.columns(3)
    for idx, plan in enumerate(row2_plans):
        with cols[idx]:
            st.markdown(f"## {plan['name']}")
            st.markdown(f"# {plan['price']}")
            st.markdown(f"*per {plan['period']}*")
            
            if plan.get('save'):
                st.success(plan['save'])
            
            st.markdown("---")
            
            for feature in plan['features']:
                st.markdown(f"✅ {feature}")
            
            st.markdown("---")
            
            button_key = f"btn_{idx + 3}"
            
            if st.button(f"Select {plan['name']}", key=button_key, use_container_width=True):
                if not plan['price_id']:
                    st.error(f"⚠️ {plan['name']} not configured yet.")
                else:
                    with st.spinner("Creating secure checkout session..."):
                        try:
                            checkout_session = stripe.checkout.Session.create(
                                payment_method_types=['card'],
                                line_items=[{
                                    'price': plan['price_id'],
                                    'quantity': 1
                                }],
                                mode='subscription',
                                success_url=f"{app_url}/?success=true&plan={plan['tier']}",
                                cancel_url=f"{app_url}/?cancelled=true",
                                client_reference_id=user_id,
                                customer_email=user_email,
                                metadata={
                                    'plan_name': plan['name'],
                                    'user_id': user_id,
                                    'tier': plan['tier']
                                }
                            )
                            
                            st.success("✅ Redirecting to checkout...")
                            st.markdown(f"[Click here if not redirected]({checkout_session.url})")
                            st.markdown(f'<meta http-equiv="refresh" content="1;url={checkout_session.url}">', unsafe_allow_html=True)
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

# ============================================================================
# CREDIT PACKS
# ============================================================================
st.markdown("---")
st.markdown("### 💎 One-Time Credit Packs")

credit_packs = [
    {
        'name': '1,000 Credits',
        'price': '€10',
        'credits': 1000,
        'price_id': st.secrets.get("STRIPE_PRICE_CREDITS_1000", ""),
        'per_credit': '€0.01'
    },
    {
        'name': '5,000 Credits',
        'price': '€40',
        'credits': 5000,
        'price_id': st.secrets.get("STRIPE_PRICE_CREDITS_5000", ""),
        'badge': '⭐ BEST VALUE',
        'per_credit': '€0.008'
    },
    {
        'name': '10,000 Credits',
        'price': '€75',
        'credits': 10000,
        'price_id': st.secrets.get("STRIPE_PRICE_CREDITS_10000", ""),
        'per_credit': '€0.0075'
    }
]

cols = st.columns(3)

for idx, pack in enumerate(credit_packs):
    with cols[idx]:
        if pack.get('badge'):
            st.success(pack['badge'])
        
        st.markdown(f"### {pack['name']}")
        st.markdown(f"## {pack['price']}")
        st.caption(f"{pack['per_credit']} per credit")
        
        st.markdown("---")
        
        if st.button(f"Buy {pack['name']}", key=f"credit_{idx}", use_container_width=True):
            if not pack['price_id']:
                st.error("⚠️ Not configured yet. Add STRIPE_PRICE_CREDITS_{credits} to secrets.")
            else:
                with st.spinner("Creating checkout..."):
                    try:
                        checkout_session = stripe.checkout.Session.create(
                            payment_method_types=['card'],
                            line_items=[{
                                'price': pack['price_id'],
                                'quantity': 1
                            }],
                            mode='payment',
                            success_url=f"{app_url}/?success=true&credits={pack['credits']}",
                            cancel_url=f"{app_url}/?cancelled=true",
                            client_reference_id=user_id,
                            customer_email=user_email,
                            metadata={
                                'credits': pack['credits'],
                                'user_id': user_id,
                                'type': 'credit_pack'
                            }
                        )
                        
                        st.success("✅ Redirecting to checkout...")
                        st.markdown(f"[Click here if not redirected]({checkout_session.url})")
                        st.markdown(f'<meta http-equiv="refresh" content="1;url={checkout_session.url}">', unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# ============================================================================
# FAQ
# ============================================================================
st.markdown("---")

with st.expander("❓ Frequently Asked Questions"):
    st.markdown("""
    **Q: Can I change plans anytime?**  
    A: Yes! You can upgrade or downgrade your plan at any time. Changes take effect immediately.
    
    **Q: Do credits expire?**  
    A: No, credits never expire. Use them whenever you need them.
    
    **Q: Can I cancel my subscription?**  
    A: Yes, you can cancel anytime from the billing portal. You'll keep access until the end of your billing period.
    
    **Q: What payment methods do you accept?**  
    A: We accept all major credit cards through Stripe's secure payment processing.
    
    **Q: Is my payment information secure?**  
    A: Yes! We use Stripe for payment processing. We never store your card details.
    
    **Q: Do you offer refunds?**  
    A: We offer a 14-day money-back guarantee on annual plans. Contact support for details.
    """)

# ============================================================================
# BILLING PORTAL (for existing subscribers)
# ============================================================================
if user_profile and user_profile.get('stripe_customer_id'):
    st.markdown("---")
    st.markdown("### ⚙️ Manage Your Subscription")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔧 Open Billing Portal", use_container_width=True):
            try:
                portal_session = stripe.billing_portal.Session.create(
                    customer=user_profile['stripe_customer_id'],
                    return_url=app_url
                )
                st.success("✅ Opening billing portal...")
                st.markdown(f"[Click here to manage your subscription]({portal_session.url})")
                st.markdown(f'<meta http-equiv="refresh" content="1;url={portal_session.url}">', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        st.info("💡 Use the billing portal to update payment methods, view invoices, and manage your subscription.")

# ============================================================================
# SUCCESS/CANCEL MESSAGES
# ============================================================================
if 'success' in st.query_params:
    st.success("🎉 Payment successful! Your account has been upgraded.")
    st.balloons()

if 'cancelled' in st.query_params:
    st.info("ℹ️ Payment was cancelled. No charges were made.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("💳 Secure payments powered by Stripe | 🔒 Your data is encrypted and secure | 🌍 Prices shown in EUR")