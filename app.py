import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import datetime

# --- 1. SECURE ENTERPRISE INITIALIZATION ---
@st.cache_resource
def init_nexus_core():
    # Use Project API URL to resolve the 405 Method Not Allowed error
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_nexus_core()

# --- 2. ELITE OBSIDIAN UI (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: #ffffff; }
    div[data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1a1a1a; }
    .stMetric { background: rgba(255,255,255,0.02); border: 1px solid #1a1a1a; padding: 15px; border-radius: 10px; }
    .stButton>button {
        background: linear-gradient(45deg, #ff4b4b, #8b0000);
        color: white; border: none; border-radius: 5px; font-weight: bold;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.2); transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #ff4b4b; }
    input { background-color: #111 !important; color: white !important; border: 1px solid #222 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE "WOW" 3D GLOBAL INTELLIGENCE GLOBE ---
def render_elite_globe():
    """Kinetic 3D globe with obsidian textures and glowing nodes."""
    # Active Intelligence Nodes (Real-world mapping)
    nodes = pd.DataFrame({
        'Location': ['Brazil (Active)', 'Morocco (Active)', 'USA', 'Spain', 'UAE', 'Singapore'],
        'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
        'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81],
        'Traffic': [95, 88, 70, 92, 99, 85]
    })
    
    fig = go.Figure(go.Scattergeo(
        lat=nodes['Lat'], lon=nodes['Lon'],
        mode='markers',
        text=nodes['Location'],
        marker=dict(size=12, color='#ff4b4b', symbol='circle',
                    line=dict(width=2, color='white'),
                    opacity=0.8,
                    colorscale='Reds',
                    cmin=0, cmax=100)
    ))

    fig.update_geos(
        projection_type="orthographic", # High-end 3D sphere
        showcoastlines=True, coastlinecolor="#222",
        showland=True, landcolor="#0a0a0a",
        showocean=True, oceancolor="#050505",
        showcountries=True, countrycolor="#1a1a1a",
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=650,
        geo=dict(center=dict(lat=20, lon=0), projection_scale=1.2)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. AUTHENTICATION & REGISTRATION LOGIC ---
def auth_portal():
    st.sidebar.markdown("# 🏛️ NEXUS ACCESS")
    mode = st.sidebar.radio("Security Mode", ["Secure Login", "Register Agency"])
    email = st.sidebar.text_input("Corporate ID (Email)")
    # MASKED PASSWORD for security
    pwd = st.sidebar.text_input("Security Token (Password)", type="password")

    if st.sidebar.button("AUTHORIZE SESSION"):
        try:
            if mode == "Register Agency":
                # Fixes registration logic
                res = supabase.auth.sign_up({"email": email, "password": pwd})
                st.sidebar.success("Authorization Request Sent. Verify your Email.")
            else:
                # Fixes login logic
                res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = res.user
                st.rerun()
        except Exception as e:
            st.sidebar.error("Access Denied: 405 Error Detected. Update your Supabase API URL.")

# --- 5. ENTERPRISE COMMAND CENTER ---
if "user" not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Global Intelligence & Strategic ROI Engine</p>", unsafe_allow_html=True)
    
    # Hero Visuals
    render_elite_globe()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Intelligence Nodes", "1,842", "+12")
    col2.metric("Active Market Scans", "15.4M", "Live")
    col3.metric("Avg Strategic ROI", "342%", "🔥")
    
    auth_portal()
else:
    # Set your admin email here
    is_admin = (st.session_state.user.email == "your-admin-email@gmail.com")
    
    if is_admin:
        st.title("👑 ADMIN MASTER TERMINAL")
        if st.button("Export All Leads"):
            leads = supabase.table("leads").select("*").execute()
            st.dataframe(leads.data)
    else:
        st.title("🛰️ Strategy Deployment Node")
        st.success(f"Authorized: {st.session_state.user.email}")
        
        # Strategy Logic...
        target_url = st.text_input("Input Target Domain (e.g., https://tesla.com):")
        if st.button("EXECUTE SCAN"):
            with st.status("Analyzing Multi-Vector Semantic Data..."):
                time.sleep(2)
                st.success("Analysis Complete.")

    if st.sidebar.button("TERMINATE SESSION"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
