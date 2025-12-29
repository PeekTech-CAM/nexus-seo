import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import json
import re

# --- 1. ENTERPRISE INITIALIZATION ---
@st.cache_resource
def init_enterprise_system():
    # Use the API URL to fix the 405 error from your screenshot
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_enterprise_system()

# --- 2. HIGH-TICKET PRICING LOGIC ---
# Updated to your new premium values
PREMIUM_PLANS = {
    "Starter": {"price": 100, "credits": 5, "viz": "Standard"},
    "Pro": {"price": 1500, "credits": 9999, "viz": "Advanced"},
    "Agency": {"price": 3000, "credits": 9999, "viz": "White-Label"}
}

# --- 3. THE "WOW" VISUALIZATION ENGINE ---
def render_enterprise_radar(metrics):
    """Motion-enabled Radar Chart to justify €3,000 pricing."""
    st.markdown("### 🛰️ Competitive Strategic Intelligence")
    
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Current Strategy',
        line_color='#ff4b4b',
        fillcolor='rgba(255, 75, 75, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10], color="white"),
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "white", 'size': 14},
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. SECURE AUTHENTICATION ---
def render_auth():
    st.sidebar.markdown("# 🏛️ NEXUS ELITE")
    email = st.sidebar.text_input("Corporate ID")
    pwd = st.sidebar.text_input("Security Token", type="password")
    
    if st.sidebar.button("Authorize Organization"):
        try:
            # Secure login via Supabase Auth
            res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = res.user
            st.rerun()
        except:
            st.sidebar.error("Access Denied. Check Enterprise Credentials.")

# --- 5. MAIN EXECUTION ---
if "user" not in st.session_state:
    render_auth()
    st.title("⚡ NEXUS Strategic Intelligence")
    st.subheader("The world's most advanced SEO prioritization engine for high-ticket agencies.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070")
else:
    # Production Sync from 'profiles' table
    profile = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    tier = profile['plan_tier']
    
    st.sidebar.success(f"Active License: {tier}")
    if tier != "Agency":
        st.sidebar.markdown("---")
        st.sidebar.link_button(f"💎 Upgrade to Agency (€3,000)", "https://buy.stripe.com/agency_link")

    st.title("🏛️ Strategic Analysis Terminal")
    target_site = st.text_input("Global Domain Analysis (e.g., https://tesla.com):")

    if st.button("🚀 EXECUTE ELITE INTELLIGENCE SCAN") and target_site:
        if profile['credits'] <= 0 and tier == "Demo":
            st.error("Quota Exceeded. Please upgrade to the €100 Starter plan.")
        else:
            with st.spinner("Analyzing Global Data Nodes..."):
                # Simulation of Advanced AI JSON output
                strategic_metrics = {
                    "Technical SEO": 9,
                    "UX Authority": 7,
                    "Backlink Velocity": 8,
                    "Content ROI": 6,
                    "Mobile Dominance": 9
                }
                
                render_enterprise_radar(strategic_metrics)
                st.markdown("### 📝 Executive Strategic Roadmap")
                st.write("Detailed high-level report continues here...")

    if st.sidebar.button("Terminate Session"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
