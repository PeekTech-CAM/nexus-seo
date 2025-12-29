import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import datetime

# --- 1. ENTERPRISE ARCHITECTURE & SECURITY ---
# High-level secret management to avoid GitHub exposure
@st.cache_resource
def init_connections():
    try:
        # Crucial: Must be the API URL (https://xxx.supabase.co), not the Dashboard URL
        supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        firecrawl = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gemini = genai.Client(api_key=st.secrets["GEMINI_KEY"])
        return supabase, firecrawl, gemini
    except Exception as e:
        st.error(f"Initialization Failed: Ensure TOML secrets are correctly formatted. Error: {e}")
        st.stop()

supabase, firecrawl, gemini = init_connections()

# --- 2. SAAS PRODUCT TIERS (VALUE-BASED GATING) ---
# Designed for ROI-driven sales to businesses and agencies
PLANS = {
    "Demo": {
        "label": "Free Demo", 
        "depth": 3000, 
        "pdf": False, 
        "credits": 1,
        "model": "gemini-2.0-flash-exp"
    },
    "Starter": {
        "label": "Starter (€29/mo)", 
        "depth": 7000, 
        "pdf": True, 
        "credits": 5,
        "model": "gemini-2.0-flash-exp"
    },
    "Pro": {
        "label": "Pro (€79/mo)", 
        "depth": 18000, 
        "pdf": True, 
        "unlimited": True,
        "model": "gemini-2.0-flash-exp"
    },
    "Agency": {
        "label": "Agency (€199/mo)", 
        "depth": 25000, 
        "pdf": True, 
        "unlimited": True, 
        "white_label": True,
        "model": "gemini-2.0-pro-exp" # High-end model for enterprise reports
    }
}

st.set_page_config(page_title="NEXUS Pro | Enterprise SEO Intelligence", layout="wide")

# --- 3. DATABASE OPERATIONS (USER PROFILE MANAGEMENT) ---
def fetch_user_state(user_id):
    # Fetches real-time tier/credits from your Supabase profiles table
    try:
        res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data
    except:
        return None

def process_credit_deduction(user_id, current_credits, plan):
    # Only deducts for limited plans
    if not PLANS[plan].get("unlimited") and current_credits > 0:
        supabase.table("profiles").update({"credits": current_credits - 1}).eq("id", user_id).execute()

# --- 4. THE PRIORITIZATION ENGINE (AI STRATEGY) ---
def generate_strategic_audit(url, lang, tier):
    config = PLANS[tier]
    
    with st.status(f"⚡ NEXUS AI: Deep-Scanning {url}...") as status:
        # Data Acquisition via Firecrawl
        scrape = firecrawl.scrape(url)
        raw_content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # High-level Strategic Prompting for ROI
        prompt = f"""
        Role: Senior SEO Strategist for Enterprise Clients.
        Analyze: {url} in {lang}.
        Tier: {tier} (Context Depth: {config['depth']} chars).
        
        Deliverable Structure:
        1. EXECUTIVE SUMMARY & STRATEGIC SCORE (0-100)
        2. PRIORITIZED TECHNICAL ROADMAP:
           - [CRITICAL/HIGH] (Fix in <48hrs for immediate ROI)
           - [MEDIUM] (Strategic structural changes)
           - [LOW] (Long-term brand authority)
        3. CONTENT GAP ANALYSIS
        4. CONVERSION RATE OPTIMIZATION (CRO) SUGGESTIONS
        
        Language: {lang}. Content: {raw_content[:config['depth']]}
        """
        
        response = gemini.models.generate_content(model=config["model"], contents=prompt)
        return response.text

# --- 5. ENTERPRISE REPORT GENERATOR (PDF) ---
def export_professional_report(content, url, tier, logo=None):
    pdf = FPDF()
    pdf.add_page()
    is_agency = PLANS[tier].get("white_label", False)
    
    # White-Labeling for Agency Tier
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(40, 40, 40)
    header = "PROFESSIONAL SEO STRATEGY" if is_agency else "NEXUS STRATEGIC AUDIT"
    pdf.cell(0, 20, header, ln=True, align='L')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Analysis Date: {datetime.date.today()} | Target: {url}", ln=True)
    pdf.ln(10)
    
    # Body Content
    pdf.set_font("Arial", size=11)
    clean_text = content.replace("**", "").replace("#", "").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, clean_text)
    
    return bytes(pdf.output())

# --- 6. UNIFIED AUTHENTICATION INTERFACE ---
def render_auth_portal():
    st.sidebar.title("🔐 NEXUS Pro Access")
    action = st.sidebar.selectbox("Account Action", ["Login", "Create Account"])
    email = st.sidebar.text_input("Corporate Email")
    password = st.sidebar.text_input("Access Password", type="password")

    if action == "Create Account":
        if st.sidebar.button("Register & Initialize Profile"):
            try:
                # Triggers Supabase Auth + SQL Profile creation
                supabase.auth.sign_up({"email": email, "password": password})
                st.sidebar.success("Verification link sent to email.")
            except Exception as e:
                st.sidebar.error("Registration failed. Use a valid API URL in secrets.")
    else:
        if st.sidebar.button("Authorize Access"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.sidebar.error("Authentication invalid. Check credentials.")

# --- 7. MAIN PRODUCTION DASHBOARD ---
if "user" not in st.session_state:
    render_auth_portal()
    st.title("⚡ NEXUS Strategic SEO Intelligence")
    st.write("Professional-grade audits optimized for technical ROI and decision-making.")
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=2426&ixlib=rb-4.0.3")
else:
    # Production State Sync
    profile = fetch_user_state(st.session_state.user.id)
    if not profile:
        st.error("Profile not found. Contact support.")
        st.stop()
        
    tier = profile['plan_tier']
    credits = profile['credits']
    
    # Sidebar Metrics & Upsell logic
    st.sidebar.success(f"Enterprise Tier: {tier}")
    if not PLANS[tier].get("unlimited"):
        st.sidebar.metric("Analysis Credits", credits)
        st.sidebar.divider()
        st.sidebar.markdown("### 🚀 Need More Depth?")
        st.sidebar.link_button("Upgrade to Agency (€199)", "https://buy.stripe.com/agency_link")

    st.title("⚡ SEO Strategy Engine")
    col_a, col_b = st.columns([3, 1])
    
    with col_a:
        target_site = st.text_input("Target URL (Enterprise or Client Site):", placeholder="https://www.example.com")
    with col_b:
        target_lang = st.selectbox("Intelligence Language:", ["English", "Español", "Arabic", "German"])
    
    if st.button("🚀 EXECUTE STRATEGIC ANALYSIS") and target_site:
        # Enforcement of usage limits
        if not PLANS[tier].get("unlimited") and credits <= 0:
            st.error("🚨 Credit exhaustion. Upgrade required for additional audits.")
        else:
            report_text = generate_strategic_audit(target_site, target_lang, tier)
            st.divider()
            st.markdown(report_text)
            
            # Post-processing
            process_credit_deduction(st.session_state.user.id, credits, tier)
            
            # Gated Export Logic
            if PLANS[tier]["pdf"]:
                pdf_data = export_professional_report(report_text, target_site, tier)
                st.download_button("📩 Download PDF Strategy", pdf_data, f"NEXUS_Audit_{target_site}.pdf")
            else:
                st.warning("🔒 PDF Generation is restricted to Starter, Pro, and Agency tiers.")

    if st.sidebar.button("Terminate Session"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
