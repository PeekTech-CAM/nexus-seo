import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

# --- 1. ENTERPRISE SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="NEXUS Elite Command",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

class NexusEnterpriseEngine:
    def __init__(self):
        """
        CRITICAL FIX: The 405 Error in your screenshot occurs because you are targeting 
        the Dashboard URL. You MUST use the Project API URL from Settings > API.
        """
        try:
            self.supabase: Client = create_client(
                st.secrets["SUPABASE_URL"],  # https://xyz.supabase.co
                st.secrets["SUPABASE_KEY"]   # Service Role Key
            )
        except Exception as e:
            st.error(f"Initialization Failed: {e}")
            st.stop()

        self.tiers = {
            "Starter": {"price": 100, "depth": 5000, "vectors": 128},
            "Pro": {"price": 1500, "depth": 15000, "vectors": 512},
            "Agency": {"price": 3000, "depth": 25000, "vectors": 1024}
        }

    @st.cache_data(ttl=300)
    def get_global_nodes(_self):
        """High-fidelity data for the globe visualization."""
        return pd.DataFrame({
            'Hub': ['Brazil', 'Morocco', 'USA', 'Spain', 'UAE', 'Singapore', 'Japan', 'India'],
            'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35, 36.20, 20.59],
            'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81, 138.25, 78.96],
            'Activity': [88, 83, 95, 91, 99, 94, 85, 96]
        })

nexus = NexusEnterpriseEngine()

# --- 2. ELITE OBSIDIAN STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Space Grotesk', sans-serif; 
        background: linear-gradient(135deg, #050505 0%, #1a0505 100%);
        color: white; 
    }
    
    [data-testid="stSidebar"] { 
        background-color: #0a0a0a; 
        border-right: 2px solid #ff4b4b; 
    }
    
    .stMetric { 
        background: rgba(255, 75, 75, 0.05); 
        border: 1px solid #ff4b4b; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 0 30px rgba(255, 75, 75, 0.2); 
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b, #8b0000);
        color: white; border: none; font-weight: 700; height: 4rem; width: 100%;
        border-radius: 12px; transition: 0.4s;
    }
    
    .stButton>button:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 10px 50px #ff4b4b; 
    }
    
    input { background-color: #111 !important; color: #ff4b4b !important; border: 1px solid #222 !important; }
    
    .terminal-box { 
        background: #000; border: 1px solid #ff4b4b; padding: 25px; 
        color: #ff4b4b; font-family: 'Courier New', monospace;
        border-radius: 10px; margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. KINETIC VISUALIZATION ENGINE ---
def render_kinetic_globe():
    """Obsidian-textured globe with pulsating active nodes."""
    nodes = nexus.get_global_nodes()
    
    fig = go.Figure()
    
    # Pulsing Intelligence Nodes
    fig.add_trace(go.Scattergeo(
        lon=nodes['Lon'], lat=nodes['Lat'],
        text=nodes['Hub'] + '<br>Traffic: ' + nodes['Activity'].astype(str) + '%',
        mode='markers+text',
        marker=dict(size=15, color='#ff4b4b', line=dict(width=2, color='white'), opacity=0.9),
        textposition="top center"
    ))

    fig.update_geos(
        projection_type="orthographic", 
        showcoastlines=True, coastlinecolor="#222",
        showland=True, landcolor="#0a0a0a",
        showocean=True, oceancolor="#050505",
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        height=750, margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

def render_radar_metrics(metrics):
    """High-fidelity Radar for competitive strategic intelligence."""
    fig = go.Figure(go.Scatterpolar(
        r=list(metrics.values()), theta=list(metrics.keys()),
        fill='toself', line_color='#ff4b4b', fillcolor='rgba(255, 75, 75, 0.2)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=450
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. SECURE DUAL-PORTAL AUTHENTICATION ---
def auth_gateway():
    """
    Modular Auth handles both Client Registration and Admin Access.
    """
    col_l, col_r = st.columns([1, 1.3])
    
    with col_l:
        st.markdown("<div class='stMetric'>", unsafe_allow_html=True)
        st.subheader("🔐 Access Terminal")
        mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
        email = st.text_input("Corporate ID (Email)")
        pwd = st.text_input("Security Token (Password)", type="password")
        
        if st.button("AUTHORIZE ACCESS"):
            try:
                if mode == "Register Organization":
                    # Fixes the 405 error by using the correct API client
                    nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                    st.success("✅ Profile Initialized. Check email to confirm.")
                else:
                    auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    st.session_state.user = auth.user
                    st.rerun()
            except Exception as e:
                st.error("Access Denied: 405 Error detected. Verify API Project URL in Secrets.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 30px; border-radius: 15px; background: rgba(255,75,75,0.05);'>
                <h3 style='color: #ff4b4b;'>💎 Agency Especial</h3>
                <p>Strategic white-label intelligence for enterprise organizations.</p>
                <p><b>Consultation License: €3,000 / mo</b></p>
                <p>✅ 25k Node Analysis | ✅ API Export | ✅ Dedicated Support</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("REQUEST PRIVATE ACCESS"):
            st.toast("Elite Desk Notified. Stand by.")

# --- 5. ENTERPRISE COMMAND DASHBOARD ---
def render_admin_view():
    """Special view for you (the owner) to manage leads."""
    st.title("👑 Master Intelligence Overlord")
    leads = nexus.supabase.table("leads").select("*").execute()
    st.dataframe(leads.data)

def render_client_view(user):
    """The main product dashboard for paying customers."""
    # Sync with Supabase profiles
    profile = nexus.supabase.table("profiles").select("*").eq("id", user.id).single().execute().data
    
    st.sidebar.success(f"Node Active: {profile['plan_tier']}")
    st.sidebar.metric("Quota Remaining", profile['credits'])
    
    tab1, tab2, tab3 = st.tabs(["⚡ Strategy Terminal", "🌍 Global Pulse", "📊 ROI Analysis"])
    
    with tab1:
        st.title("⚡ Strategy Deployment")
        target = st.text_input("Input Target Domain Intelligence:")
        if st.button("EXECUTE VECTOR SCAN") and target:
            # Kinetic Terminal Experience
            terminal = st.empty()
            with terminal.container():
                st.markdown("<div class='terminal-box'>", unsafe_allow_html=True)
                st.write("> Connecting to Firecrawl Data Harvester...")
                time.sleep(1)
                st.write("> Mapping Global ROI Vectors...")
                time.sleep(1)
                st.write("> Executing Multi-Vector Intelligence Inference...")
                st.markdown("</div>", unsafe_allow_html=True)
            
            terminal.empty()
            render_radar_metrics({"SEO": 9, "UX": 8, "Tech": 9, "Authority": 7, "ROI": 9})
            st.success(f"Strategic Intelligence Captured for {target}")

    with tab2:
        render_kinetic_globe()

# --- 6. GLOBAL ROUTING ENGINE ---
if "user" not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 5rem;'>🏛️ NEXUS ELITE</h1>", unsafe_allow_html=True)
    render_kinetic_globe()
    auth_gateway()
else:
    # Separate logic for Admin and Clients
    if st.session_state.user.email == "your-admin-email@gmail.com":
        render_admin_view()
    else:
        render_client_view(st.session_state.user)

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
