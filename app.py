import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS Pro | Intelligence", page_icon="⚡", layout="wide")

# --- 2. SEGURIDAD ---
def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("🔐 NEXUS Pro Access")
            pwd = st.text_input("License Key:", type="password")
            if st.button("Activate"):
                if pwd == "NEXUS2025":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else: st.error("Invalid License")
        return False
    return True

# --- 3. CARGA DE SECRETOS ---
try:
    KEY_FC = st.secrets["FIRE_KEY"]
    KEY_GG = st.secrets["GEMINI_KEY"]
except:
    st.error("Missing API Keys in Streamlit Secrets.")
    st.stop()

# --- 4. GENERADOR DE PDF UNICODE (Powered by fpdf2) ---
def crear_pdf(texto, url, score, lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Soporte para Árabe y Unicode
    font_path = "Amiri-Regular.ttf"
    if os.path.exists(font_path):
        pdf.add_font("Amiri", "", font_path)
        font_name = "Amiri"
    else:
        font_name = "Arial" # Fallback

    # Traducciones de Interfaz de PDF
    labels = {
        "Arabic": {"t": "NEXUS تقرير", "s": "النتيجة:", "u": "تحليل لـ:", "align": "R"},
        "English": {"t": "NEXUS REPORT", "s": "Score:", "u": "Analysis for:", "align": "L"},
        "German": {"t": "NEXUS BERICHT", "s": "Ergebnis:", "u": "Analyse für:", "align": "L"},
        "Español": {"t": "REPORTE NEXUS", "s": "Puntuación:", "u": "Análisis para:", "align": "L"},
        "Portugues": {"t": "RELATÓRIO NEXUS", "s": "Pontuação:", "u": "Análise para:", "align": "L"},
        "Dutch": {"t": "NEXUS RAPPORT", "s": "Score:", "u": "Analyse voor:", "align": "L"},
        "Italian": {"t": "RAPPORTO NEXUS", "s": "Punteggio:", "u": "Analisi per:", "align": "L"}
    }
    
    cfg = labels.get(lang, labels["English"])
    
    # Header
    pdf.set_font(font_name, 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, cfg["t"], ln=True, align=cfg["align"])
    
    # Subheader
    pdf.set_font(font_name, '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"{cfg['u']} {url}", ln=True, align=cfg["align"])
    pdf.cell(0, 10, f"{cfg['s']} {score}/100", ln=True, align=cfg["align"])
    pdf.ln(10)
    
    # Body
    pdf.set_font(font_name, size=11)
    clean_text = texto.replace("**", "").replace("#", "").replace("`", "")
    
    # Renderizado con soporte RTL para Árabe
    align_body = 'R' if lang == "Arabic" else 'L'
    pdf.multi_cell(0, 8, clean_text, align=align_body)
    
    return bytes(pdf.output())

# --- 5. EJECUCIÓN DEL AGENTE ---
def run_nexus(url, lang):
    try:
        fc = Firecrawl(api_key=KEY_FC)
        gg = genai.Client(api_key=KEY_GG)
    except: return "Connection Error", 0

    with st.status(f"⚡ NEXUS Pro Analyzing ({lang})...") as s:
        try:
            # Scrape
            res_fc = fc.scrape(url)
            content = res_fc.markdown if hasattr(res_fc, 'markdown') else str(res_fc)
            
            # AI Logic
            prompt = f"""
            Act as NEXUS Pro SEO Consultant. All output MUST be in {lang}.
            Analyze: {url}
            1. Start with 'SCORE: [0-100]'.
            2. 3 Critical Errors, 3 H1 Ideas, 1 Copy Rewrite.
            Context: {content[:12000]}
            """
            
            # Model Fallback System
            for model_id in ["gemini-2.0-flash-exp", "gemini-1.5-pro"]:
                try:
                    res_gg = gg.models.generate_content(model=model_id, contents=prompt)
                    report = res_gg.text
                    break
                except: continue
            
            score = 65
            if "SCORE:" in report:
                try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
                except: pass
                
            s.update(label="✅ Analysis Complete", state="complete")
            return report, score
        except Exception as e:
            return f"Agent Error: {e}", 0

# --- 6. UI ---
if verificar_password():
    st.sidebar.title("⚡ NEXUS Pro")
    idioma = st.sidebar.selectbox("Language / Idioma", 
        ["English", "Español", "Arabic", "German", "Portugues", "Dutch", "Italian"])
    
    if st.sidebar.button("Logout"):
        st.session_state["autenticado"] = False
        st.rerun()

    st.title("⚡ NEXUS SEO Intelligence")
    url_target = st.text_input("URL:", placeholder="https://client-website.com")

    if st.button("🚀 GENERATE REPORT") and url_target:
        report_text, score_val = run_nexus(url_target, idioma)
        
        if score_val > 0:
            st.balloons()
            c1, c2 = st.columns([1, 2])
            c1.metric("SEO Score", f"{score_val}/100")
            c1.progress(score_val / 100)
            
            st.markdown("---")
            st.info(report_text)
            
            # Export
            pdf_data = crear_pdf(report_text, url_target, score_val, idioma)
            st.download_button(
                label=f"📩 Download PDF ({idioma})",
                data=pdf_data,
                file_name=f"NEXUS_{idioma}_{url_target.replace('https://','')}.pdf",
                mime="application/pdf"
            )
