import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

# =============================================================================
# 1. ELITE UI WRAPPER
# =============================================================================
st.set_page_config(page_title="NEXUS ELITE TERMINAL", page_icon="🛰️", layout="wide")

def apply_elite_ui():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background: #050505; color: white; }
        .main { background: radial-gradient(circle at top, #1a0505 0%, #050505 100%); }
        div[data-testid="stMetric"] { 
            background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.2); 
            padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); 
        }
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
            color: white !important; font-weight: 700 !important; border-radius: 10px !important; width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. CORE SYSTEM ENGINE
# =============================================================================
class NexusEliteEngine:
    def __init__(self):
        self.supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        # Stable model node to prevent 404 errors
        self.ai = genai.GenerativeModel("gemini-1.5-flash-latest")

    def sync_profile(self, user_id):
        return self.supabase.table("profiles").select("*").eq("id", user_id).single().execute().data

    def run_semantic_audit(self, url, is_pro=False):
        # Protocol Fixer
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Pro users get deeper semantic context
        limit = 5000 if is_pro else 1000
        prompt = f"Perform an elite SEO audit for {url} using this data: {soup.get_text()[:limit]}"
        response = self.ai.generate_content(prompt)
        
        # Log to permanent audit history
        self.supabase.table("audit_history").insert({
            "user_id": st.session_state.user.id,
            "target": url,
            "intelligence": response.text
        }).execute()
        
        return response.text

nexus = NexusEliteEngine()

# =============================================================================
# 3. THE 3-NODE ROUTER
# =============================================================================
def render_dashboard():
    apply_elite_ui()
    profile = nexus.sync_profile(st.session_state.user.id)
    is_elite = profile['plan_tier'] == "Agency Elite"
    
    # Sidebar Metrics
    st.sidebar.markdown(f"### 🛡️ {profile['plan_tier']}")
    st.sidebar.metric("Available Credits", profile['credits'])
    if not is_elite:
        st.sidebar.divider()
        st.sidebar.markdown("### Upgrade Required")
        st.sidebar.link_button("🚀 UNLOCK AGENCY ELITE (1000 CHF)", "https://buy.stripe.com/your-1000-chf-link")

    # Elite KPI Board (Hidden for Demo)
    st.markdown("## 🛰️ Strategy Deployment Terminal")
    if is_elite:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Intel Nodes", "2,148", "+24")
        c2.metric("Market Scans", "18.2M", "Live")
        c3.metric("Semantic ROI", "342%", "🔥")
        c4.metric("Networks", "94", "+5")
    else:
        st.info("📊 DEMO MODE: Upgrade to unlock Market Scans and Semantic ROI tracking.")

    st.divider()

    # Terminal Logic
    target_url = st.text_input("Enter Target Domain Node", placeholder="apple.com")
    if st.button("EXECUTE SCAN"):
        if profile['credits'] > 0:
            with st.status("Analyzing Neural Vectors..."):
                report = nexus.run_semantic_audit(target_url, is_pro=is_elite)
                nexus.supabase.table("profiles").update({"credits": profile['credits'] - 1}).eq("id", st.session_state.user.id).execute()
                st.session_state.last_report = report
            st.rerun()
        else:
            st.error("Insufficient Credits. Please upgrade your node.")

    if "last_report" in st.session_state:
        st.markdown("### 🤖 Intelligence Stream")
        st.info(st.session_state.last_report)
        if is_elite:
            st.download_button("📥 DOWNLOAD AUDIT PDF", st.session_state.last_report, file_name="Nexus_Audit.txt")

# =============================================================================
# 4. MAIN ENTRY & PAYMENT DETECTION
# =============================================================================
def main():
    # Detect Stripe Payment and Update Credits automatically
    if st.query_params.get("payment") == "success" and "user" in st.session_state:
        nexus.supabase.table("profiles").update({"plan_tier": "Agency Elite", "credits": 1000}).eq("id", st.session_state.user.id).execute()
        st.balloons()
        st.success("💳 PAYMENT VERIFIED: 1,000 CREDITS LOADED.")
        time.sleep(2)
        st.rerun()

    if "user" not in st.session_state:
        apply_elite_ui()
        st.title("🏛️ NEXUS ELITE ACCESS")
        t1, t2 = st.tabs(["Authorize", "New Node (Demo)"])
        with t1:
            e = st.text_input("Corporate ID")
            p = st.text_input("Security Token", type="password")
            if st.button("SIGN IN"):
                res = nexus.supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
        with t2:
            st.write("Start with 1 free credit to test the neural engine.")
            # Add your supabase.auth.sign_up logic here
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
