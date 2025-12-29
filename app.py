import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. SECURE INITIALIZATION ---
try:
    # Pulling from TOML to prevent security leaks
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"] 
    FIRE_KEY = st.secrets["FIRE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Secrets Missing: Configure TOML in Streamlit Cloud Settings.")
    st.stop()

# --- 2. SAAS TIER DEFINITIONS ---
# Gating features by business value
PLANS = {
    "Demo": {"depth": 2500, "pdf": False, "label": "Free Demo", "credits": 1},
    "Starter": {"depth": 5000, "pdf": True, "label": "Starter (€29)", "credits": 5},
    "Pro": {"depth": 15000, "pdf": True, "label": "Pro (€79)", "unlimited": True},
    "Agency": {"depth": 20000, "pdf": True, "label": "Agency (€199)", "white_label": True}
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO", page_icon="⚡", layout="wide")

# --- 3. CORE LOGIC FUNCTIONS ---
def get_user_profile(user_id):
    # Fetch plan and credits from Supabase
    res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return res.data

def update_credits(user_id, current_credits):
    if current_credits > 0:
        supabase.table("profiles").update({"credits": current_credits - 1}).eq("id", user_id).execute()

def run_strategic_audit(url, lang, tier):
    config = PLANS[tier]
    fc = Firecrawl(api_key=FIRE_KEY)
    gg = genai.Client(api_key=GEMINI_KEY)

    with st.status(f"⚡ NEXUS AI Analyzing {url}...") as status:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # Optimized for "Clarity in Action"
        prompt = f"""
        Act as a Senior SEO Strategist. Analyze {url} in {lang}. Tier: {tier}.
        Format for ROI:
        1. STRATEGIC SCORE: [0-100]
        2. [HIGH IMPACT] Actions (Do these first)
        3. [MEDIUM/LOW IMPACT] Actions
        Content: {content[:config['depth']]}
        """
        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 4. AUTHENTICATION & REGISTRATION ---
def auth_ui():
    st.sidebar.title("🔐 NEXUS Pro Access")
    choice = st.sidebar.radio("Action", ["Login", "Sign Up"])
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.sidebar.button("Create Account"):
            try:
                # This triggers the Supabase trigger to create the profile
                res = supabase.auth.sign_up({"email": email, "password": password})
                st.sidebar.success("Check your email for confirmation!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    else:
        if st.sidebar.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.sidebar.error("Invalid credentials.")

# --- 5. MAIN APP FLOW ---
if "user" not in st.session_state:
    auth_ui()
    st.title("⚡ Welcome to NEXUS SEO")
    st.info("Log in or create an account to start your prioritized SEO audit.")
else:
    # User is logged in
    user_info = get_user_profile(st.session_state.user.id)
    tier = user_info['plan_tier']
    credits = user_info['credits']
    
    st.sidebar.success(f"Plan: {tier}")
    
    # Feature Gating & Stripe Integration
    if not PLANS[tier].get("unlimited"):
        st.sidebar.write(f"Credits: {credits}")
        st.sidebar.markdown("---")
        st.sidebar.link_button("🚀 Upgrade for Unlimited", "https://buy.stripe.com/your_pro_link")

    st.title("⚡ Strategic SEO Engine")
    target_url = st.text_input("Enter Website URL (include https://):")
    lang = st.selectbox("Report Language:", ["English", "Español", "Arabic", "German"])
    
    if st.button("Generate Prioritized Audit") and target_url:
        if not PLANS[tier].get("unlimited") and credits <= 0:
            st.error("🚨 Credit limit reached. Please upgrade to continue.")
        else:
            report = run_strategic_audit(target_url, lang, tier)
            st.divider()
            st.markdown(report)
            
            # Auto-deduct credit
            if not PLANS[tier].get("unlimited"):
                update_credits(st.session_state.user.id, credits)
            
            # Gated PDF Download
            if PLANS[tier]["pdf"]:
                # Simple PDF Generation
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=11)
                pdf.multi_cell(0, 10, report.replace("**", "").replace("#", ""))
                st.download_button("📩 Download PDF Report", bytes(pdf.output()), f"Audit_{target_url}.pdf")

    if st.sidebar.button("Log Out"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
