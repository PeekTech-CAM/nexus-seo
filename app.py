import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# --------------------
# SESSION INIT
# --------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# --------------------
# NEXUS ELITE ENGINE
# --------------------
class NexusEliteEngine:
    def __init__(self):
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )

nexus = NexusEliteEngine()

# --------------------
# AUTH GATE
# --------------------
def render_auth_gate():
    st.markdown("<h1 style='text-align:center;'>🏛️ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🔐 Access Terminal")
        mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
        email = st.text_input("Corporate ID (Email)")
        pwd = st.text_input("Security Token", type="password")
        
        if st.button("AUTHORIZE ACCESS"):
            try:
                if mode == "Register Organization":
                    # Sign up with redirect (replace YOUR_DOMAIN with your app URL)
                    nexus.supabase.auth.sign_up(
                        {
                            "email": email,
                            "password": pwd
                        },
                        redirect_to="https://YOUR_DOMAIN"  
                    )
                    st.success("✅ Registration Request Sent. Check your email for confirmation.")
                else:
                    res = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    if res.user:
                        # Upsert user profile
                        nexus.supabase.table("profiles").upsert({
                            "id": res.user.id,
                            "email": email,
                            "plan_tier": "Starter"
                        }).execute()
                        st.session_state.authenticated = True
                        st.session_state.user = res.user
                        st.experimental_rerun()
                    else:
                        st.error("⚠️ Login failed. Email might not be confirmed yet.")
            except Exception as e:
                st.error(f"Access Denied: {str(e)}")

    with col_r:
        st.markdown("""
            <div style='border: 2px solid #ff4b4b; padding: 25px; border-radius: 15px; background: rgba(255,75,75,0.05); text-align: center;'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence for global organizations.</p>
                <p><b>Pricing: Contact Sales for Consultation</b></p>
            </div>
        """, unsafe_allow_html=True)

# --------------------
# INTERNAL DASHBOARD
# --------------------
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

    # Plotly Globe
    fig = go.Figure(go.Scattergeo(
        lat=[-14.23, 31.79, 37.09], lon=[-51.92, -7.09, -95.71],
        mode='markers', marker=dict(size=12, color='#ff4b4b')
    ))
    fig.update_geos(projection_type="orthographic", showland=True, landcolor="#0a0a0a", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)

    if st.sidebar.button("TERMINATE SESSION"):
        nexus.supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.user = None
        st.experimental_rerun()

# --------------------
# ROUTER
# --------------------
if not st.session_state.authenticated:
    render_auth_gate()
else:
    render_internal_dashboard()
