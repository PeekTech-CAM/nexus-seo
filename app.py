import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import time
from datetime import datetime

# --- 1. CORE ENTERPRISE SYSTEM ---
class NexusEliteSaaS:
    def __init__(self):
        """Initializes secure database, AI nodes, and pulls billing from secrets."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            self.ai = genai.GenerativeModel("gemini-1.5-pro")
        
        # Stripe URLs securely stored in Streamlit Secrets
        self.billing = {
            "Pro": st.secrets.get("STRIPE_PRO_URL", "https://buy.stripe.com/error"),
            "Agency": st.secrets.get("STRIPE_AGENCY_URL", "https://nexus.ai/contact")
        }

    def sync_user_data(self, user_id):
        """Fetches tier and credits from the 'profiles' table."""
        res = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data

    def get_global_scan_count(self):
        """Counts every audit performed on the platform."""
        res = self.supabase.table("audit_history").select("id", count="exact").execute()
        return res.count if res.count else 0

nexus = NexusEliteSaaS()
class NexusEliteEngine:
    def __init__(self):
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            # USE THIS SPECIFIC MODEL NAME FOR STABILITY
            self.model_name = 'gemini-1.5-flash' # Flash is faster and more widely available
            try:
                self.ai = genai.GenerativeModel(self.model_name)
            except Exception:
                self.ai = None

    def safe_generate_audit(self, prompt):
        """Fail-safe AI generation to prevent 'NotFound' crashes."""
        if not self.ai:
            return "AI Node Offline: Check API Key or Model Name in Secrets."
        try:
            response = self.ai.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Intelligence Stream Interrupted: {str(e)}"
# --- 2. ELITE UI ARCHITECTURE ---
def apply_elite_ui():
    """Renders the obsidian-crimson design system."""
    st.set_page_config(page_title="Nexus GPT-SEO Terminal", page_icon="🛰️", layout="wide")
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Space Grotesk', sans-serif; background: #050505; color: white; }}
        .main {{ background: radial-gradient(circle at top, #1a0505 0%, #050505 100%); }}
        div[data-testid="stMetric"] {{ 
            background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.2); 
            padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); 
        }}
        .stButton>button {{
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
            color: white !important; border: none !important; font-weight: 700 !important;
            border-radius: 10px !important; height: 3.5rem !important; width: 100% !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- 3. PRODUCTION DASHBOARD ---
def render_terminal():
    apply_elite_ui()
    
    # Live Data Fetch
    profile = nexus.sync_user_data(st.session_state.user.id)
    global_scans = nexus.get_global_scan_count()
    
    # 🛰️ Header & Metrics
    st.markdown("## 🛰️ Strategy Deployment Terminal")
    st.sidebar.markdown(f"**Node:** {profile['email']}")
    st.sidebar.markdown(f"**Tier:** {profile['plan_tier']}")
    st.sidebar.markdown(f"**Credits:** {profile['credits']}")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nodes", "2,148", "+24")
    c2.metric("Market Scans", f"{global_scans + 18200000:,}", "Live")
    c3.metric("Semantic ROI", "342%", "🔥")
    c4.metric("Networks", "94", "+5")

    st.divider()

    # --- GPT-SEO ENGINE ---
    col_l, col_r = st.columns([1, 1.2])
    
    with col_l:
        st.subheader("🤖 AI Semantic Audit")
        target = st.text_input("Target Domain", placeholder="example.com")
        comp = st.text_input("Top Competitor", placeholder="competitor.com")
        
        if st.button("EXECUTE STRATEGIC SCAN"):
            if profile['credits'] > 0:
                with st.status("Analyzing Search Vectors..."):
                    # Custom GPT-SEO Logic
                    prompt = f"Perform an elite SEO semantic gap analysis for {target} vs {comp}."
                    intel = nexus.ai.generate_content(prompt).text
                    # Log Audit & Decrement Credit
                    nexus.supabase.table("audit_history").insert({
                        "user_id": st.session_state.user.id, "target": target, "intelligence": intel
                    }).execute()
                    nexus.supabase.table("profiles").update({
                        "credits": profile['credits'] - 1
                    }).eq("id", st.session_state.user.id).execute()
                    st.session_state.last_audit = intel
                st.rerun()
            else:
                st.error("Insufficient Credits. Upgrade to Pro Tier.")
        
        st.divider()
        st.markdown("### 💎 Premium Upgrades")
        st.link_button("🚀 Upgrade to Pro (Unlimited Audits)", nexus.billing["Pro"])

    with col_r:
        if "last_audit" in st.session_state:
            st.info(st.session_state.last_audit)
            # White-Label PDF Framework
            st.download_button("📥 DOWNLOAD BRANDED REPORT (PDF)", 
                             data=st.session_state.last_audit, 
                             file_name=f"Nexus_Audit_{datetime.now().strftime('%Y%m%d')}.txt")
        else:
            st.markdown("<div style='border:1px dashed #444; padding:50px; text-align:center;'>Awaiting Deployment...</div>", unsafe_allow_html=True)

# --- 4. ADMIN MASTER VIEW ---
def render_admin():
    st.title("⚖️ Admin Overlord Terminal")
    try:
        # Fetch all user data from Supabase
        response = nexus.supabase.table("profiles").select("*").execute()
        users = response.data
        
        if users:
            df = pd.DataFrame(users)
            
            # Define the columns we WANT to show
            target_cols = ['email', 'plan_tier', 'credits', 'created_at']
            
            # Only select columns that actually exist in the database to prevent KeyError
            available_cols = [col for col in target_cols if col in df.columns]
            
            st.subheader(f"👤 Organization Nodes ({len(users)})")
            st.dataframe(df[available_cols], use_container_width=True)
            
            # Raw Data Inspector for Debugging
            with st.expander("🛠️ Debug: Raw Database JSON"):
                st.write(users)
        else:
            st.info("No organization nodes detected in the database.")
            
    except Exception as e:
        st.error(f"Terminal Connection Error: {e}")

# --- 5. SYSTEM ROUTER ---
def main():
    if "user" not in st.session_state:
        # User is here because email confirmation is OFF
        apply_elite_ui()
        st.markdown("<h1 style='text-align:center;'>🏛️ NEXUS ELITE ACCESS</h1>", unsafe_allow_html=True)
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        if st.button("AUTHORIZE ACCESS"):
            try:
                auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = auth.user
                st.rerun()
            except Exception as e:
                st.error(f"Access Denied: {e}")
    else:
        # Private Admin Access for your verified account
        if st.session_state.user.email == "3dpeektech@gmail.com":
            tab1, tab2 = st.tabs(["🚀 Terminal", "⚖️ Admin Master"])
            with tab1: render_terminal()
            with tab2: render_admin()
        else:
            render_terminal()

if __name__ == "__main__":
    main()
