import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. STRATEGIC SAAS TIERS ---
# We sell clarity + ROI. Each tier unlocks more "Decision Power"
PLANS = {
    "Demo": {
        "depth": 2500, 
        "pdf": False, 
        "label": "Free Demo",
        "features": "Basic SEO Score"
    },
    "Starter": {
        "depth": 5000, 
        "pdf": True, 
        "label": "Starter (€29/mo)",
        "features": "Critical Errors + PDF Export"
    },
    "Pro": {
        "depth": 15000, 
        "pdf": True, 
        "label": "Pro (€79/mo)", 
        "features": "Prioritized Fixes + Deep Audit"
    },
    "Agency": {
        "depth": 20000, 
        "pdf": True, 
        "label": "Agency (€199/mo)", 
        "white_label": True, # For ROI-driven branding
        "features": "White-Label + All Languages"
    }
}

st.set_page_config(page_title="NEXUS Pro | Strategic SEO Agent", page_icon="⚡", layout="wide")

# --- 2. AUTH & PAYMENT GATEWAY (SIMULATED) ---
# In production, this connects to Supabase and Stripe
if "user_tier" not in st.session_state:
    st.session_state["user_tier"] = "Demo"

def login_sidebar():
    st.sidebar.title("⚡ NEXUS User Portal")
    
    # Simulate Plan Detection from Database
    st.session_state["user_tier"] = st.sidebar.selectbox(
        "Select Your Plan:", 
        options=list(PLANS.keys()), 
        index=list(PLANS.keys()).index(st.session_state["user_tier"])
    )
    
    config = PLANS[st.session_state["user_tier"]]
    st.sidebar.info(f"**Current:** {config['label']}\n\n**Included:** {config['features']}")
    
    if st.session_state["user_tier"] == "Demo":
        st.sidebar.markdown("---")
        # Stripe Payment Link Placeholder
        st.sidebar.button("🔓 Unlock Pro Features") 

# --- 3. THE PRIORITIZATION ENGINE (PDF) ---
def crear_pdf_pro(texto, url, score, lang, is_agency):
    pdf = FPDF()
    pdf.add_page()
    
    # Font Management
    font_name = "Arial"
    if os.path.exists("Amiri-Regular.ttf"):
        pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
        font_name = "Amiri"

    # White-Labeling for Agency Plan
    header = "NEXUS STRATEGIC AUDIT" if not is_agency else "PROFESSIONAL SEO AUDIT"
    
    pdf.set_font(font_name, size=22)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, header, ln=True, align='L')
    
    pdf.set_font(font_name, size=12)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(0, 10, f"Analysis for: {url} | Health Score: {score}/100", ln=True)
    pdf.ln(10)
    
    # Clean text and render
    txt_clean = texto.replace("**", "").replace("#", "").replace("`", "")
    pdf.set_font(font_name, size=11)
    pdf.multi_cell(0, 8, txt_clean)
    
    return bytes(pdf.output())

# --- 4. DEEP AUDIT LOGIC ---
def ejecutar_auditoria(url, lang, tier):
    config = PLANS[tier]
    
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except: return "Check API Keys in Secrets.", 0

    with st.status(f"⚡ Running {tier} Intelligence...") as s:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # PRIORITIZATION ENGINE PROMPT
        prompt = f"""
        Act as a Senior SEO Consultant. Analyze {url} in {lang}.
        User Tier: {tier}. Depth: {config['depth']} characters.
        
        OUTPUT STRUCTURE:
        1. SCORE: [0-100]
        2. PRIORITIZED ACTION ITEMS:
           - [HIGH IMPACT] (Fix immediately for Revenue/ROI)
           - [MEDIUM IMPACT] (Content & Structure)
           - [LOW IMPACT] (Optimization)
        3. STRATEGIC RECOMMENDATION.
        
        Language: {lang}. 
        Content: {content[:config['depth']]}
        """

        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        report = res.text
        
        score = 65
        if "SCORE:" in report:
            try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
            except: pass
            
        return report, score

# --- 5. UI FLOW ---
login_sidebar()

st.title("⚡ NEXUS SEO Agent Pro")
st.markdown("### Selling Clarity, Speed, and ROI.")

col1, col2 = st.columns([2, 1])
with col1:
    target_url = st.text_input("Target URL:", placeholder="https://example.com")
with col2:
    idioma = st.selectbox("Report Language:", ["English", "Español", "Arabic", "German"])

if st.button("🚀 GENERATE STRATEGIC AUDIT") and target_url:
    current_tier = st.session_state["user_plan"] if "user_plan" in st.session_state else st.session_state["user_tier"]
    resultado, puntuacion = ejecutar_auditoria(target_url, idioma, current_tier)
    
    if resultado:
        st.divider()
        st.metric("SEO ROI Score", f"{puntuacion}/100")
        st.markdown(resultado)
        
        # Access Gating
        if PLANS[current_tier]["pdf"]:
            is_agency = PLANS[current_tier].get("white_label", False)
            pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma, is_agency)
            st.download_button("📩 Download Professional PDF", pdf_data, f"NEXUS_{target_url}.pdf")
        else:
            st.warning("🔒 Upgrade to Starter or Pro to unlock PDF Reports and Deep Analysis.")
