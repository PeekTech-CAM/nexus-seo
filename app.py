import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. SAAS TIER CONFIGURATION ---
# People buy clarity + ROI, so we gate features by value
PLANS = {
    "Demo": {
        "depth": 2500, 
        "pdf": False, 
        "label": "Free Demo",
        "features": "Basic Score only"
    },
    "Starter": {
        "depth": 5000, 
        "pdf": True, 
        "label": "Starter Plan (€29)",
        "features": "Critical Errors + PDF"
    },
    "Pro": {
        "depth": 15000, 
        "pdf": True, 
        "label": "Pro Plan (€79)", 
        "features": "Deep Audit + Priority Fixes" # Addressing Denise's comment
    },
    "Agency": {
        "depth": 20000, 
        "pdf": True, 
        "label": "Agency Plan (€199)", 
        "white_label": True, # Branding for ROI
        "features": "White-Label + Multi-language"
    }
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO", page_icon="⚡", layout="wide")

# --- 2. AUTH & PLAN SIMULATION ---
if "user_plan" not in st.session_state:
    st.session_state["user_plan"] = "Demo"

def login_sidebar():
    st.sidebar.title("⚡ NEXUS SaaS Panel")
    
    # Tier Selector (This simulates your Stripe/Database connection)
    st.session_state["user_plan"] = st.sidebar.selectbox(
        "Current Subscription:", 
        options=list(PLANS.keys()), 
        index=list(PLANS.keys()).index(st.session_state["user_plan"])
    )
    
    current = PLANS[st.session_state["user_plan"]]
    st.sidebar.info(f"**Plan:** {current['label']}\n\n**Included:** {current['features']}")
    
    if st.session_state["user_plan"] == "Demo":
        st.sidebar.markdown("---")
        st.sidebar.button("🚀 Upgrade to Pro") # Placeholder for Stripe Link

# --- 3. THE PRIORITIZATION ENGINE (PDF) ---
def crear_pdf_pro(texto, url, score, lang, is_agency):
    pdf = FPDF()
    pdf.add_page()
    
    # Logic to handle fonts safely
    font_name = "Arial"
    if os.path.exists("Amiri-Regular.ttf"):
        pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
        font_name = "Amiri"

    # White-Label Check
    header_text = "NEXUS STRATEGIC REPORT" if not is_agency else "SEO AUDIT REPORT"
    
    pdf.set_font(font_name, size=20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, header_text, ln=True, align='L')
    
    pdf.set_font(font_name, size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"URL: {url} | Score: {score}/100", ln=True)
    pdf.ln(10)
    
    # Clean and write body
    txt_clean = texto.replace("**", "").replace("#", "")
    pdf.set_font(font_name, size=11)
    pdf.multi_cell(0, 8, txt_clean)
    
    return bytes(pdf.output())

# --- 4. AUDIT ENGINE ---
def ejecutar_auditoria(url, lang, plan_name):
    config = PLANS[plan_name]
    
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except: return "Check API Keys in Secrets.", 0

    with st.status(f"⚡ Running {plan_name} Analysis...") as s:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # PROMPT BASED ON CLARITY + PRIORITY
        prompt = f"""
        Act as a Senior SEO Strategist. Analyze {url} in {lang}.
        Plan Tier: {plan_name}. 
        Depth: {config['depth']} chars.
        
        FORMAT:
        1. SCORE: [0-100]
        2. PRIORITIZED ACTIONS:
           - [HIGH PRIORITY] (Do this first for immediate ROI)
           - [MEDIUM PRIORITY] (Secondary fixes)
           - [LOW PRIORITY] (Future growth)
        
        Strictly use {lang}. 
        Content context: {content[:config['depth']]}
        """

        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        report = res.text
        
        score = 65
        if "SCORE:" in report:
            try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
            except: pass
            
        return report, score

# --- 5. INTERFACE ---
login_sidebar()

st.title("⚡ NEXUS SEO Agent Pro")
st.caption("Selling Decisions, Not Features. Designed for Agencies.")

target_url = st.text_input("Client URL:", placeholder="https://client-site.com")
idioma = st.selectbox("Language:", ["English", "Español", "Arabic", "German"])

if st.button("🚀 GENERATE STRATEGIC AUDIT") and target_url:
    current_plan = st.session_state["user_plan"]
    resultado, puntuacion = ejecutar_auditoria(target_url, idioma, current_plan)
    
    if resultado:
        st.divider()
        st.metric("SEO Performance Score", f"{puntuacion}/100")
        st.markdown(resultado)
        
        # Access Gating
        if PLANS[current_plan]["pdf"]:
            is_agency = PLANS[current_plan].get("white_label", False)
            pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma, is_agency)
            st.download_button("📩 Download Strategic PDF", pdf_data, f"Audit_{target_url}.pdf")
        else:
            st.warning("🔒 Upgrade to Starter or Pro to download the prioritized PDF report.")
