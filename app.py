import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. SECURE CONFIGURATION ---
# Accessing the TOML secrets you just saved
try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"] # service_role key
    FIRE_KEY = st.secrets["FIRE_KEY"]
    GEMINI_KEY = st.secrets["GEMINI_KEY"]
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error("⚠️ Configuration Error: Check your Streamlit Secrets TOML format.")
    st.stop()

# --- 2. SAAS TIER DEFINITIONS ---
# ROI-driven gating for Starter, Pro, and Agency
PLANS = {
    "Demo": {"depth": 2500, "pdf": False, "label": "Free Demo", "credits": 1},
    "Starter": {"depth": 5000, "pdf": True, "label": "Starter (€29/mo)", "credits": 5},
    "Pro": {"depth": 15000, "pdf": True, "label": "Pro (€79/mo)", "unlimited": True},
    "Agency": {"depth": 20000, "pdf": True, "label": "Agency (€199/mo)", "white_label": True}
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO", page_icon="⚡", layout="wide")

# --- 3. DATABASE LOGIC ---
def get_user_profile(user_id):
    # Fetch tier/credits from the SQL table you created
    res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return res.data

def update_credits(user_id, current_credits):
    if current_credits > 0:
        supabase.table("profiles").update({"credits": current_credits - 1}).eq("id", user_id).execute()

# --- 4. PRIORITIZATION ENGINE ---
def run_strategic_audit(url, lang, tier):
    config = PLANS[tier]
    fc = Firecrawl(api_key=FIRE_KEY)
    gg = genai.Client(api_key=GEMINI_KEY)

    with st.status(f"⚡ NEXUS AI Analyzing {url}...") as status:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # Responding to Denise's feedback for "Clarity + Priority"
        prompt = f"""
        Act as a Senior SEO Strategist. Analyze {url} in {lang}.
        User Tier: {tier}. Analysis Depth: {config['depth']} chars.
        
        Deliver results optimized for business ROI:
        1. STRATEGIC SCORE: [0-100]
        2. PRIORITIZED ACTIONS:
           - [HIGH IMPACT] (Immediate fixes for revenue growth)
           - [MEDIUM IMPACT] (Structural/Content improvements)
           - [LOW IMPACT] (Long-term growth)
        3. COMPETITOR INSIGHTS.
        
        Content: {content[:config['depth']]}
        """
        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 5. PDF GENERATOR ---
def generate_pdf(text, url, tier):
    pdf = FPDF()
    pdf.add_page()
    is_agency = (tier == "Agency")
    
    # White-Label Branding for Agency Tier
    pdf.set_font("Arial", 'B', 16)
    title = "NEXUS STRATEGIC AUDIT" if not is_agency else "PROFESSIONAL SEO AUDIT"
    pdf.cell(0, 10, title, ln=True, align='C')
    
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, text.replace("**", "").replace("#", ""))
    return bytes(pdf.output())

# --- 6. MAIN INTERFACE ---
st.sidebar.title("⚡ NEXUS Pro Portal")

if "user" not in st.session_state:
    # Login Panel
    email = st.sidebar.text_input("Email")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            auth_res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = auth_res.user
            st.rerun()
        except: st.sidebar.error("Invalid Email/Password")
else:
    # Logged in: Fetch profile data
    user_info = get_user_profile(st.session_state.user.id)
    tier = user_info['plan_tier']
    credits = user_info['credits']
    
    st.sidebar.success(f"Current Plan: {tier}")
    if not PLANS[tier].get("unlimited"):
        st.sidebar.write(f"Credits Remaining: {credits}")
        st.sidebar.markdown("---")
        # Placeholder for your Stripe Payment Links
        st.sidebar.button("🚀 Upgrade Plan") 

    st.title("⚡ NEXUS Strategic SEO Agent")
    target_url = st.text_input("Client Website URL:", placeholder="https://example.com")
    lang = st.selectbox("Language:", ["English", "Español", "Arabic", "German"])
    
    if st.button("Generate Prioritized Audit") and target_url:
        # Check credit limits
        if not PLANS[tier].get("unlimited") and credits <= 0:
            st.error("🚨 Credit limit reached. Upgrade to continue.")
        else:
            report = run_strategic_audit(target_url, lang, tier)
            st.divider()
            st.markdown(report)
            
            # Deduct credit if applicable
            if not PLANS[tier].get("unlimited"):
                update_credits(st.session_state.user.id, credits)
            
            # PDF Export Gating
            if PLANS[tier]["pdf"]:
                pdf_file = generate_pdf(report, target_url, tier)
                st.download_button("📩 Download Professional PDF", pdf_file, f"Audit_{target_url}.pdf")
            else:
                st.warning("🔒 Upgrade to Starter or Pro to unlock PDF Exports.")

if st.sidebar.button("Log Out"):
    supabase.auth.sign_out()
    del st.session_state.user
    st.rerun()
