import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. SECURE CONFIGURATION (PULLING FROM TOML) ---
# This setup prevents API keys from being leaked in your code
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
# Tiers are gated by analysis depth and feature access
PLANS = {
    "Demo": {"depth": 2500, "pdf": False, "label": "Free Demo", "credits": 1},
    "Starter": {"depth": 5000, "pdf": True, "label": "Starter (€29/mo)", "credits": 5},
    "Pro": {"depth": 15000, "pdf": True, "label": "Pro (€79/mo)", "unlimited": True},
    "Agency": {"depth": 20000, "pdf": True, "label": "Agency (€199/mo)", "white_label": True}
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO", page_icon="⚡", layout="wide")

# --- 3. DATABASE LOGIC (SUPABASE) ---
def get_user_profile(user_id):
    # Fetch user tier and credit count from your 'profiles' table
    res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return res.data

def update_credits(user_id, current_credits):
    # Automatically deducts one credit after a successful audit
    if current_credits > 0:
        supabase.table("profiles").update({"credits": current_credits - 1}).eq("id", user_id).execute()

# --- 4. PRIORITIZATION ENGINE (AI LOGIC) ---
def run_strategic_audit(url, lang, tier):
    config = PLANS[tier]
    fc = Firecrawl(api_key=FIRE_KEY)
    gg = genai.Client(api_key=GEMINI_KEY)

    with st.status(f"⚡ NEXUS AI Analyzing {url}...") as status:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # This prompt is optimized for ROI and clarity
        prompt = f"""
        Act as a Senior SEO Strategist. Analyze {url} in {lang}.
        User Tier: {tier}. Analysis Depth: {config['depth']} chars.
        
        Structure results for maximum business ROI:
        1. STRATEGIC SCORE: [0-100]
        2. PRIORITIZED ACTION ITEMS:
           - [HIGH IMPACT] (Immediate fixes for revenue/growth)
           - [MEDIUM IMPACT] (Structural/Content improvements)
           - [LOW IMPACT] (Long-term growth)
        3. COMPETITOR INSIGHTS.
        
        Content context: {content[:config['depth']]}
        """
        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 5. PDF GENERATOR (GATED BRANDING) ---
def generate_pdf(text, url, tier):
    pdf = FPDF()
    pdf.add_page()
    is_agency = (tier == "Agency")
    
    # White-Label Branding logic for the Agency tier
    pdf.set_font("Arial", 'B', 16)
    title = "NEXUS STRATEGIC AUDIT" if not is_agency else "PROFESSIONAL SEO AUDIT"
    pdf.cell(0, 10, title, ln=True, align='C')
    
    pdf.set_font("Arial", size=11)
    # Clean text to prevent PDF encoding errors
    clean_text = text.replace("**", "").replace("#", "").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, clean_text)
    return bytes(pdf.output())

# --- 6. MAIN INTERFACE ---
st.sidebar.title("⚡ NEXUS Pro Portal")

if "user" not in st.session_state:
    # Login / Access Management
    email = st.sidebar.text_input("Email")
    pwd = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        try:
            auth_res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            st.session_state.user = auth_res.user
            st.rerun()
        except: st.sidebar.error("Invalid Login Credentials")
else:
    # Load profile data from Supabase
    user_info = get_user_profile(st.session_state.user.id)
    tier = user_info['plan_tier']
    credits = user_info['credits']
    
    st.sidebar.success(f"Current Plan: {tier}")
    
    # Feature Gating & Upsell
    if not PLANS[tier].get("unlimited"):
        st.sidebar.write(f"Credits Remaining: {credits}")
        st.sidebar.markdown("---")
        # Replace these URLs with your Stripe Payment Links
        st.sidebar.link_button("🚀 Upgrade to Pro (€79)", "https://buy.stripe.com/your_pro_link")

    st.title("⚡ Strategic SEO Agent")
    target_url = st.text_input("Enter Client URL:", placeholder="https://example.com")
    lang = st.selectbox("Report Language:", ["English", "Español", "Arabic", "German"])
    
    if st.button("Generate Prioritized Audit") and target_url:
        # Check credit limits before running AI
        if not PLANS[tier].get("unlimited") and credits <= 0:
            st.error("🚨 Credit limit reached. Please upgrade to continue.")
        else:
            report = run_strategic_audit(target_url, lang, tier)
            st.divider()
            st.markdown(report)
            
            # Deduct credit after success
            if not PLANS[tier].get("unlimited"):
                update_credits(st.session_state.user.id, credits)
            
            # Gated PDF Download
            if PLANS[tier]["pdf"]:
                pdf_file = generate_pdf(report, target_url, tier)
                st.download_button("📩 Download Professional PDF", pdf_file, f"Audit_{target_url}.pdf")
            else:
                st.warning("🔒 PDF Exports are locked. Upgrade to Starter or Pro to unlock.")

if st.sidebar.button("Log Out"):
    supabase.auth.sign_out()
    del st.session_state.user
    st.rerun()
