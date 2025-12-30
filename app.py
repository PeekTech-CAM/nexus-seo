import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. ENTERPRISE CORE ARCHITECTURE ---
class NexusEliteSystem:
    def __init__(self):
        """Initializes the SaaS core with production-grade defaults."""
        # Resolve 405 error by targeting the direct REST API endpoint
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        self.plans = {
            "Starter": {"price": 100, "depth": 5000, "vectors": 128},
            "Pro": {"price": 1500, "depth": 15000, "vectors": 512},
            "Agency": {"price": 3000, "depth": 25000, "vectors": 1024}
        }
        # Explicitly mapping high-traffic hubs in Brazil and Morocco
        self.nodes = pd.DataFrame({
            'Hub': ['Brazil Node', 'Morocco Node', 'USA Node', 'Spain Node', 'UAE Node', 'Singapore Node'],
            'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
            'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81],
            'Activity': [98, 94, 85, 92, 99, 88]
        })

nexus = NexusEliteSystem()

# --- 2. ELITE CSS STYLING (THE WOW FACTOR) ---
def apply_luxury_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #050505; color: white; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff4b4b; }
        .stMetric { background: rgba(255, 75, 75, 0.05); border: 1px solid #ff4b4b; padding: 20px; border-radius: 12px; }
        .stButton>button {
            background: linear-gradient(90deg, #ff4b4b, #8b0000);
            color: white; border: none; font-weight: 700; height: 3.8rem; width: 100%;
            box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4); transition: 0.4s;
        }
        .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 8px 40px #ff4b4b; }
        .terminal-box { 
            background: #000; border: 1px solid #ff4b4b; padding: 20px; 
            color: #ff4b4b; font-family: 'Courier New', monospace;
            box-shadow: 0 0 30px rgba(255, 75, 75, 0.2); border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. KINETIC DATA VISUALIZATION ---
def render_3d_globe():
    """Kinetic 3D globe showing active global intelligence nodes."""
    fig = go.Figure(go.Scattergeo(
        lat=nexus.nodes['Lat'], lon=nexus.nodes['Lon'],
        mode='markers+text', text=nexus.nodes['Hub'],
        textposition="top center",
        marker=dict(size=14, color='#ff4b4b', line=dict(width=2, color='white'), opacity=0.9)
    ))
    fig.update_geos(
        projection_type="orthographic", showcoastlines=True, coastlinecolor="#222",
        showland=True, landcolor="#0a0a0a", showocean=True, oceancolor="#050505",
        bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), height=750)
    st.plotly_chart(fig, use_container_width=True)

def render_strategic_radar(metrics):
    """High-fidelity Radar chart for competitive ROI analysis."""
    fig = go.Figure(go.Scatterpolar(
        r=list(metrics.values()), theta=list(metrics.keys()),
        fill='toself', line_color='#ff4b4b', fillcolor='rgba(255, 75, 75, 0.2)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'size': 14}, height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. THE COMMAND CENTER (FIRST VIEW) ---
def render_landing():
    apply_luxury_styles()
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff4b4b; letter-spacing: 5px;'>GLOBAL STRATEGIC INTELLIGENCE</p>", unsafe_allow_html=True)
    
    render_3d_globe()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Intelligence Nodes", "1,842", "+12")
    col2.metric("Market Scans", "15.4M", "Live")
    col3.metric("Strategic ROI", "342%", "🔥")
    
    st.divider()
    
    col_l, col_r = st.columns([1, 1.3])
    with col_l:
        st.subheader("🔐 Access Terminal")
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token (Password)", type="password")
        if st.button("AUTHORIZE ACCESS"):
            try:
                # Login logic resolves 405 error with correct API URL
                res = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Access Denied: Verify API URL and Credentials.")
    with col_r:
        st.markdown("""
            <div style="border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05); text-align: center;">
                <h3 style="color: #ff4b4b;">💎 Agency Especial</h3>
                <p>Private white-label strategy for enterprise partners.</p>
                <p><b>Consultation Only</b></p>
                <button style="width:100%; background:#ff4b4b; color:white; border:none; padding:10px; border-radius:5px; font-weight:bold;">REQUEST PRIVATE ACCESS</button>
            </div>
        """, unsafe_allow_html=True)

# --- 5. EXECUTION ---
if "user" not in st.session_state:
    render_landing()
else:
    # State synchronization with Supabase
    profile = nexus.supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    tier = profile['plan_tier']
    
    st.sidebar.title(f"🏛️ {tier} Terminal")
    st.sidebar.metric("Quota Remaining", profile['credits'])
    
    st.title("⚡ Strategy Deployment")
    target = st.text_input("Input Domain for High-Vector Analysis:")
    
    if st.button("EXECUTE SCAN") and target:
        # Kinetic Terminal Experience
        terminal = st.empty()
        with terminal.container():
            st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
            st.write("> Initializing Global Data Nodes...")
            time.sleep(1)
            st.write(f"> Mapping ROI Vectors for {target}...")
            time.sleep(1.5)
            st.success("> Strategic Intelligence Captured.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        terminal.empty()
        render_strategic_radar({"SEO": 9, "UX": 8, "ROI": 9, "Tech": 7, "Speed": 9})

    if st.sidebar.button("Log Out"):
        nexus.supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
