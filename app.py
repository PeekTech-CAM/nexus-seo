import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time

# --- 1. ENTERPRISE INITIALIZATION ---
@st.cache_resource
def init_nexus_engine():
    # Targeted API URL to resolve the 405 error
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_nexus_engine()

# --- 2. THE "WOW" GLOBAL INTELLIGENCE MAP ---
def render_elite_globe():
    """High-fidelity globe showing global node density."""
    # Real-world coordinate mapping for 'Elite' nodes
    data = pd.DataFrame({
        'City': ['New York', 'Madrid', 'Dubai', 'London', 'Singapore', 'Tokyo'],
        'Lat': [40.71, 40.41, 25.20, 51.50, 1.35, 35.67],
        'Lon': [-74.00, -3.70, 55.27, -0.12, 103.81, 139.65],
        'Status': ['Online', 'Online', 'Active', 'Active', 'Online', 'Online']
    })
    
    fig = px.scatter_geo(data, lat='Lat', lon='Lon', hover_name='City',
                         color_discrete_sequence=['#ff4b4b'],
                         projection="orthographic") # Makes it a 3D Globe
    
    fig.update_geos(
        showcoastlines=True, coastlinecolor="#333",
        showland=True, landcolor="#050505",
        showocean=True, oceancolor="#000",
        showcountries=True, countrycolor="#1a1a1a"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"},
        margin=dict(l=0, r=0, t=0, b=0), height=500
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 3. DUAL-PORTAL AUTHENTICATION ---
def auth_terminal():
    st.sidebar.markdown("# 🏛️ NEXUS ACCESS")
    action = st.sidebar.selectbox("Access Mode", ["Secure Login", "Register Agency"])
    email = st.sidebar.text_input("Corporate ID")
    pwd = st.sidebar.text_input("Security Token", type="password")

    if st.sidebar.button("AUTHORIZE"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = res.user
            st.rerun()
        except: st.sidebar.error("Access Denied.")

# --- 4. THE COMMAND CENTER ---
if "user" not in st.session_state:
    st.title("🏛️ NEXUS ELITE COMMAND")
    render_elite_globe()
    auth_terminal()
else:
    # --- ADMIN VS CUSTOMER LOGIC ---
    # Change 'your-email@gmail.com' to your actual email
    is_admin = (st.session_state.user.email == "your-email@gmail.com")
    
    if is_admin:
        st.title("👑 Admin Intelligence Terminal")
        st.write("System status: All nodes operational.")
        # Admin can see all leads
        if st.button("View Global Leads"):
            leads = supabase.table("leads").select("*").execute()
            st.table(leads.data)
    else:
        st.title("⚡ Strategy Deployment Terminal")
        # Standard customer view...
        st.write(f"Welcome back, {st.session_state.user.email}")

    if st.sidebar.button("TERMINATE SESSION"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
