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
        # Uses your verified Project API URL
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        # Strategic Nodes for visual authority
        self.nodes = pd.DataFrame({
            'Hub': ['Brazil Hub', 'Morocco Hub', 'USA Node', 'Spain Node'],
            'Lat': [-14.23, 31.79, 37.09, 40.46],
            'Lon': [-51.92, -7.09, -95.71, -3.74]
        })

nexus = NexusEliteEngine()

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

# --- 3. THE AUTHORIZATION GATE (EXTERNAL) ---
def render_auth_gate():
    apply_luxury_theme()
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem;'>🏛️ NEXUS ELITE</h1>", unsafe_allow_html=True)
    
    # 3D Kinetic Globe visualization
    fig = go.Figure(go.Scattergeo(lat=nexus.nodes['Lat'], lon=nexus.nodes['Lon'], mode='markers'))
    fig.update_geos(projection_type="orthographic", showland=True, landcolor="#0a0a0a", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=550)
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
                        st.success("✅ Profile Initialized. If 'Confirm Email' is OFF, switch to Login.")
                    else:
                        auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        # Sync profile AFTER login to fix foreign key error
                        nexus.supabase.table("profiles").upsert({
                            "id": auth.user.id, "email": email, "plan_tier": "Starter"
                        }).execute()
                        st.session_state.authenticated = True
                        st.session_state.user = auth.user
                        st.rerun()
                except Exception as e:
                    st.error("Access Denied: Check credentials or verify 'Confirm Email' is OFF.")

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05); text-align: center;'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence and custom data depth for global organizations.</p>
                <p><b>Pricing: Contact Sales for Consultation</b></p>
            </div>
        """, unsafe_allow_html=True)

# --- 4. THE COMMAND CENTER (INTERNAL) ---
def render_internal_dashboard():
    apply_luxury_theme()
    st.sidebar.title("🏛️ Terminal Active")
    st.sidebar.write(f"Authorized: {st.session_state.user.email}")
    
    st.title("🛰️ Strategy Deployment Terminal")
    
    # Intelligence KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intelligence Nodes", "1,842", "+12")
    c2.metric("Market Scans", "15.4M", "Live")
    c3.metric("Strategic ROI", "342%", "🔥")
    c4.metric("Networks", "94", "+5")
    
    st.subheader("📊 Semantic Vector ROI Analysis")
    st.area_chart(pd.DataFrame(np.random.randn(20, 3)))

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.rerun()

# --- 5. SYSTEM ROUTER ---
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    render_auth_gate()
else:
    render_internal_dashboard()
