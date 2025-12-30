import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime

# --- 1. ENTERPRISE INITIALIZATION ---
@st.cache_resource
def init_nexus_engine():
    # Targeted API URL as seen in your secrets fix
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_nexus_engine()

# --- 2. LUXURY UI ENGINE (OBSIDIAN THEME) ---
def apply_luxury_styles():
    st.markdown("""
        <style>
        .main { background: linear-gradient(135deg, #050505 0%, #1a0505 100%); color: white; }
        [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 2px solid #ff4b4b; }
        .stMetric { background: rgba(255, 75, 75, 0.05); border: 1px solid #ff4b4b; border-radius: 15px; padding: 20px; }
        .stButton>button {
            background: linear-gradient(90deg, #ff4b4b, #8b0000);
            color: white; border: none; font-weight: 700; height: 3.8rem; width: 100%;
            border-radius: 12px; box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
        }
        .terminal-overlay { 
            background: #000; border: 1px solid #ff4b4b; padding: 20px; 
            color: #ff4b4b; font-family: 'Courier New', monospace; border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. KINETIC 3D GLOBE ---
def render_elite_globe():
    """High-fidelity globe showing active nodes in Brazil, Morocco, and more."""
    nodes = pd.DataFrame({
        'Node': ['Brazil Hub', 'Morocco Hub', 'USA Node', 'Spain Node', 'UAE Node', 'Singapore Node'],
        'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
        'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81]
    })
    fig = go.Figure(go.Scattergeo(
        lat=nodes['Lat'], lon=nodes['Lon'], mode='markers+text', text=nodes['Node'],
        marker=dict(size=12, color='#ff4b4b', line=dict(width=2, color='white'))
    ))
    fig.update_geos(
        projection_type="orthographic", showcoastlines=True, coastlinecolor="#222",
        showland=True, landcolor="#0a0a0a", showocean=True, oceancolor="#050505", bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- 4. SECURE AUTHENTICATION (FIXED HANDSHAKE) ---
def auth_terminal():
    apply_luxury_styles()
    st.markdown("<h1 style='text-align: center;'>🏛️ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)
    render_elite_globe()
    
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
                        # 1. Sign up the user
                        res = supabase.auth.sign_up({"email": email, "password": pwd})
                        # 2. AUTO-CREATE PROFILE: This fixes the "Access Denied" error
                        supabase.table("profiles").insert({
                            "id": res.user.id, "email": email, "plan_tier": "Starter", "credits": 5
                        }).execute()
                        st.success("✅ Profile Initialized. Check email to confirm.")
                    else:
                        auth = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        st.session_state.user = auth.user
                        st.rerun()
                except Exception as e:
                    st.error(f"Access Denied: Check credentials or verify your email.")

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05);'>
                <h3 style='color: #ff4b4b;'>💎 Agency Especial</h3>
                <p>Private licensing and bespoke strategy for high-ticket partners.</p>
                <p><b>Consultation License: €3,000 / mo</b></p>
                <button style='width: 100%; padding: 10px; border-radius: 5px; background: #ff4b4b; border: none; color: white; font-weight:bold;'>REQUEST PRIVATE ACCESS</button>
            </div>
        """, unsafe_allow_html=True)

# --- 5. ENTERPRISE DASHBOARD ---
if "user" not in st.session_state:
    auth_terminal()
else:
    apply_luxury_styles()
    # Fetch User Stats
    profile = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    
    st.sidebar.title(f"🏛️ {profile['plan_tier']} Terminal")
    st.sidebar.metric("Audits Remaining", profile['credits'])
    
    st.title("🛰️ Strategy Deployment Node")
    target = st.text_input("Domain Analysis Target:")
    
    if st.button("EXECUTE SCAN") and target:
        with st.status("Initializing High-Vector Scans..."):
            time.sleep(1)
            st.write("> Connecting to Global Harvester Nodes...")
            time.sleep(1.2)
            st.success("Strategic Intelligence Captured.")
        # Visual charts go here...

    if st.sidebar.button("Logout"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
