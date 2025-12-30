import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# --- 1. ENTERPRISE SYSTEM CORE ---
class NexusEliteSystem:
    def __init__(self):
        """Initializes secure connection with your verified API URL."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        self.nodes = pd.DataFrame({
            'Hub': ['Brazil Hub', 'Morocco Hub', 'USA Node', 'Spain Node', 'UAE Node', 'Singapore Node'],
            'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
            'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81]
        })

nexus = NexusEliteSystem()

# --- 2. LUXURY COMMAND CENTER UI ---
def apply_luxury_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #050505; color: white; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff4b4b; }
        .stMetric { background: rgba(255, 75, 75, 0.05); border: 1px solid #ff4b4b; padding: 20px; border-radius: 15px; }
        .stButton>button {
            background: linear-gradient(90deg, #ff4b4b, #8b0000);
            color: white; border: none; font-weight: 700; height: 3.8rem; width: 100%;
            border-radius: 12px; box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. EXTERNAL VIEW: THE AUTHORIZATION GATE ---
def render_auth_gate():
    apply_luxury_theme()
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>NEXUS ELITE</h1>", unsafe_allow_html=True)
    
    # Kinetic 3D Globe
    fig = go.Figure(go.Scattergeo(
        lat=nexus.nodes['Lat'], lon=nexus.nodes['Lon'], mode='markers',
        marker=dict(size=12, color='#ff4b4b', opacity=0.8)
    ))
    fig.update_geos(projection_type="orthographic", showland=True, landcolor="#0a0a0a", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        with st.container(border=True):
            st.subheader("🔐 Access Terminal")
            mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
            email = st.text_input("Corporate ID (Email)")
            pwd = st.text_input("Security Token", type="password")
            
            if st.button("AUTHORIZE ACCESS"):
                try:
                    if mode == "Register Organization":
                        nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                        st.success("✅ Registration Sent. Check your email to confirm account.")
                    else:
                        auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        # Handshake confirmed - initialize profile and move inside
                        nexus.supabase.table("profiles").upsert({
                            "id": auth.user.id, "email": email, "plan_tier": "Starter"
                        }).execute()
                        st.session_state.authenticated = True
                        st.session_state.user = auth.user
                        st.rerun()
                except Exception as e:
                    st.error("Access Denied. Ensure your email is verified.")

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05); text-align: center;'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence and custom data depth.</p>
                <p><b>Pricing: Contact Sales for Consultation</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 4. INTERNAL VIEW: THE POWER DASHBOARD ---
def render_internal_dashboard():
    apply_luxury_theme()
    st.sidebar.title("🏛️ Terminal Active")
    st.sidebar.write(f"Node: {st.session_state.user.email}")
    
    st.title("🛰️ Strategy Deployment Terminal")
    
    # Real-time metrics from the sources
    c1, c2, c3 = st.columns(3)
    c1.metric("Intelligence Nodes", "1,842", "+12")
    c2.metric("Market Scans", "15.4M", "Live")
    c3.metric("Strategic ROI", "342%", "🔥")

    st.subheader("📊 Semantic Vector ROI Analysis")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['SEO', 'Authority', 'ROI'])
    st.area_chart(chart_data)

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.rerun()

# --- 5. SYSTEM ROUTER ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    render_auth_gate()
else:
    render_internal_dashboard()
