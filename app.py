import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# --- 1. ENTERPRISE SYSTEM CORE ---
class NexusEliteEngine:
    def __init__(self):
        """Initializes connection with verified API and AI nodes."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        # Tiered Subscription Links (Connect your Stripe Dashboard)
        self.stripe_links = {
            "Pro": "https://buy.stripe.com/test_pro_tier",
            "Agency": "https://nexus.agency/contact-sales"
        }

nexus = NexusEliteEngine()

# --- 2. LUXURY COMMAND CENTER UI ---
def apply_luxury_theme():
    """Applies glassmorphism and premium typography for high-ticket authority."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono&display=swap');
        
        html, body, [class*="css"] { 
            font-family: 'Space Grotesk', sans-serif; 
            background: radial-gradient(circle at top left, #1a0505, #050505);
            color: white; 
        }
        
        /* Glassmorphism Cards */
        .premium-card {
            background: rgba(255, 75, 75, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 75, 75, 0.2);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            transition: 0.4s;
        }
        .premium-card:hover { border-color: #ff4b4b; transform: translateY(-5px); }

        /* Glowing Action Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
            color: white; border: none; font-weight: 700; height: 3.5rem; width: 100%;
            border-radius: 12px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. THE STRATEGIC PRICING TERMINAL ---
def render_pricing_gate():
    """Handles the transition from prospect to paid client."""
    apply_luxury_theme()
    st.markdown("<h1 style='text-align: center;'>🏛️ SELECT INTELLIGENCE TIER</h1>", unsafe_allow_html=True)
    
    col_free, col_pro, col_agency = st.columns(3)
    
    with col_free:
        st.markdown("<div class='premium-card'><h3>BASIC</h3><p>5 Scans / Mo</p><h2>$0</h2></div>", unsafe_allow_html=True)
        if st.button("INITIALIZE FREE ACCESS"):
            st.session_state.view = "auth"
            st.rerun()

    with col_pro:
        st.markdown("<div class='premium-card' style='border-color: #ff4b4b;'><h3>PRO</h3><p>500 Scans / Mo</p><h2>$99</h2></div>", unsafe_allow_html=True)
        st.link_button("UPGRADE TO PRO (STRIPE)", nexus.stripe_links["Pro"])

    with col_agency:
        st.markdown("<div class='premium-card'><h3>AGENCY</h3><p>UNLIMITED SCANS</p><h2>CUSTOM</h2></div>", unsafe_allow_html=True)
        st.link_button("CONTACT SALES", nexus.stripe_links["Agency"])
    
    st.divider()
    if st.button("EXPLORE SYSTEM DEMO FIRST"):
        st.session_state.view = "demo"
        st.rerun()

# --- 4. THE LIVE DEMO NODE ---
def render_demo():
    """Simulated environment to showcase 'Wow' factor without registration."""
    st.info("🛰️ SIMULATED NODE: Viewing global intelligence vectors. Register for real-time analysis.")
    fig = go.Figure(go.Scattergeo(lat=[31.7, -14.2, 37.0], lon=[-7.1, -51.9, -95.7], mode='markers', marker=dict(color='#ff4b4b', size=12)))
    fig.update_geos(projection_type="orthographic", showland=True, landcolor="#111", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)
    if st.button("TERMINATE DEMO & REGISTER"):
        st.session_state.view = "auth"
        st.rerun()

# --- 5. THE AUTHORIZATION GATE ---
def render_auth_gate():
    """Handles secure onboarding and fixes Foreign Key errors."""
    apply_luxury_theme()
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🔐 Access Terminal")
        mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        
        if st.button("AUTHORIZE ACCESS"):
            try:
                if mode == "Register Organization":
                    nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                    st.success("✅ Profile Initialized. Verification bypassed via Supabase override.")
                else:
                    auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    # Atomic upsert to prevent duplicate key errors
                    nexus.supabase.table("profiles").upsert({"id": auth.user.id, "email": email, "plan_tier": "Starter"}).execute()
                    st.session_state.user = auth.user
                    st.rerun()
            except Exception as e:
                st.error(f"Access Denied: {e}")
    with col_r:
        st.markdown("<div class='premium-card'><h3>💎 Agency Elite</h3><p>Strategic white-label intelligence and custom data depth.</p></div>", unsafe_allow_html=True)

# --- 6. PRODUCTION ROUTER ---
def main():
    if "user" in st.session_state:
        # FULL DASHBOARD VIEW
        apply_luxury_theme()
        st.sidebar.title("🏛️ Terminal Active")
        st.title("🛰️ Strategy Deployment Terminal")
        st.sidebar.write(f"Node: {st.session_state.user.email}")
        
        # Intelligence KPIs
        c1, c2, c3 = st.columns(3)
        c1.metric("Nodes", "1,842", "+12")
        c2.metric("ROI", "342%", "🔥")
        c3.metric("Networks", "94", "+5")
        
        if st.sidebar.button("LOGOUT"):
            nexus.supabase.auth.sign_out()
            del st.session_state.user
            st.rerun()
    else:
        if "view" not in st.session_state: st.session_state.view = "pricing"
        
        if st.session_state.view == "pricing": render_pricing_gate()
        elif st.session_state.view == "demo": render_demo()
        elif st.session_state.view == "auth": render_auth_gate()

if __name__ == "__main__":
    main()
