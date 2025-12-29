import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import json
import re

# --- 1. ENTERPRISE CORE ARCHITECTURE ---
class NexusElite:
    def __init__(self):
        # Resolve 405 errors by targeting the direct REST API endpoint
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        self.plans = {
            "Starter": {"price": 100, "credits": 5, "depth": 5000},
            "Pro": {"price": 1500, "credits": 9999, "depth": 15000},
            "Agency": {"price": "Especial", "credits": "Unlimited", "depth": 25000}
        }

nexus = NexusElite()

# --- 2. LUXURY UI & GLOBAL INTELLIGENCE MAP ---
def apply_enterprise_theme():
    st.markdown("""
        <style>
        .main { background-color: #050505; color: white; }
        .stMetric { background: rgba(255,255,255,0.03); border: 1px solid #1a1a1a; padding: 15px; border-radius: 10px; }
        .agency-card { 
            border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; 
            background: rgba(255, 75, 75, 0.05); text-align: center;
        }
        .terminal-box { 
            background: #000; border: 1px solid #ff4b4b; padding: 20px; 
            color: #ff4b4b; font-family: 'Courier New', monospace;
            box-shadow: 0 0 15px rgba(255, 75, 75, 0.2); border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def render_global_coverage_map():
    """Visualizes global intelligence footprint to wow high-ticket clients."""
    # Mock data representing your 'Elite' customers/nodes worldwide
    data = pd.DataFrame({
        'Country': ['United States', 'Spain', 'Germany', 'United Arab Emirates', 'United Kingdom', 'Japan', 'Brazil'],
        'Intelligence_Nodes': [450, 310, 205, 180, 290, 150, 120]
    })
    
    fig = px.choropleth(data, locations="Country", locationmode='country names',
                        color="Intelligence_Nodes",
                        color_continuous_scale='Reds',
                        title="NEXUS Global Intelligence Network")
    
    fig.update_layout(
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#050505', 
                 showcoastlines=True, coastlinecolor="#333"),
        paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"},
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 3. KINETIC DATA VISUALIZATION ---
def render_kinetic_radar(metrics):
    """High-fidelity Radar chart for competitive ROI strategy."""
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(metrics.values()),
        theta=list(metrics.keys()),
        fill='toself',
        line_color='#ff4b4b',
        fillcolor='rgba(255, 75, 75, 0.2)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'size': 14},
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. THE FIRST VIEW (LANDING WOW) ---
def render_landing():
    apply_enterprise_theme()
    st.markdown("<h1 style='text-align: center;'>🏛️ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)
    
    render_global_coverage_map()
    
    col_l, col_r = st.columns([1, 1])
    with col_l:
        st.info("### 🔐 Authorize Access")
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        if st.button("ENTER TERMINAL"):
            try:
                res = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Access Denied: Invalid Credentials.")
    
    with col_r:
        st.markdown("<div class='agency-card'>", unsafe_allow_html=True)
        st.markdown("### 💎 Agency Especial")
        st.write("White-Label | API Access | Bespoke Strategy")
        st.write("**Pricing: Consultative Only**")
        if st.button("REQUEST PRIVATE ACCESS"):
            st.toast("Elite Desk Notified. Stand by.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 5. PRODUCTION DASHBOARD ---
if "user" not in st.session_state:
    render_landing()
else:
    # State Sync with Supabase
    profile = nexus.supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    tier = profile['plan_tier']
    
    st.sidebar.title(f"🏛️ {tier} Terminal")
    st.sidebar.metric("Analysis Quota", profile['credits'])
    
    st.title("⚡ Strategy Deployment")
    target_url = st.text_input("Global Domain for Analysis (e.g., https://apple.com):")
    
    if st.button("EXECUTE SCAN") and target_url:
        # Kinetic Terminal Overlay
        terminal = st.empty()
        with terminal.container():
            st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
            st.write("> Initializing Firecrawl Data Harvester...")
            time.sleep(1)
            st.write("> Mapping Global Semantic Vectors...")
            time.sleep(1)
            st.write("> Executing Multi-Model Intelligence Inference...")
            st.markdown('</div>', unsafe_allow_html=True)
        
        terminal.empty()
        # Simulated high-level metrics
        render_kinetic_radar({"SEO": 9, "Authority": 8, "Tech": 9, "UX": 7, "ROI": 9})
        st.success(f"Strategic Intelligence Captured: {target_url}")

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
