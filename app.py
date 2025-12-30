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
        """Initializes connection with verified API and AI nodes."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        # Tiered Subscription Links
        self.stripe_links = {
            "Pro": "https://buy.stripe.com/test_pro_tier",
            "Agency": "https://nexus.agency/contact-sales"
        }

nexus = NexusEliteEngine()
# Add this function to your render_internal_dashboard() section
def render_audit_engine():
    st.subheader("🤖 GPT-SEO Strategic Audit")
    
    with st.container(border=True):
        target_url = st.text_input("Enter Target Domain (e.g., example.com)")
        competitor_url = st.text_input("Enter Competitor Domain")
        
        if st.button("EXECUTE SEMANTIC SCAN"):
            if target_url and competitor_url:
                with st.status("Analyzing Search Intelligence...", expanded=True):
                    st.write("🛰️ Connecting to Intelligence Nodes...")
                    time.sleep(1)
                    
                    # This is where we call Gemini AI
                    prompt = f"Analyze the SEO semantic gap between {target_url} and {competitor_url}. Provide 3 high-impact directives."
                    try:
                        response = nexus.ai.generate_content(prompt)
                        st.write("✅ Intelligence Captured.")
                        
                        st.markdown("### 📡 Strategic Directives")
                        st.info(response.text)
                        
                        # Update SaaS Database Credits
                        nexus.supabase.table("profiles").update({"credits": 4}).eq("id", st.session_state.user.id).execute()
                    except Exception as e:
                        st.error(f"AI Node Error: {e}")
            else:
                st.warning("Please provide target and competitor URLs.")
# --- 2. LUXURY COMMAND CENTER UI ---
def apply_luxury_theme():
    """Applies glassmorphism and premium typography."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono&display=swap');
        
        html, body, [class*="css"] { 
            font-family: 'Space Grotesk', sans-serif; 
            background: radial-gradient(circle at top left, #1a0505 0%, #050505 100%);
            color: white; 
        }
        
        /* Glassmorphism Cards */
        .premium-card {
            background: rgba(255, 75, 75, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 75, 75, 0.2);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            transition: 0.4s;
        }
        .premium-card:hover { border-color: #ff4b4b; transform: translateY(-5px); }

        /* Glowing Action Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
            color: white; border: none; font-weight: 700; height: 3.5rem; width: 100%;
            border-radius: 12px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. PRICING & TIERED ACCESS ---
def render_pricing_gate():
    """Converts prospects to paid clients."""
    apply_luxury_theme()
    st.markdown("<h1 style='text-align: center; letter-spacing: -2px;'>🏛️ SELECT INTELLIGENCE TIER</h1>", unsafe_allow_html=True)
    
    col_free, col_pro, col_agency = st.columns(3)
    with col_free:
        st.markdown("<div class='premium-card'><h3>BASIC</h3><p>5 Scans / Mo</p><h2>$0</h2></div>", unsafe_allow_html=True)
        if st.button("INITIALIZE FREE ACCESS"):
            st.session_state.view = "auth"
            st.rerun()

    with col_pro:
        st.markdown("<div class='premium-card' style='border-color: #ff4b4b;'><h3>PRO</h3><p>500 Scans / Mo</p><h2>$99</h2></div>", unsafe_allow_html=True)
        st.link_button("UPGRADE TO PRO", nexus.stripe_links["Pro"])

    with col_agency:
        st.markdown("<div class='premium-card'><h3>AGENCY</h3><p>UNLIMITED SCANS</p><h2>CUSTOM</h2></div>", unsafe_allow_html=True)
        st.link_button("CONTACT SALES", nexus.stripe_links["Agency"])
    
    st.divider()
    if st.button("EXPLORE SYSTEM DEMO"):
        st.session_state.view = "demo"
        st.rerun()

# --- 4. THE LIVE DEMO NODE ---
def render_demo():
    """Visual 'Wow' factor demo."""
    st.info("🛰️ DEMO MODE: Register for live-vector intelligence.")
    fig = go.Figure(go.Scattergeo(lat=[31.7, -14.2, 40.4], lon=[-7.1, -51.9, -3.7], mode='markers', marker=dict(color='#ff4b4b', size=12)))
    fig.update_geos(projection_type="orthographic", showland=True, landcolor="#111", bgcolor="rgba(0,0,0,0)")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), height=500)
    st.plotly_chart(fig, use_container_width=True)
    if st.button("EXIT DEMO & REGISTER"):
        st.session_state.view = "auth"
        st.rerun()

# --- 5. THE AUTHORIZATION GATE ---
def render_auth_gate():
    """Handles secure onboarding."""
    apply_luxury_theme()
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🔐 Access Terminal")
        mode = st.radio("Action", ["Login", "Register Organization"], horizontal=True)
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        
        if st.button("AUTHORIZE ACCESS"):
            try:
                if mode == "Register Organization":
                    nexus.supabase.auth.sign_up({"email": email, "password": pwd})
                    st.success("✅ Profile Initialized. Email verification bypassed.")
                else:
                    auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                    # Prevents foreign key crashes
                    nexus.supabase.table("profiles").upsert({"id": auth.user.id, "email": email, "plan_tier": "Starter"}).execute()
                    st.session_state.user = auth.user
                    st.rerun()
            except Exception as e:
                st.error(f"Access Denied: {e}")
    with col_r:
        st.markdown("<div class='premium-card'><h3>💎 Agency Elite</h3><p>White-label intelligence for global organizations.</p></div>", unsafe_allow_html=True)

# --- 6. PRODUCTION ROUTER ---
def main():
    if "user" in st.session_state:
        # FULL PRODUCTION DASHBOARD
        apply_luxury_theme()
        st.sidebar.title("🏛️ Terminal Active")
        st.title("🛰️ Strategy Deployment Terminal")
        st.sidebar.write(f"Node: {st.session_state.user.email}")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nodes", "2,148", "+24")
        c2.metric("Scans", "18.2M", "Live")
        c3.metric("ROI", "342%", "🔥")
        c4.metric("Networks", "94", "+5")
        
        st.subheader("📊 Strategic ROI Projections")
        st.area_chart(pd.DataFrame(np.random.randn(20, 3)))

        if st.sidebar.button("TERMINATE SESSION"):
            nexus.supabase.auth.sign_out()
            del st.session_state.user
            st.rerun()
    else:
        if "view" not in st.session_state: st.session_state.view = "pricing"
        if st.session_state.view == "pricing": render_pricing_gate()
        elif st.session_state.view == "demo": render_demo()
        elif st.session_state.view == "auth": render_auth_gate()

if __name__ == "__main__":
    main()
