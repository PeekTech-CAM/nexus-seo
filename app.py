import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import pandas as pd
import time

# --- 1. ENTERPRISE SYSTEM CORE ---
class NexusEliteSystem:
    def __init__(self):
        """Initializes secure connection using your verified API URL."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        # Strategic Nodes for visual authority
        self.nodes = pd.DataFrame({
            'Hub': ['Brazil Hub', 'Morocco Hub', 'USA Node', 'Spain Node', 'UAE Node', 'Singapore Node'],
            'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35],
            'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81]
        })

nexus = NexusEliteSystem()

# --- 2. ELITE STYLING (OBSIDIAN & CRIMSON) ---
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
        .agency-box { 
            border: 2px solid #ff4b4b; padding: 30px; border-radius: 15px; 
            background: rgba(255,75,75,0.05); text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. KINETIC 3D GLOBE ---
def render_elite_globe():
    """Kinetic 3D globe visualization to justify premium pricing."""
    fig = go.Figure(go.Scattergeo(
        lat=nexus.nodes['Lat'], lon=nexus.nodes['Lon'], mode='markers+text', text=nexus.nodes['Hub'],
        marker=dict(size=14, color='#ff4b4b', line=dict(width=2, color='white'), opacity=0.9)
    ))
    fig.update_geos(
        projection_type="orthographic", showcoastlines=True, coastlinecolor="#222",
        showland=True, landcolor="#0a0a0a", showocean=True, oceancolor="#050505", bgcolor="rgba(0,0,0,0)"
    )
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=650)
    st.plotly_chart(fig, use_container_width=True)

# --- 4. SECURE AUTHENTICATION & LEAD CAPTURE ---
def auth_terminal():
    apply_luxury_theme()
    st.markdown("<h1 style='text-align: center; font-size: 4rem; margin-bottom: 0;'>NEXUS ELITE</h1>", unsafe_allow_html=True)
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
                        res = nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                        nexus.supabase.table("profiles").upsert({
                            "id": res.user.id, "email": email, "plan_tier": "Starter", "credits": 5
                        }, on_conflict="email").execute()
                        st.success("✅ Profile Initialized. Check email to confirm.")
                    else:
                        auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                        st.session_state.user = auth.user
                        st.rerun()
                except Exception as e:
                    st.error(f"Authentication Error: {e}")

    with col_r:
        st.markdown("""
            <div class='agency-box'>
                <h3 style='color: #ff4b4b;'>💎 Agency Elite</h3>
                <p>Strategic white-label intelligence and custom data depth for global organizations.</p>
                <p style='font-size: 1.2rem; font-weight: bold;'>Pricing: Contact Sales for Consultation</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("REQUEST PRIVATE SALES CONSULTATION"):
            st.session_state.show_sales_form = True

    if st.session_state.get("show_sales_form"):
        st.divider()
        with st.form("Sales Request"):
            st.subheader("Book Your Strategic Review")
            s_name = st.text_input("Full Name")
            s_org = st.text_input("Organization / Agency Name")
            s_email = st.text_input("Corporate Email")
            s_msg = st.text_area("Provide a brief overview of your domain management volume")
            if st.form_submit_button("SUBMIT TO SALES"):
                # Captures the high-ticket lead into a 'leads' table
                nexus.supabase.table("leads").insert({
                    "name": s_name, "organization": s_org, "email": s_email, "message": s_msg
                }).execute()
                st.success("Your request has been routed to the Elite Desk. We will contact you within 24 hours.")

# --- 5. EXECUTION ---
if "user" not in st.session_state:
    auth_terminal()
else:
    # Authenticated dashboard...
    st.sidebar.title("🏛️ Command Terminal")
    if st.sidebar.button("Logout"):
        nexus.supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
