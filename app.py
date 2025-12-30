import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. ENTERPRISE SYSTEM ARCHITECTURE ---
class NexusProductionEngine:
    """Class-based backend to manage complex SaaS state and DB handshakes."""
    def __init__(self):
        # Use the verified Project API URL from your secrets
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        self.nodes = self._load_global_nodes()

    def _load_global_nodes(self):
        """Strategic global node data for kinetic visualization."""
        return pd.DataFrame({
            'Hub': ['Brazil Hub', 'Morocco Hub', 'USA Node', 'Spain Node', 'UAE Node', 'Singapore Node'],
            'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
            'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81]
        })

    def sync_user_profile(self, user_id, email):
        """Atomic upsert to prevent 'duplicate key' errors."""
        try:
            return self.supabase.table("profiles").upsert({
                "id": user_id, 
                "email": email, 
                "plan_tier": "Starter", 
                "credits": 5
            }, on_conflict="id").execute()
        except Exception as e:
            st.error(f"Sync Error: {e}")
            return None

# Initialize the engine
nexus = NexusProductionEngine()

# --- 2. ELITE OBSIDIAN UI (CSS) ---
def apply_production_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background-color: #050505; color: white; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff4b4b; }
        .stMetric { background: rgba(255, 75, 75, 0.05); border: 1px solid #ff4b4b; padding: 25px; border-radius: 15px; }
        .stButton>button {
            background: linear-gradient(90deg, #ff4b4b, #8b0000);
            color: white; border: none; font-weight: 700; height: 4rem; width: 100%;
            border-radius: 12px; box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4); transition: 0.4s;
        }
        .stButton>button:hover { transform: translateY(-5px); box-shadow: 0 10px 50px #ff4b4b; }
        .agency-box { 
            border: 2px solid #ff4b4b; padding: 35px; border-radius: 15px; 
            background: rgba(255,75,75,0.05); text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. THE "WOW" KINETIC GLOBE ---
def render_3d_intelligence_globe():
    """High-fidelity orthographic globe for high-ticket clients."""
    fig = go.Figure(go.Scattergeo(
        lat=nexus.nodes['Lat'], lon=nexus.nodes['Lon'], mode='markers+text', text=nexus.nodes['Hub'],
        marker=dict(size=14, color='#ff4b4b', line=dict(width=2, color='white'), opacity=0.9)
    ))
    fig.update_geos(
        projection_type="orthographic", showcoastlines=True, coastlinecolor="#333",
        showland=True, landcolor="#0a0a0a", showocean=True, oceancolor="#050505", bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=700)
    st.plotly_chart(fig, use_container_width=True)

# --- 4. SECURE AUTHENTICATION FLOW ---
def auth_portal():
    apply_production_styles()
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>🏛️ NEXUS ELITE</h1>", unsafe_allow_html=True)
    render_3d_intelligence_globe()
    
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        with st.container(border=True):
            st.subheader("🔐 Access Terminal")
            mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
            email = st.text_input("Corporate ID (Email)")
            pwd = st.text_input("Security Token (Password)", type="password")
            
            if st.button("AUTHORIZE ACCESS"):
                try:
                    if mode == "Register Organization":
                        # Standard Registration
                        nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                        st.success("✅ Registration Request Sent. Verify your email to activate the profile.")
                    else:
                        # Login and Profile Sync
                        auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        st.session_state.user = auth.user
                        # Sync ensures no 'Key Error' when entering dashboard
                        nexus.sync_user_profile(auth.user.id, email)
                        st.rerun()
                except Exception as e:
                    # Clean error reporting to hide 'crazy' system logs from clients
                    st.error("Authentication Error: Verify your email confirmation or check credentials.")

    with col_r:
        st.markdown("""
            <div class='agency-box'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence and custom data depth for global organizations.</p>
                <p style='font-size: 1.5rem; font-weight: bold;'>Pricing: Contact Sales</p>
                <p>✅ 25k Node Analysis | ✅ API Export | ✅ Dedicated Support</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("REQUEST SALES CONSULTATION"):
            st.toast("Elite Desk Notified. Stand by.")

# --- 5. SYSTEM ROUTING ---
if "user" not in st.session_state:
    auth_portal()
else:
    apply_production_styles()
    # Fetch real-time state for the dashboard
    user_data = nexus.supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    
    st.sidebar.title(f"🛰️ {user_data['plan_tier']} Terminal")
    st.sidebar.metric("Audits Remaining", user_data['credits'])
    
    st.title("⚡ Strategy Deployment Node")
    # ... Dashboard content ...

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
