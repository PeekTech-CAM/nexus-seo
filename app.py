import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import time

# --- 1. CORE SYSTEM INITIALIZATION ---
class NexusSaaSCommand:
    def __init__(self):
        # Database connection verified from your SQL Editor
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            self.ai = genai.GenerativeModel("gemini-1.5-pro")

    def get_user_profile(self, user_id):
        """Fetches live tier and credit status from 'profiles' table."""
        res = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data

nexus = NexusSaaSCommand()

# --- 2. ELITE COMMAND UI ---
def apply_elite_styling():
    """Applies the obsidian-crimson theme from your live terminal."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=swap');
        .main { background: radial-gradient(circle at top, #1a0505 0%, #050505 100%); color: white; }
        div[data-testid="stMetric"] { 
            background: rgba(255, 75, 75, 0.05); 
            border: 1px solid rgba(255, 75, 75, 0.2); 
            border-radius: 15px; padding: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. THE STRATEGY DEPLOYMENT TERMINAL ---
def render_terminal():
    apply_elite_styling()
    
    # Sync with live database record
    profile = nexus.get_user_profile(st.session_state.user.id)
    
    st.title("🛰️ Strategy Deployment Terminal")
    st.sidebar.markdown(f"### Node: {profile['email']}")
    st.sidebar.info(f"Tier: {profile['plan_tier']} | Credits: {profile['credits']}")
    
    # KPIs from your active terminal
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nodes", "2,148", "+24")
    c2.metric("Scans", "18.2M", "Live")
    c3.metric("ROI", "342%", "🔥")
    c4.metric("Networks", "94", "+5")

    st.divider()

    # GPT-SEO Intelligence Node
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🤖 AI Semantic Audit")
        target = st.text_input("Target Domain")
        if st.button("EXECUTE SCAN"):
            if profile['credits'] > 0:
                with st.status("Analyzing Vectors..."):
                    prompt = f"Perform an advanced SEO audit for {target}."
                    intel = nexus.ai.generate_content(prompt).text
                    st.session_state.audit_result = intel
                st.rerun()
            else:
                st.error("Upgrade required. Current tier: " + profile['plan_tier'])
        
        # Fixing the Stripe link
        st.link_button("🚀 Upgrade to Pro Tier", "https://buy.stripe.com/test_pro_tier")

    with col_r:
        if "audit_result" in st.session_state:
            st.info(st.session_state.audit_result)
            st.download_button("📥 DOWNLOAD PDF REPORT", data=st.session_state.audit_result, file_name="audit.txt")

# --- 4. ROUTER ---
if "user" not in st.session_state:
    st.warning("Authorize via Access Terminal.")
else:
    render_terminal()
