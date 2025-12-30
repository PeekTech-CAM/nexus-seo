import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import numpy as np
import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# --- 1. GA4 INJECTION ENGINE ---
def inject_ga():
    """Injects GA4 tracking code into the app's sandboxed iframe."""
    # Replace G-XXXXXXXXXX with your actual Measurement ID from Google Analytics
    GA_ID = st.secrets.get("GA_MEASUREMENT_ID", "G-XXXXXXXXXX")
    
    ga_js = f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{GA_ID}');
        </script>
    """
    # height=0 keeps the component invisible to the user
    components.html(ga_js, height=0)

# --- 2. THE TERMINAL WITH OBSERVABILITY ---
def main():
    inject_ga() # Initialize tracking on every page load
    
    if "user" not in st.session_state:
        # (Standard Auth Logic remains here)
        pass
    else:
        # (Standard Dashboard Logic remains here)
        pass
# --- 1. CORE ENTERPRISE ENGINE ---
class NexusEliteEngine:
    def __init__(self):
        """Initializes secure database and AI neural nodes."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            # Switching to 'flash' resolves the google.api_core.exceptions.NotFound error
            try:
                self.ai = genai.GenerativeModel('gemini-1.5-flash')
            except Exception:
                self.ai = None

    def safe_audit(self, prompt):
        """Fail-safe generation to prevent terminal crashes."""
        if not self.ai:
            return "AI Node Offline. Check API Key permissions."
        try:
            response = self.ai.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Intelligence Stream Error: {str(e)}"

    def sync_user(self, user_id):
        """Fetches live profile data from Supabase."""
        res = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data

nexus = NexusEliteEngine()

# --- 2. LUXURY COMMAND UI ---
def apply_elite_ui():
    """Renders the high-authority obsidian-crimson design."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=JetBrains+Mono&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background: #050505; color: white; }
        .main { background: radial-gradient(circle at top, #1a0505 0%, #050505 100%); }
        div[data-testid="stMetric"] { 
            background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.2); 
            padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); 
        }
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
            color: white !important; font-weight: 700 !important; border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC TERMINAL ---
def render_terminal():
    apply_elite_ui()
    profile = nexus.sync_user(st.session_state.user.id)
    
    # Live KPI Board
    st.markdown("## 🛰️ Strategy Deployment Terminal")
    st.sidebar.markdown(f"**Node:** {profile.get('email', 'Unknown')}")
    st.sidebar.markdown(f"**Tier:** {profile.get('plan_tier', 'Starter')}")
    st.sidebar.markdown(f"**Credits:** {profile.get('credits', 0)}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intel Nodes", "2,148", "+24")
    c2.metric("Market Scans", "18.2M", "Live")
    c3.metric("Semantic ROI", "342%", "🔥")
    c4.metric("Networks", "94", "+5")

    st.divider()

    # GPT-SEO Engine
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🤖 AI Semantic Audit")
        target = st.text_input("Target Domain")
        comp = st.text_input("Top Competitor")
        
        if st.button("EXECUTE SCAN"):
            if profile.get('credits', 0) > 0:
                with st.status("Analyzing Vectors..."):
                    prompt = f"Perform an elite SEO audit for {target} vs {comp}."
                    intel = nexus.safe_audit(prompt)
                    # Log Audit & Decrement Credit
                    nexus.supabase.table("audit_history").insert({"user_id": st.session_state.user.id, "target": target, "intelligence": intel}).execute()
                    nexus.supabase.table("profiles").update({"credits": profile['credits']-1}).eq("id", st.session_state.user.id).execute()
                    st.session_state.last_audit = intel
                st.rerun()
            else:
                st.error("Insufficient Credits. Purchase 1,000 CHF Tier.")

    with col_r:
        if "last_audit" in st.session_state:
            st.info(st.session_state.last_audit)
            st.download_button("📥 DOWNLOAD PDF", data=st.session_state.last_audit, file_name="Nexus_Audit.txt")

# --- 4. BULLETPROOF ADMIN ---
def render_admin():
    st.title("⚖️ Admin Overlord Terminal")
    try:
        response = nexus.supabase.table("profiles").select("*").execute()
        users = response.data
        if users:
            df = pd.DataFrame(users)
            # Dynamic check to prevent KeyError
            cols = ['email', 'plan_tier', 'credits', 'created_at']
            valid = [c for c in cols if c in df.columns]
            st.dataframe(df[valid], use_container_width=True)
    except Exception as e:
        st.error(f"Admin Error: {e}")

# --- 5. SYSTEM ROUTER ---
def main():
    if "user" not in st.session_state:
        apply_elite_ui()
        st.title("🏛️ NEXUS ELITE ACCESS")
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        if st.button("AUTHORIZE"):
            auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = auth.user
            st.rerun()
    else:
        if st.session_state.user.email == "3dpeektech@gmail.com":
            t1, t2 = st.tabs(["🚀 Terminal", "⚖️ Admin Master"])
            with t1: render_terminal()
            with t2: render_admin()
        else:
            render_terminal()

if __name__ == "__main__":
    main()
