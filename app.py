import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# --- 1. ENTERPRISE CORE ---
class NexusEliteEngine:
    def __init__(self):
        # Using your verified API URL
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )

nexus = NexusEliteEngine()

# --- 2. ELITE OBSIDIAN STYLING ---
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
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
    st.markdown("<h1 style='text-align: center;'>🏛️ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)
    
    # High-impact Globe visualization
    fig = go.Figure(go.Scattergeo(
        lat=[-14.23, 31.79, 37.09], lon=[-51.92, -7.09, -95.71],
        mode='markers', marker=dict(size=12, color='#ff4b4b')
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
                        # Only sign up; don't touch profiles yet to avoid Foreign Key errors
                        nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                        st.success("✅ Registration Request Sent. Check email to activate.")
                    else:
                        res = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        # Handshake successful - create profile on first login
                        nexus.supabase.table("profiles").upsert({
                            "id": res.user.id, "email": email, "plan_tier": "Starter"
                        }).execute()
                        st.session_state.authenticated = True
                        st.session_state.user = res.user
                        st.rerun()
                except Exception as e:
                    st.error(f"Access Denied: Please confirm email first.")

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05); text-align: center;'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence for global organizations.</p>
                <p><b>Pricing: Contact Sales for Consultation</b></p>
                <button style='width: 100%; background:#ff4b4b; color:white; border:none; padding:10px; border-radius:5px;'>REQUEST PRIVATE ACCESS</button>
            </div>
        """, unsafe_allow_html=True)

# --- 4. INTERNAL VIEW: THE DASHBOARD ---
def render_internal_dashboard():
    st.sidebar.title("🏛️ Terminal Active")
    st.sidebar.write(f"Node: {st.session_state.user.email}")
    
    st.title("🛰️ Strategy Deployment Terminal")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Intelligence Nodes", "1,842", "+12")
    c2.metric("Market Scans", "15.4M", "Live")
    c3.metric("Strategic ROI", "342%", "🔥")

    st.subheader("📊 Semantic Vector Analysis")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['SEO', 'UX', 'ROI'])
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
