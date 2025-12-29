import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import time

# ==========================================
# 🛑 CONFIGURACIÓN DE LLAVES (Hardcoded para tu uso privado)
# ==========================================
# Busca la zona de llaves y cámbiala por esto:
KEY_FIRECRAWL = st.secrets["FIRE_KEY"]
KEY_GOOGLE = st.secrets["GEMINI_KEY"]

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS SEO Agent", page_icon="⚡", layout="wide")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    .report-card { padding: 20px; border-radius: 10px; background-color: #1e2129; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN: GENERADOR DE PDF ---
def crear_pdf(texto_reporte, url_analizada):
    pdf = FPDF()
    pdf.add_page()
    
    # Título y Branding
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "NEXUS: Reporte de Inteligencia SEO", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Analisis para: {url_analizada}", ln=True, align='C')
    pdf.ln(10)
    
    # Limpieza de texto para evitar errores de codificación en PDF
    # Eliminamos símbolos de Markdown para el documento final
    texto_limpio = texto_reporte.replace("**", "").replace("#", "").replace("`", "")
    
    pdf.set_font("Arial", size=11)
    # multi_cell ajusta el texto automáticamente al ancho de la página
    pdf.multi_cell(0, 8, texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.set_y(-20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS AI - Agente Autonomo de Auditoria", align='C')
    
    return pdf.output(dest='S')

# --- FUNCIÓN: AGENTE DE INTELIGENCIA ---
def ejecutar_agente_nexus(url):
    # Inicialización de clientes
    try:
        app = Firecrawl(api_key=KEY_FIRECRAWL)
        client = genai.Client(api_key=KEY_GOOGLE)
    except Exception as e:
        return f"Error de configuración: {e}", None

    with st.status("🕵️‍♂️ NEXUS analizando sitio...", expanded=True) as status:
        # 1. Extracción de datos
        st.write("👀 Extrayendo contenido con Firecrawl...")
        try:
            scrape_result = app.scrape(url)
            # Manejo de respuesta flexible
            if hasattr(scrape_result, 'markdown'):
                contenido = scrape_result.markdown
            elif isinstance(scrape_result, dict):
                contenido = scrape_result.get('markdown') or scrape_result.get('data', {}).get('markdown', str(scrape_result))
            else:
                contenido = str(scrape_result)
        except Exception as e:
            status.update(label="❌ Error de lectura", state="error")
            return f"Error al leer la web: {e}", None

        # 2. Procesamiento IA con Auto-Recuperación
        st.write("🧠 Generando estrategia SEO de alto nivel...")
        prompt = f"""
        Actúa como NEXUS, el agente SEO más avanzado.
        Analiza este sitio: {url}
        Contenido extraído:
        ---
        {contenido[:15000]}
        ---
        TAREA: Genera un reporte profesional que incluya:
        1. ANÁLISIS CRÍTICO: 3 errores que bloquean el crecimiento.
        2. ESTRATEGIA DE TÍTULOS: 3 opciones de H1 optimizados.
        3. COPYWRITING: Reescribe la sección hero (primer párrafo) para conversión.
        4. ACCIÓN: Plan de implementación de 3 pasos.
        Responde de forma directa y profesional.
        """

        # Lista jerárquica de modelos (si uno falla, prueba el siguiente)
        modelos = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
        
        resultado_ia = None
        for mod in modelos:
            try:
                st.write(f"🔌 Conectando motor: `{mod}`...")
                response = client.models.generate_content(model=mod, contents=prompt)
                resultado_ia = response.text
                if resultado_ia:
                    status.update(label="✅ Análisis finalizado con éxito", state="complete")
                    break
            except Exception as e:
                continue
        
        if not resultado_ia:
            status.update(label="❌ Error de IA", state="error")
            return "No se pudo conectar con los modelos de Gemini. Revisa tu cuota de API.", None
        
        return resultado_ia, contenido

# --- INTERFAZ DE USUARIO (FRONTEND) ---
st.title("⚡ NEXUS: Agente SEO Autónomo")
st.markdown("Genera auditorías de nivel agencia en segundos usando Inteligencia Artificial.")

# Layout de columnas
col1, col2 = st.columns([2, 1])

with col1:
    url_input = st.text_input("URL del sitio web a optimizar:", placeholder="https://ejemplo.com")

with col2:
    st.write(" ") # Espaciador
    boton_run = st.button("🚀 AUDITAR AHORA")

if boton_run:
    if not url_input:
        st.error("Por favor, introduce una URL válida.")
    else:
        resultado, raw_data = ejecutar_agente_nexus(url_input)
        
        if "Error" in resultado and len(resultado) < 100:
            st.error(resultado)
        else:
            st.balloons()
            
            # Mostrar Reporte en Pantalla
            st.markdown("---")
            st.subheader(f"📊 Reporte Estratégico para {url_input}")
            
            with st.container():
                st.markdown(f'<div class="report-card">{resultado}</div>', unsafe_allow_html=True)
            
            st.markdown(" ")
            
            # Opción de Descarga PDF
            try:
                pdf_data = crear_pdf(resultado, url_input)
                st.download_button(
                    label="📩 Descargar Reporte en PDF",
                    data=pdf_data,
                    file_name=f"Auditoria_NEXUS_{url_input.replace('https://', '').replace('/', '_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.warning(f"Nota: El reporte está listo, pero el PDF tuvo un error de formato: {e}")

st.sidebar.markdown("---")
st.sidebar.info("NEXUS Agent v1.2 - Powered by Gemini 2.0 & Firecrawl")
