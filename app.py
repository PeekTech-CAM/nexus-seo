import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="NEXUS SEO Agent Pro", page_icon="⚡", layout="wide")

# --- SEGURIDAD: CONTROL DE ACCESO ---
def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.title("🔐 Acceso NEXUS Pro")
            password_input = st.text_input("Introduce tu Código de Licencia:", type="password")
            if st.button("Activar Licencia"):
                # Contraseña maestra de acceso
                if password_input == "NEXUS2025": 
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Código inválido. Contacta al administrador para obtener una licencia.")
        return False
    return True

# --- CARGA DE LLAVES DESDE SECRETS ---
try:
    KEY_FIRECRAWL = st.secrets["FIRE_KEY"]
    KEY_GOOGLE = st.secrets["GEMINI_KEY"]
except Exception:
    st.error("Configuración incompleta: Asegúrate de añadir FIRE_KEY y GEMINI_KEY en los Secrets de Streamlit.")
    st.stop()

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .report-card { padding: 25px; border-radius: 12px; background-color: #1e2129; border: 1px solid #3d444d; margin-bottom: 20px; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #ff4b4b, #ffeb3b, #4caf50); }
    .stDownloadButton>button { background-color: #28a745 !important; color: white !important; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN: GENERADOR DE PDF ---
def crear_pdf(texto_reporte, url_analizada, score):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(255, 75, 75)
    pdf.cell(0, 15, "NEXUS SEO REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Sitio Analizado: {url_analizada}", ln=True, align='C')
    pdf.cell(0, 10, f"SEO Health Score: {score}/100", ln=True, align='C')
    pdf.ln(10)
    
    # Cuerpo del reporte
    pdf.set_font("Arial", size=11)
    # Limpieza de caracteres no compatibles con Latin-1
    texto_limpio = texto_reporte.replace("**", "").replace("#", "").replace("`", "").replace("•", "-")
    pdf.multi_cell(0, 8, texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
    
    # Pie de página
    pdf.set_y(-20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Este documento es una auditoria generada por IA. Nexus Agent Pro.", align='C')
    
    return pdf.output(dest='S')

# --- FUNCIÓN: LÓGICA DEL AGENTE ---
def ejecutar_auditoria(url):
    try:
        app = Firecrawl(api_key=KEY_FIRECRAWL)
        client = genai.Client(api_key=KEY_GOOGLE)
    except Exception as e:
        return f"Error de conexión: {e}", 0

    with st.status("🕵️‍♂️ NEXUS rastreando y analizando sitio...", expanded=True) as status:
        st.write("👀 Extrayendo contenido web...")
        try:
            scrape = app.scrape(url)
            contenido = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        except Exception as e:
            return f"Error en Firecrawl: {e}", 0

        st.write("🧠 Calculando métricas y estrategia con IA...")
        prompt = f"""
        Eres NEXUS, el auditor SEO más crítico y experto del mundo. Analiza el sitio: {url}
        
        INSTRUCCIONES:
        1. Comienza SIEMPRE con la línea: "SCORE: [Número del 0 al 100]"
        2. Proporciona una explicación breve de la nota.
        3. Reporte detallado: 3 Errores Críticos, 3 Sugerencias de H1, y reescritura de conversión para el primer párrafo.
        
        Contenido: {contenido[:15000]}
        """
        
        modelos = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp"]
        resultado = None
        
        for mod in modelos:
            try:
                st.write(f"🔌 Conectando con motor: {mod}...")
                response = client.models.generate_content(model=mod, contents=prompt)
                resultado = response.text
                if resultado: break
            except:
                continue
        
        if resultado:
            status.update(label="✅ Análisis estratégico finalizado", state="complete")
            # Extraer Score numérico
            try:
                score_val = int(resultado.split("SCORE:")[1].split("\n")[0].strip())
            except:
                score_val = 50 # Valor por defecto si falla la extracción
            return resultado, score_val
        else:
            return "Error: Los motores de IA no están disponibles.", 0

# --- INTERFAZ PRINCIPAL ---
if verificar_password():
    st.title("⚡ NEXUS SEO Agent Pro")
    st.write("Introduce una URL para que la IA realice una auditoría de nivel agencia.")

    # Panel de entrada
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        url_input = st.text_input("URL del cliente:", placeholder="https://ejemplo.com", label_visibility="collapsed")
    with col_btn:
        boton_run = st.button("🚀 INICIAR AUDITORÍA")

    if boton_run and url_input:
        reporte, score = ejecutar_auditoria(url_input)
        
        if "Error" in reporte and len(reporte) < 150:
            st.error(reporte)
        else:
            st.balloons()
            st.markdown("---")
            
            # Visualización de Score
            st.subheader("📊 Diagnóstico de Salud SEO")
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.metric(label="SEO Health Score", value=f"{score}/100")
                st.progress(score / 100)
                if score < 50: st.warning("⚠️ Este sitio necesita mejoras urgentes.")
                elif score < 85: st.info("📈 El sitio está bien, pero hay margen de optimización.")
                else: st.success("✅ ¡Excelente optimización!")

            # Resultados del Reporte
            st.markdown("### 📝 Informe Detallado")
            st.markdown(f'<div class="report-card">{reporte}</div>', unsafe_allow_html=True)
            
            # Descarga de PDF
            try:
                pdf_bytes = crear_pdf(reporte, url_input, score)
                st.download_button(
                    label="📩 Descargar Reporte Completo (PDF)",
                    data=pdf_bytes,
                    file_name=f"Auditoria_NEXUS_{url_input.replace('https://','').replace('.','_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error al generar PDF: {e}")

    # Sidebar
    st.sidebar.title("NEXUS Pro")
    st.sidebar.write("Panel de Control")
    st.sidebar.info("Estado: Licencia Activa ✅")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["autenticado"] = False
        st.rerun()
