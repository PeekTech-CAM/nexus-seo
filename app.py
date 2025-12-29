import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS SEO Agent", page_icon="⚡", layout="wide")

# --- SEGURIDAD: CONTROL DE ACCESO ---
def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.container()
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Acceso NEXUS Pro")
            password_input = st.text_input("Introduce tu Código de Licencia:", type="password")
            if st.button("Activar Licencia"):
                # Cambia 'NEXUS2025' por la contraseña que tú quieras
                if password_input == "NEXUS2025": 
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Código inválido. Contacta al administrador.")
        return False
    return True

# --- CARGA DE LLAVES DESDE SECRETS ---
try:
    KEY_FIRECRAWL = st.secrets["FIRE_KEY"]
    KEY_GOOGLE = st.secrets["GEMINI_KEY"]
except Exception:
    st.error("Error: No se encontraron las API Keys en los Secrets de Streamlit.")
    st.stop()

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .report-card { padding: 25px; border-radius: 12px; background-color: #1e2129; border: 1px solid #3d444d; line-height: 1.6; }
    .stDownloadButton>button { background-color: #28a745 !important; color: white !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN: GENERADOR DE PDF ---
def crear_pdf(texto_reporte, url_analizada):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "NEXUS: Reporte de Inteligencia SEO", ln=True, align='C')
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 10, f"Analisis para: {url_analizada}", ln=True, align='C')
    pdf.ln(10)
    
    # Limpieza básica para evitar fallos de codificación
    texto_limpio = texto_reporte.replace("**", "").replace("#", "").replace("`", "")
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
    
    pdf.set_y(-20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS AI - Reporte Confidencial", align='C')
    return pdf.output(dest='S')

# --- FUNCIÓN: LÓGICA DEL AGENTE ---
def ejecutar_auditoria(url):
    try:
        app = Firecrawl(api_key=KEY_FIRECRAWL)
        client = genai.Client(api_key=KEY_GOOGLE)
    except Exception as e:
        return f"Error de conexión: {e}"

    with st.status("🕵️‍♂️ NEXUS rastreando sitio web...", expanded=True) as status:
        st.write("👀 Extrayendo datos...")
        try:
            scrape = app.scrape(url)
            contenido = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        except Exception as e:
            return f"Error en Firecrawl: {e}"

        st.write("🧠 Procesando con Inteligencia Artificial...")
        prompt = f"Actua como experto SEO. Analiza este contenido y genera un reporte con: 1. Errores criticos, 2. Sugerencias de H1, 3. Mejora de copy del primer parrafo y 4. Plan de accion. Sitio: {url}\n\nContenido: {contenido[:12000]}"
        
        # Sistema de auto-recuperación de modelos
        modelos = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
        resultado = None
        
        for mod in modelos:
            try:
                st.write(f"🔌 Intentando con motor: {mod}...")
                response = client.models.generate_content(model=mod, contents=prompt)
                resultado = response.text
                if resultado: break
            except:
                continue
        
        if resultado:
            status.update(label="✅ Auditoría Completa", state="complete")
            return resultado
        else:
            return "Error: Los motores de IA no están disponibles ahora mismo."

# --- INTERFAZ PRINCIPAL ---
if verificar_password():
    st.title("⚡ NEXUS SEO Agent Pro")
    st.write("Bienvenido al panel de control. Introduce una URL para iniciar la auditoría.")

    url_input = st.text_input("URL del cliente:", placeholder="https://cliente.com")
    
    if st.button("🚀 INICIAR ANÁLISIS"):
        if not url_input:
            st.warning("Introduce una URL primero.")
        else:
            reporte = ejecutar_auditoria(url_input)
            
            if "Error" in reporte and len(reporte) < 150:
                st.error(reporte)
            else:
                st.balloons()
                st.markdown("---")
                st.subheader("📊 Resultados de la Auditoría")
                st.markdown(f'<div class="report-card">{reporte}</div>', unsafe_allow_html=True)
                
                # Botón de Descarga
                try:
                    pdf_bytes = crear_pdf(reporte, url_input)
                    st.download_button(
                        label="📩 Descargar Reporte PDF",
                        data=pdf_bytes,
                        file_name=f"Auditoria_NEXUS_{url_input.replace('https://','').replace('.','_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.info("Reporte listo. El botón de PDF aparecerá en la próxima actualización.")

    # Sidebar con info
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    st.sidebar.title("NEXUS Pro")
    st.sidebar.write("Estado: Licencia Activa ✅")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["autenticado"] = False
        st.rerun()
