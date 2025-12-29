import streamlit as st
from supabase import create_client, Client
import stripe
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURATION & SECRETS ---
# Ensure these are in your Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
FIRE_KEY = st.secrets["FIRE_KEY"]
GEMINI_KEY = st.secrets["GEMINI_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 2. SAAS TIER DEFINITIONS ---
# Selling Clarity + Speed + ROI
PLANS = {
    "Demo": {"depth": 2500, "pdf": False, "label": "Free Demo", "credits": 1},
    "Starter": {"depth": 5000, "pdf": True, "label": "Starter (€29/mo)", "credits": 5},
    "Pro": {"depth": 15000, "pdf": True, "label": "Pro (€79/mo)", "priority": True},
    "Agency": {"depth": 20000, "pdf": True, "label": "Agency (€199/mo)", "white_label": True}
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO", page_icon="⚡", layout="wide")

# --- 3. AUTHENTICATION HELPERS ---
def login_user(email, password):
    try:
        return supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None

def get_user_data(user_id):
    # Fetch tier and credits from the 'profiles' table you created
    res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
    return res.data

# --- 4. THE PRIORITIZATION ENGINE (AI LOGIC) ---
def run_strategic_audit(url, lang, tier):
    config = PLANS[tier]
    fc = Firecrawl(api_key=FIRE_KEY)
    gg = genai.Client(api_key=GEMINI_KEY)

    with st.status(f"⚡ NEXUS Intelligence analyzing {url}...") as status:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # Clarity + Action Prompt
        prompt = f"""
        Act as a Senior SEO Consultant. Analyze {url} in {lang}.
        Tier: {tier}. Depth: {config['depth']} chars.
        
        Structure your response for ROI:
        1. STRATEGIC SCORE: [0-100]
        2. PRIORITIZED ACTIONS (Address 'Clarity in Action'):
           - [HIGH IMPACT] (Immediate technical/content fixes)
           - [MEDIUM IMPACT] (Structural improvements)
           - [LOW IMPACT] (Long-term growth)
        3. COMPETITOR ANALYSIS (Brief).
        
        Content: {content[:config['depth']]}
        """
        
        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 5. PDF GENERATOR (WHITE-LABEL READY) ---
def generate_pdf(text, url, tier):
    pdf = FPDF()
    pdf.add_page()
    is_agency = PLANS[tier].get("white_label", False)
    
    # Header Branding
    pdf.set_font("Arial", 'B', 16)
    title = "NEXUS STRATEGIC AUDIT" if not is_agency else "PROFESSIONAL SEO AUDIT"
    pdf.cell(0, 10, title, ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Target: {url}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, text.replace("**", "").replace("#", ""))
    return bytes(pdf.output())

# --- 6. MAIN APP INTERFACE ---
st.sidebar.title("⚡ NEXUS Pro Panel")

if "user" not in st.session_state:
    # Login / Sign up Form
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    with tab1:
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            auth_res = login_user(email, pwd)
            if auth_res:
                st.session_state.user = auth_res.user
                st.rerun()
    with tab2:
        st.info("Direct users to your landing page or Stripe link to register")

else:
    # Logged In UI
    user_info = get_user_data(st.session_state.user.id)
    tier = user_info['plan_tier']
    credits = user_info['credits']
    
    st.sidebar.success(f"Plan: {tier}")
    if tier == "Demo":
        st.sidebar.write(f"Credits: {credits}/1")
        if st.sidebar.button("🚀 Upgrade to Pro"):
            st.sidebar.markdown("[Go to Stripe Checkout](https://buy.stripe.com/your_link)") #
    
    st.title("⚡ Strategic SEO Audit")
    st.write("Targeting high-impact decisions for your business.")
    
    target_url = st.text_input("Enter Website URL:", placeholder="https://example.com")
    lang = st.selectbox("Language:", ["English", "Español", "Arabic", "German"])
    
    if st.button("Run Audit") and target_url:
        # Check credits for Demo/Starter
        if tier == "Demo" and credits <= 0:
            st.error("Out of credits! Please upgrade to continue.")
        else:
            report = run_strategic_audit(target_url, lang, tier)
            st.markdown(report)
            
            # Deduct credit if Demo
            if tier == "Demo":
                supabase.table("profiles").update({"credits": credits - 1}).eq("id", st.session_state.user.id).execute()
            
            # PDF Access
            if PLANS[tier]["pdf"]:
                pdf_file = generate_pdf(report, target_url, tier)
                st.download_button("📩 Download Professional Report", pdf_file, "Audit.pdf")
            else:
                st.warning("🔒 Upgrade to Starter or Pro to download this as a PDF.")

if st.sidebar.button("Sign Out"):
    supabase.auth.sign_out()
    del st.session_state.user
    st.rerun()
