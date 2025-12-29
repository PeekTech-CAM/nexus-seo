import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE MARCA ---
st.set_page_config(page_title="NEXUS Pro | Global SEO Intelligence", page_icon="⚡", layout="wide")

# --- 2. GESTIÓN DE ESTADO Y ACCESO ---
if "nivel_acceso" not in st.session_state:
    st.session_state["nivel_acceso"] = "Demo"

def login_sidebar():
    st.sidebar.title("⚡ NEXUS Pro Panel")
    if st.session_state["nivel_acceso"] == "Demo":
        st.sidebar.warning("Acceso: Demo Gratuita")
        with st.sidebar.expander("🔓 Activar Versión Pro"):
            key = st.text_input("Introduce tu Licencia:", type="password")
            if st.button("Validar Acceso"):
                if key == "NEXUS2025":
                    st.session_state["nivel_acceso"] = "Pro"
                    st.success("¡Modo Pro Activado!")
                    st.rerun()
                else:
                    st.error("Licencia inválida")
    else:
        st.sidebar.success("Acceso: PRO ACTIVADO ✅")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["nivel_acceso"] = "Demo"
            st.rerun()

# --- 3. MOTOR DE GENERACIÓN PDF UNICODE ---
def crear_pdf_pro(texto, url, score, lang):
    pdf = FPDF()
    pdf.add_page()
    
    # Soporte para fuentes globales (Asegúrate de tener el archivo .ttf en GitHub)
    font_name = "Arial"
    if os.path.exists("Amiri-Regular.ttf"):
        pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
        font_name = "Amiri"

    # Encabezado Premium
    pdf.set_font(font_name, 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, "NEXUS STRATEGIC AUDIT", ln=True, align='C')
    
    pdf.set_font(font_name, '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Analysis for: {url}", ln=True, align='C')
    pdf.cell(0, 10, f"SEO Health Score: {score}/100", ln=True, align='C')
    pdf.ln(10)
    
    # Cuerpo del Reporte
    pdf.set_font(font_name, size=11)
    # Limpieza de caracteres para evitar errores en el PDF
    clean_text = texto.encode('utf-8', 'ignore').decode('utf-8').replace("**", "").replace("#", "")
    
    align_body = 'R' if lang == "Arabic" else 'L'
    pdf.multi_cell(0, 8, clean_text, align=align_body)
    
    pdf.set_y(-20)
    pdf.set_font(font_name, 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS Pro - Reporte de Consultoría Estratégica", align='C')
    
    return bytes(pdf.output())

# --- 4. LÓGICA DEL AGENTE IA (DEMO VS PRO) ---
def ejecutar_auditoria(url, lang, acceso):
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except:
        st.error("Error de configuración de API Keys.")
        return None, 0

    with st.status(f"⚡ NEXUS Analizando ({acceso})...") as s:
        # 1. Scrape
        data = fc.scrape(url)
        content = data.markdown if hasattr(data, 'markdown') else str(data)
        
        # 2. Diferenciación de Potencia
        if acceso == "Demo":
            limit = 2500
            prompt = f"Eres NEXUS SEO. Idioma: {lang}. Haz un resumen MUY breve de 2 puntos sobre {url}. Di que para el reporte completo necesita Pro."
        else:
            limit = 15000
            prompt = f"""Actúa como Consultor SEO Pro. Idioma: {lang}. 
            Analiza {url} con Score: [0-100], 3 errores críticos, 3 ideas de H1 y mejora de copy.
            Contenido: {content[:limit]}"""

        # 3. Llamada a IA
        res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        report = res.text
        
        # 4. Cálculo de Score
        score = 65
        if "SCORE:" in report:
            try: score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
            except: pass
            
        s.update(label="✅ Análisis Finalizado", state="complete")
        return report, score

# --- 5. INTERFAZ DE USUARIO ---
login_sidebar()

st.title("⚡ NEXUS SEO Intelligence")
st.subheader("La herramienta definitiva para agencias y consultores")

if st.session_state["nivel_acceso"] == "Demo":
    st.info("💡 Estás usando la **Demo Gratuita**. Desbloquea el modo **Pro** para obtener reportes detallados, PDF descargables y soporte multi-idioma completo.")

# Input Principal
target_url = st.text_input("Introduce la URL de la web a analizar:", placeholder="https://tu-cliente.com")

# Opciones Pro
col1, col2 = st.columns(2)
with col1:
    idioma = st.selectbox("Idioma del Reporte", ["Español", "English", "Arabic", "German", "Portugues", "Italian", "Dutch"])
with col2:
    if st.session_state["nivel_acceso"] == "Pro":
        st.write("✨ Opciones Pro activadas: Reporte Profundo + PDF")
    else:
        st.write("🔒 Opciones Pro bloqueadas")

if st.button("🚀 INICIAR AUDITORÍA") and target_url:
    resultado, puntuacion = ejecutar_auditoria(target_url, idioma, st.session_state["nivel_acceso"])
    
    if resultado:
        st.divider()
        c_score, c_info = st.columns([1, 2])
        c_score.metric("SEO Score", f"{puntuacion}/100")
        c_score.progress(puntuacion / 100)
        
        st.markdown("### 📝 Análisis de Resultados")
        st.markdown(resultado)
        
        # Botón de Descarga SOLO para Pro
        if st.session_state["nivel_acceso"] == "Pro":
            st.success("Reporte Profesional generado.")
            pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma)
            st.download_button(
                label="📩 Descargar Auditoría PDF",
                data=pdf_data,
                file_name=f"NEXUS_Pro_{target_url.replace('https://','')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("⚠️ La descarga de PDF y el análisis detallado están desactivados en la Demo.")
