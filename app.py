import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import os

# --- 1. CONFIGURACIÓN DE MARCA Y PÁGINA ---
st.set_page_config(
    page_title="NEXUS Pro | Global SEO Intelligence",
    page_icon="⚡",
    layout="wide"
)

# --- 2. GESTIÓN DE ESTADO Y ACCESO (DEMO vs PRO) ---
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
                    st.error("Licencia inválida")
    else:
        st.sidebar.success("Estado: PRO ACTIVADO ✅")
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state["nivel_acceso"] = "Demo"
            st.rerun()

# --- 3. MOTOR DE GENERACIÓN PDF UNICODE ---
def crear_pdf_pro(texto, url, score, lang):
    # Usamos FPDF con soporte Unicode (fpdf2)
    pdf = FPDF()
    pdf.add_page()
    
    # Intentar cargar fuente para Árabe/Global si existe en el repo
    font_name = "Arial"
    if os.path.exists("Amiri-Regular.ttf"):
        try:
            pdf.add_font("Amiri", "", "Amiri-Regular.ttf")
            font_name = "Amiri"
        except:
            pass

    # Títulos según idioma
    titulos = {
        "English": "NEXUS STRATEGIC REPORT",
        "Español": "REPORTE ESTRATÉGICO NEXUS",
        "Arabic": "NEXUS تقرير",
        "German": "NEXUS STRATEGIEREPORT",
        "Italian": "RAPPORTO STRATEGICO NEXUS",
        "Dutch": "NEXUS STRATEGISCH RAPPORT",
        "Portugues": "RELATÓRIO ESTRATÉGICO NEXUS"
    }
    
    # Encabezado Premium
    pdf.set_font(font_name, 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, titulos.get(lang, titulos["English"]), ln=True, align='C')
    
    pdf.set_font(font_name, '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Analysis for: {url} | Score: {score}/100", ln=True, align='C')
    pdf.ln(10)
    
    # Cuerpo del Reporte
    pdf.set_font(font_name, size=11)
    # Limpieza para evitar errores de renderizado
    clean_text = texto.replace("**", "").replace("#", "").replace("`", "")
    
    align_body = 'R' if lang == "Arabic" else 'L'
    pdf.multi_cell(0, 8, clean_text, align=align_body)
    
    pdf.set_y(-20)
    pdf.set_font(font_name, 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS Pro - Intelligence for Agencies", align='C')
    
    return bytes(pdf.output())

# --- 4. AGENTE DE INTELIGENCIA IA (DEMO VS PRO) ---
def ejecutar_auditoria(url, lang, acceso):
    try:
        fc = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gg = genai.Client(api_key=st.secrets["GEMINI_KEY"])
    except:
        st.error("Error: Asegúrate de tener las Keys en Streamlit Secrets.")
        return None, 0

    with st.status(f"⚡ NEXUS Analizando ({acceso})...", expanded=True) as s:
        # 1. Scrapeo de contenido
        s.write("🕵️‍♂️ Escaneando sitio web...")
        try:
            data = fc.scrape(url)
            content = data.markdown if hasattr(data, 'markdown') else str(data)
        except Exception as e:
            st.error(f"Error al leer la web: {e}")
            return None, 0
        
        # 2. Configuración de potencia según el modo
        if acceso == "Demo":
            s.write("⚠️ Modo Demo: Generando resumen rápido...")
            limit = 2500
            prompt = f"Analiza brevemente el SEO de {url} en idioma {lang}. Da un SCORE: [0-100] y 2 consejos rápidos. Avisa que el reporte completo es versión Pro."
        else:
            s.write("🧠 Modo Pro: Ejecutando motores avanzados...")
            limit = 15000
            prompt = f"""Actúa como un Consultor SEO Pro. Todo el reporte debe estar en {lang}.
            Analiza {url} detalladamente:
            1. SCORE: [0-100]
            2. 3 Errores Críticos detallados.
            3. Sugerencias de H1 optimizados.
            4. Reescritura de Copywriting para conversión.
            Contenido: {content[:limit]}"""

        # 3. Consulta a la IA
        try:
            res = gg.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
            report = res.text
            
            # Extraer puntuación
            score = 65
            if "SCORE:" in report:
                try:
                    score = int(report.split("SCORE:")[1].split("\n")[0].strip(" []"))
                except: pass
                
            s.update(label="✅ Análisis Finalizado", state="complete")
            return report, score
        except Exception as e:
            st.error(f"Error en IA: {e}")
            return None, 0

# --- 5. INTERFAZ DE USUARIO PRINCIPAL ---
login_sidebar()

st.title("⚡ NEXUS SEO Agent Pro")
st.markdown("### Tu competencia usa ChatSEO. Tú usas Agentes Autónomos.")

if st.session_state["nivel_acceso"] == "Demo":
    st.info("💡 Estás en **Modo Demo**. Los reportes son cortos y no incluyen descarga de PDF.")

# Input de URL
target_url = st.text_input("URL a analizar:", placeholder="https://apple.com")

# Opciones de Idioma
idioma = st.selectbox("Selecciona el Idioma del Reporte:", 
                      ["Español", "English", "Arabic", "German", "Portugues", "Italian", "Dutch"])

if st.button("🚀 INICIAR AUDITORÍA") and target_url:
    resultado, puntuacion = ejecutar_auditoria(target_url, idioma, st.session_state["nivel_acceso"])
    
    if resultado:
        st.divider()
        c_score, c_info = st.columns([1, 2])
        
        with c_score:
            st.metric("Salud SEO Score", f"{puntuacion}/100")
            st.progress(puntuacion / 100)
        
        with c_info:
            if puntuacion < 50: st.error("¡Alerta! Necesita optimización urgente.")
            elif puntuacion < 85: st.warning("Buen sitio, pero con margen de mejora.")
            else: st.success("SEO excelente, sigue así.")

        st.markdown("---")
        st.markdown(resultado)
        
        # Bloque exclusivo para usuarios PRO
        if st.session_state["nivel_acceso"] == "Pro":
            st.success("✨ Reporte Pro Completo")
            pdf_data = crear_pdf_pro(resultado, target_url, puntuacion, idioma)
            st.download_button(
                label=f"📩 Descargar Reporte PDF ({idioma})",
                data=pdf_data,
                file_name=f"NEXUS_Audit_{idioma}_{target_url.replace('https://','')}.pdf",
                mime="application/pdf"
            )
        else:
            st.warning("🔒 Descarga de PDF y análisis profundo bloqueado. Activa la versión Pro para desbloquear.")
