import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS Pro | Global SEO", page_icon="⚡", layout="wide")

# --- 2. GESTIÓN DE ACCESO ---
if "nivel_acceso" not in st.session_state:
    st.session_state["nivel_acceso"] = "Demo"

def login_sidebar():
    st.sidebar.title("⚡ NEXUS Pro Panel")
    if st.session_state["nivel_acceso"] == "Demo":
        st.sidebar.warning("Estado: Demo Gratuita")
        with st.sidebar.expander("🔓 Desbloquear Versión Pro"):
            key = st.text_input("License Key:", type="password")
            if st.button("Validar Acceso"):
                if key == "NEXUS2025":
                    st.session_state["nivel_acceso"] = "Pro"
                    st.rerun()
                else: st.sidebar.error("Key Inválida")
    else:
        st.sidebar.success("Estado: PRO ACTIVADO")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["nivel_acceso"] = "Demo"
            st.rerun()

# --- 3. MOTOR DE PDF PROFESIONAL (SIN ERRORES) ---
def crear_pdf_pro(texto, url, score, lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Lógica de fuentes segura
    font_name = "Arial"
    style_bold = 'B'
    
    if os.path.exists("Amiri-Regular.ttf"):
        try:
            pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
            font_name = "Amiri"
            style_bold = "" # Quitamos 'B' para evitar el error si no hay Amiri-Bold.ttf
        except: pass

    # Títulos dinámicos
    titulos = {
        "Arabic": {"t": "NEXUS تقرير", "s": "النتيجة:", "u": "تحليل لـ:", "align": "R"},
        "English": {"t": "NEXUS STRATEGIC REPORT", "s": "Score:", "u": "Analysis for:", "align": "L"},
        "Español": {"t": "REPORTE ESTRATÉGICO NEXUS", "s": "Puntuación:", "u": "Análisis para:", "align": "L"}
    }
    cfg = titulos.get(lang, titulos["English"])

    # Header seguro
    pdf.set_font(font_name, style_bold, 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, cfg["t"], ln=True, align=cfg["align"])
    
    pdf.set_font(font_name, style_bold, 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"{cfg['u']} {url} | {cfg['s']} {score}/100", ln=True, align=cfg["align"])
    pdf.ln(10)
    
    # Limpieza de texto para compatibilidad total
    txt_clean = texto.replace("**", "").replace("#", "").replace("`", "")
    
    pdf.set_font(font_name, size=11)
    align_body = 'R' if lang == "Arabic" else 'L'
    
    # Manejo de encodificación para evitar fallos de caracteres
    try:
        pdf.multi_cell(0, 8, txt_clean, align=align_body)
    except:
        pdf.multi_cell(0, 8, txt_clean.encode('latin-1', 'replace').decode('latin-1'), align=align_body)
    
    return bytes(pdf.output())

# --- 4. AGENTE DE IA ---
def ejecutar_auditoria(url, lang, acceso):
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except: return "Error: Configura tus API Keys.", 0

    with st.status(f"⚡ NEXUS {acceso} Mode...") as s:
        scrape = fc.scrape(url)
        content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        if acceso == "Demo":
            limit, prompt_type = 2500, "Brief summary (2 lines)"
        else:
            limit, prompt_type = 15000, "Deep audit (Errors, H1, Copy)"

        prompt = f"""
        You are NEXUS PRO SEO. 
        MANDATORY LANGUAGE: {lang}.
        TASK: {prompt_type} for {url}.
        FORMAT: Include 'SCORE: [0-100]'.
        Strictly write ONLY in {lang}.
        Content: {content[:limit]}
        """

        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        report = res.text
        
        score = 65
        if "SCORE:" in report:
            try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
            except: pass
            
        return report, score

# --- 5. INTERFAZ ---
login_sidebar()
st.title("⚡ NEXUS SEO Agent Pro")

target_url = st.text_input("URL del cliente:", placeholder="https://ejemplo.com")
idioma = st.selectbox("Idioma:", ["English", "Español", "Arabic", "German", "Portugues", "Italian", "Dutch"])

if st.button("🚀 INICIAR AUDITORÍA") and target_url:
    resultado, puntuacion = ejecutar_auditoria(target_url, idioma, st.session_state["nivel_acceso"])
    
    if resultado:
        st.divider()
        st.metric("SEO Score", f"{puntuacion}/100")
        st.markdown(resultado)
        
        if st.session_state["nivel_acceso"] == "Pro":
            pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma)
            st.download_button(f"📩 Descargar PDF ({idioma})", pdf_data, f"NEXUS_{target_url}.pdf", "application/pdf")
        else:
            st.warning("🔒 Compra la licencia Pro para descargar el PDF.")
