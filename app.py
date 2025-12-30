import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import numpy as np
import time
from datetime import datetime
import streamlit.components.v1 as components

# --- 1. TRACKING INJECTION (FIXED) ---
def inject_tracking():
    """Injects GTM tracking into the Streamlit sandboxed environment."""
    # Your verified ID from screenshot image_22dfa3.png
    GTM_ID = "GTM-KXF6VCFJ"
    
    gtm_code = f"""
        <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
        new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
        j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
        'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        }})(window,document,'script','dataLayer','{GTM_ID}');</script>
        """
    # This must be indented exactly 4 spaces inside the function
    components.html(gtm_code, height=0)

# --- 2. CORE ENTERPRISE ENGINE ---
class NexusEliteEngine:
    def __init__(self):
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            try:
                # Try the latest production-stable model name
                self.ai = genai.GenerativeModel('gemini-1.5-flash')
                # If that fails, the SDK might require the 'models/' prefix
                # self.ai = genai.GenerativeModel('models/gemini-1.5-flash')
            except Exception:
                self.ai = None

    def safe_audit(self, prompt):
        if not self.ai:
            return "AI Node Offline. Check API Key permissions."
        try:
            response = self.ai.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Intelligence Stream Error: {str(e)}"

    def sync_user(self, user_id):
        res = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data

nexus = NexusEliteEngine()

# --- 3. LUXURY COMMAND UI ---
def apply_elite_ui():
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

# --- 4. DYNAMIC TERMINAL ---
def render_terminal():
    apply_elite_ui()
    profile = nexus.sync_user(st.session_state.user.id)
    
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

# --- 5. ADMIN OVERLORD ---
def render_admin():
    st.title("⚖️ Admin Overlord Terminal")
    try:
        response = nexus.supabase.table("profiles").select("*").execute()
        users = response.data
        if users:
            df = pd.DataFrame(users)
            cols = ['email', 'plan_tier', 'credits', 'created_at']
            valid = [c for c in cols if c in df.columns]
            st.dataframe(df[valid], use_container_width=True)
    except Exception as e:
        st.error(f"Admin Error: {e}")

# --- 6. MAIN ROUTER ---
def main():
    inject_tracking()
    
    # 1. AUTHENTICATION GATE
    if "user" not in st.session_state:
        render_public_landing() # Registration, Demo info, and Pro upgrade links
    else:
        profile = nexus.sync_user(st.session_state.user.id)
        
        # 2. ADMIN NODE (Exclusive to you)
        if profile['email'] == "3dpeektech@gmail.com":
            render_admin_master()
            
        # 3. CLIENT NODE (Features based on Tier)
        else:
            if profile['plan_tier'] == 'Demo':
                render_demo_terminal(profile)
            elif profile['plan_tier'] == 'Starter':
                render_starter_terminal(profile)
            elif profile['plan_tier'] == 'Agency Elite':
                render_elite_terminal(profile)
    else:
        # Admin check for your specific node
        if st.session_state.user.email == "3dpeektech@gmail.com":
            t1, t2 = st.tabs(["🚀 Terminal", "⚖️ Admin Master"])
            with t1: render_terminal()
            with t2: render_admin()
        else:
            render_terminal()

if __name__ == "__main__":
    main()
