"""
NEXUS SEO INTELLIGENCE - Billing Page (Fixed for Demo Users)
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Billing & Subscription",
    page_icon="💳",
    layout="wide"
)

# Check if user is logged in
if 'user' not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Get user info safely
user_email = st.session_state.user.email
user_plan = st.session_state.get('user_plan', 'demo')
is_demo = (st.session_state.user.id == 'demo_user')

# Stripe Payment Links
YEARLY_PAYMENT_LINK = "https://buy.stripe.com/4gM5kD2R74kPcjL3o3ao804"
MONTHLY_PAYMENT_LINK = "https://buy.stripe.com/dRm4gz3VbeZt0B36Afao803"

CREDITS_1000_LINK = "https://buy.stripe.com/test/1000credits"
CREDITS_5000_LINK = "https://buy.stripe.com/test/5000credits"
CREDITS_10000_LINK = "https://buy.stripe.com/test/10000credits"

# CSS
st.markdown("""
<style>
    .plan-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .price-tag {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    .savings-badge {
        background: #10b981;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        font-weight: bold;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
try:
    st.image("logo.png", width=100)
except:
    pass

st.title("💳 Billing & Subscription")
st.markdown("### Choose the perfect plan for your SEO needs")

# User info
st.info(f"👤 Logged in as: **{user_email}** | Current Plan: **{user_plan.upper()}**")

if is_demo:
    st.warning("🎮 **Demo Mode** - Upgrade to unlock all features and unlimited scans!")

st.markdown("---")

# Billing cycle selection
st.markdown("## 🎯 Select Your Billing Cycle")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="plan-card">
        <h2>💰 Annual Billing</h2>
        <div class="savings-badge">💎 SAVE UP TO 20%</div>
        <div class="price-tag">Best Value!</div>
        
        <div style="margin: 1rem 0; font-size: 1.1rem;">
        <strong>What's included:</strong><br/>
        ✅ Pro Yearly - €2,457/year<br/>
        ✅ Agency Yearly - €1,430/year<br/>
        ✅ Elite Yearly - Premium features<br/>
        <br/>
        <strong>All plans include:</strong><br/>
        🎨 White label reports<br/>
        🚀 Priority support<br/>
        🔓 All features unlocked<br/>
        💳 One payment per year<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    if st.button("🎯 View Yearly Plans", type="primary", use_container_width=True, key="yearly_btn"):
        st.markdown(f"""
        ### 🔗 Opening Stripe Checkout...
        
        Click the link below if it doesn't open automatically:
        
        **[→ Open Yearly Plans Checkout]({YEARLY_PAYMENT_LINK})**
        """)
        st.markdown(f'<meta http-equiv="refresh" content="1; url={YEARLY_PAYMENT_LINK}">', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="plan-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
        <h2>📅 Monthly Billing</h2>
        <div class="savings-badge" style="background: #3b82f6;">✨ FLEXIBLE</div>
        <div class="price-tag">Pay as you go</div>
        
        <div style="margin: 1rem 0; font-size: 1.1rem;">
        <strong>What's included:</strong><br/>
        ✅ Pro Monthly - Flexible pricing<br/>
        ✅ Agency Monthly - Scale easily<br/>
        ✅ Elite Monthly - No commitment<br/>
        <br/>
        <strong>All plans include:</strong><br/>
        🎨 White label reports<br/>
        🚀 Priority support<br/>
        🔓 All features unlocked<br/>
        🔄 Cancel anytime<br/>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    if st.button("📆 View Monthly Plans", use_container_width=True, key="monthly_btn"):
        st.markdown(f"""
        ### 🔗 Opening Stripe Checkout...
        
        Click the link below if it doesn't open automatically:
        
        **[→ Open Monthly Plans Checkout]({MONTHLY_PAYMENT_LINK})**
        """)
        st.markdown(f'<meta http-equiv="refresh" content="1; url={MONTHLY_PAYMENT_LINK}">', unsafe_allow_html=True)

st.markdown("---")

# Plan comparison
st.markdown("## 📊 Compare Plans")

with st.expander("🔍 Detailed Plan Comparison", expanded=False):
    st.markdown("""
    | Feature | Pro | Agency | Elite |
    |---------|-----|--------|-------|
    | **SEO Cases/Month** | 50 | 200 | Unlimited |
    | **Annual Credits** | 100,000 | 500,000 | 10,000,000 |
    | **AI Agents** | 2 | 3 | 4 |
    | **White Label Reports** | ✅ | ✅ | ✅ |
    | **Priority Support** | ✅ | ✅ | ✅ |
    | **Team Collaboration** | ❌ | ✅ | ✅ |
    | **Dedicated Manager** | ❌ | ❌ | ✅ |
    | **API Access** | ❌ | ✅ | ✅ |
    | **Custom Integrations** | ❌ | ❌ | ✅ |
    | **PDF Export** | ❌ | ✅ | ✅ |
    """)

# Credit Packs
st.markdown("---")
st.markdown("## 💎 Buy Credit Packs")
st.info("💡 One-time purchases • Never expire • Work with any plan")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="border: 2px solid #6366f1; border-radius: 15px; padding: 2rem; text-align: center; background: white;">
        <h3>🔷 Starter Pack</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #6366f1; margin: 1rem 0;">
            €10.00
        </div>
        <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">
            1,000 Credits
        </div>
        <p style="color: #6b7280;">
            ✅ One-time purchase<br/>
            ✅ Never expires<br/>
            ✅ Instant delivery
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("💳 Buy 1,000 Credits", use_container_width=True, key="credits_1000"):
        st.markdown(f"**[→ Complete Purchase]({CREDITS_1000_LINK})**")

with col2:
    st.markdown("""
    <div style="border: 3px solid #8b5cf6; border-radius: 15px; padding: 2rem; text-align: center; background: linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%);">
        <div style="background: #8b5cf6; color: white; padding: 0.25rem 1rem; border-radius: 20px; display: inline-block; margin-bottom: 1rem; font-weight: bold;">
            🔥 POPULAR
        </div>
        <h3>🔶 Growth Pack</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #8b5cf6; margin: 1rem 0;">
            €40.00
        </div>
        <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">
            5,000 Credits
        </div>
        <p style="color: #6b7280;">
            ✅ One-time purchase<br/>
            ✅ Never expires<br/>
            ✅ Instant delivery
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("💳 Buy 5,000 Credits", use_container_width=True, type="primary", key="credits_5000"):
        st.markdown(f"**[→ Complete Purchase]({CREDITS_5000_LINK})**")

with col3:
    st.markdown("""
    <div style="border: 2px solid #10b981; border-radius: 15px; padding: 2rem; text-align: center; background: white;">
        <h3>🔸 Enterprise Pack</h3>
        <div style="font-size: 2.5rem; font-weight: bold; color: #10b981; margin: 1rem 0;">
            €75.00
        </div>
        <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">
            10,000 Credits
        </div>
        <p style="color: #6b7280;">
            ✅ One-time purchase<br/>
            ✅ Never expires<br/>
            ✅ Instant delivery
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("💳 Buy 10,000 Credits", use_container_width=True, key="credits_10000"):
        st.markdown(f"**[→ Complete Purchase]({CREDITS_10000_LINK})**")

# FAQ
st.markdown("---")
st.markdown("## ❓ Frequently Asked Questions")

with st.expander("💰 How much can I save with annual billing?"):
    st.markdown("""
    Annual billing offers up to **20% savings** compared to monthly billing:
    - Pay once a year instead of 12 times
    - Lock in your rate for the full year
    - Get premium features at a lower cost
    """)

with st.expander("🔄 Can I change plans later?"):
    st.markdown("""
    Yes! You can:
    - Upgrade to a higher plan anytime
    - Switch between monthly and yearly billing
    - Changes take effect on your next billing cycle
    """)

with st.expander("💳 What payment methods do you accept?"):
    st.markdown("""
    We accept all major payment methods through Stripe:
    - Credit/Debit cards (Visa, Mastercard, Amex)
    - Apple Pay
    - Google Pay
    - Bank transfers (for annual plans)
    """)

# Back button
st.markdown("---")
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")