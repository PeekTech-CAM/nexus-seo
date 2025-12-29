import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE MARCA ---
st.set_page_config(
    page_title="NEXUS Pro | Global SEO Intelligence",
    page_icon="⚡",
    layout="wide"
)

# --- 2. GESTIÓN DE ACCESO (DEMO vs PRO) ---
if "nivel_acceso" not in st.session_state:
    st.session_state["nivel_acceso"] = "Demo"

def login_sidebar():
    st.sidebar.title("⚡ NEXUS Pro Panel")
    if st.session_state["nivel_acceso"] == "Demo":
        st.sidebar.warning("Estado: Demo Gratuita")
        with st.sidebar.expander("🔓 Desbloquear Versión Pro"):
            key = st.text_input("Introduce tu Licencia:", type="password")
            if st.button("Validar Acceso"):
                if key == "NEXUS2025":
                    st.session_state["nivel_acceso"] = "Pro"
                    st.success("¡Modo Pro Activado! ✅")
                    st.rerun()
                else:
                    st.sidebar.error("Licencia inválida")
    else:
        st.sidebar.success("Estado: PRO ACTIVADO ✅")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["nivel_acceso"] = "Demo"
            st.rerun()

# --- 3. MOTOR DE PDF PROFESIONAL ---
def crear_pdf_pro(texto, url, score, lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Soporte Unicode para Árabe y caracteres especiales
    font_name = "Arial"
    if os.path.exists("Amiri-Regular.ttf"):
        try:
            pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
            font_name = "Amiri"
        except: pass

    # Traducción de etiquetas fijas en el PDF
    labels = {
        "Arabic": {"t": "NEXUS تقرير", "s": "النتيجة:", "u": "تحليل لـ:", "align": "R"},
        "English": {"t": "NEXUS STRATEGIC REPORT", "s": "SEO Score:", "u": "Analysis for:", "align": "L"},
        "Español": {"t": "REPORTE ESTRATÉGICO NEXUS", "s": "Salud SEO:", "u": "Análisis para:", "align": "L"},
        "German": {"t": "NEXUS STRATEGIEREPORT", "s": "SEO-Score:", "u": "Analyse für:", "align": "L"},
        "Italian": {"t": "RAPPORTO STRATEGICO NEXUS", "s": "Punteggio SEO:", "u": "Analisi per:", "align": "L"},
        "Dutch": {"t": "NEXUS STRATEGISCH RAPPORT", "s": "SEO-Score:", "u": "Analyse voor:", "align": "L"},
        "Portugues": {"t": "RELATÓRIO ESTRATÉGICO NEXUS", "s": "Pontuação SEO:", "u": "Análise para:", "align": "L"}
    }
    cfg = labels.get(lang, labels["English"])

    # Encabezado
    pdf.set_font(font_name, 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, cfg["t"], ln=True, align=cfg["align"])
    
    pdf.set_font(font_name, '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"{cfg['u']} {url} | {cfg['s']} {score}/100", ln=True, align=cfg["align"])
    pdf.ln(10)
    
    # Limpieza de texto para evitar errores binarios
    txt_clean = texto.replace("**", "").replace("#", "").replace("`", "")
    
    pdf.set_font(font_name, size=11)
    align_body = 'R' if lang == "Arabic" else 'L'
    pdf.multi_cell(0, 8, txt_clean, align=align_body)
    
    pdf.set_y(-20)
    pdf.set_font(font_name, 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS Pro - Strategic Consulting", align='C')
    
    return bytes(pdf.output())

# --- 4. AGENTE IA (FUERZA DE IDIOMA REFORZADA) ---
def ejecutar_auditoria(url, lang, acceso):
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except:
        st.error("Configura FIRE_KEY y GEMINI_KEY en los Secrets.")
        return None, 0

    with st.status(f"⚡ NEXUS {acceso} Mode...", expanded=True) as s:
        s.write("🕵️‍♂️ Escaneando sitio web...")
        data = fc.scrape(url)
        content = data.markdown if hasattr(data, 'markdown') else str(data)
        
        # PROMPT REFORZADO POR IDIOMA
        if acceso == "Demo":
            limit = 2500
            prompt = f"""
            You are NEXUS SEO PRO. 
            MANDATORY LANGUAGE: {lang}. 
            Task: Brief SEO analysis of {url}.
            Format: Write 2 sentences in {lang} and include SCORE: [0-100].
            Strictly DO NOT use any other language than {lang}.
            Mention: 'Upgrade to Pro for full PDF' in {lang}.
            """
        else:
            limit = 15000
            prompt = f"""
            Act as a Senior SEO Consultant. 
            MANDATORY LANGUAGE: {lang}.
            Analyze {url} deeply. 
            Format:
            1. SCORE: [0-100]
            2. 3 Critical Errors.
            3. H1 Optimization Ideas.
            4. Copywriting Rewrite.
            Strictly DO NOT use any other language than {lang}.
            Content: {content[:limit]}
            """

        try:
            res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
            report = res.text
            
            score = 65
            if "SCORE:" in report:
                try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
                except: pass
                
            s.update(label="✅ Análisis Completo", state="complete")
            return report, score
        except Exception as e:
            st.error(f"Error IA: {e}")
            return None, 0

# --- 5. INTERFAZ DE USUARIO ---
login_sidebar()

st.title("⚡ NEXUS SEO Agent Pro")
st.markdown("### Inteligencia SEO Global para Agencias de Élite")

if st.session_state["nivel_acceso"] == "Demo":
    st.info("💡 Modo Demo: Reportes rápidos. PDF bloqueado.")

target_url = st.text_input("URL del cliente:", placeholder="https://ejemplo.com")

idioma = st.selectbox("Idioma del Reporte / Report Language:", 
                      ["Arabic", "Español", "English", "German", "Portugues", "Italian", "Dutch"])

if st.button("🚀 INICIAR AUDITORÍA"):
    if target_url:
        resultado, puntuacion = ejecutar_auditoria(target_url, idioma, st.session_state["nivel_acceso"])
        
        if resultado:
            st.divider()
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("SEO Score", f"{puntuacion}/100")
                st.progress(puntuacion / 100)
            
            st.markdown("---")
            st.markdown(resultado)
            
            # Bloque Pro
            if st.session_state["nivel_acceso"] == "Pro":
                pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma)
                st.download_button(
                    label=f"📩 Descargar Reporte PDF ({idioma})",
                    data=pdf_data,
                    file_name=f"NEXUS_{idioma}_{target_url.replace('https://','')}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("🔒 Versión Pro requerida para descargar el PDF y ver el análisis profundo.")
    else:
        st.error("Por favor introduce una URL.")
