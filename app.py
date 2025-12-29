import streamlit as st
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="NEXUS SEO Agent Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. SEGURIDAD: CONTROL DE ACCESO ---
def verificar_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.title("🔐 Acceso NEXUS Pro")
            password_input = st.text_input("Introduce tu Código de Licencia:", type="password")
            if st.button("Activar Licencia"):
                # La contraseña maestra configurada
                if password_input == "NEXUS2025":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("Código inválido. Contacta al administrador.")
        return False
    return True

# --- 3. CARGA DE SECRETOS ---
try:
    KEY_FIRECRAWL = st.secrets["FIRE_KEY"]
    KEY_GOOGLE = st.secrets["GEMINI_KEY"]
except Exception:
    st.error("Error: Configura FIRE_KEY y GEMINI_KEY en los Secrets de Streamlit.")
    st.stop()

# --- 4. FUNCIÓN: GENERADOR DE PDF PROFESIONAL ---
def crear_pdf(texto_reporte, url_analizada, score):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado con Estilo
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(255, 75, 75) # Color Rojo Nexus
    pdf.cell(0, 15, "NEXUS SEO REPORT", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Analisis para: {url_analizada}", ln=True, align='C')
    pdf.cell(0, 10, f"SEO Health Score: {score}/100", ln=True, align='C')
    pdf.ln(10)
    
    # Cuerpo del reporte
    pdf.set_font("Arial", size=11)
    # Limpieza de caracteres para compatibilidad Latin-1
    texto_limpio = texto_reporte.replace("**", "").replace("#", "").replace("`", "").replace("•", "-")
    
    # Usamos multi_cell para que el texto fluya correctamente
    pdf.multi_cell(0, 8, texto_limpio.encode('latin-1', 'replace').decode('latin-1'))
    
    # Pie de pagina
    pdf.set_y(-20)
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Generado por NEXUS AI Pro - Reporte de Auditoria Estrategica", align='C')
    
    # RETORNO DE BYTES (Soluciona el error de bytearray)
    return bytes(pdf.output(dest='S'))

# --- 5. LÓGICA DEL AGENTE ---
def ejecutar_auditoria(url):
    try:
        app = Firecrawl(api_key=KEY_FIRECRAWL)
        client = genai.Client(api_key=KEY_GOOGLE)
    except Exception as e:
        return f"Error de conexion: {e}", 0

    with st.status("🕵️‍♂️ NEXUS analizando sitio...", expanded=True) as status:
        st.write("👀 Extrayendo contenido web...")
        try:
            scrape = app.scrape(url)
            contenido = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        except Exception as e:
            return f"Error en Firecrawl: {e}", 0

        st.write("🧠 Procesando estrategia con IA...")
        prompt = f"""
        Actua como NEXUS, experto en SEO. Analiza el sitio: {url}
        INSTRUCCIONES:
        1. Comienza con: "SCORE: [Numero del 0 al 100]"
        2. Proporciona: 3 Errores Criticos, 3 Sugerencias de H1 y Mejora de Copywriting.
        Contenido: {contenido[:15000]}
        """
        
        # Probar modelos disponibles
        modelos = ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"]
        resultado = None
        
        for mod in modelos:
            try:
                st.write(f"🔌 Conectando con: {mod}...")
                response = client.models.generate_content(model=mod, contents=prompt)
                resultado = response.text
                if resultado: break
            except: continue
        
        if resultado:
            status.update(label="✅ Analisis Completo", state="complete")
            try:
                score_val = int(resultado.split("SCORE:")[1].split("\n")[0].replace("[","").replace("]","").strip())
            except: score_val = 65
            return resultado, score_val
        else:
            return "Error: IA no disponible.", 0

# --- 6. INTERFAZ DE USUARIO ---
if verificar_password():
    st.sidebar.title("⚡ NEXUS Pro")
    st.sidebar.success("Licencia Activa")
    if st.sidebar.button("Cerrar Sesion"):
        st.session_state["autenticado"] = False
        st.rerun()

    st.title("⚡ NEXUS SEO Agent Pro")
    st.markdown("### Auditoria de nivel agencia impulsada por IA")

    url_input = st.text_input("Introduce la URL del sitio web:", placeholder="https://ejemplo.com")

    if st.button("🚀 INICIAR AUDITORIA") and url_input:
        reporte, score = ejecutar_auditoria(url_input)
        
        if "Error" in reporte and len(reporte) < 150:
            st.error(reporte)
        else:
            st.balloons()
            st.divider()
            
            # Layout de Resultados
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("SEO Health Score", f"{score}/100")
                st.progress(score / 100)
                
            with c2:
                st.markdown("#### Diagnostico Visual")
                if score < 50: st.error("Mejoras urgentes necesarias.")
                elif score < 85: st.warning("Margen de optimizacion detectado.")
                else: st.success("Sitio bien optimizado.")

            st.markdown("### 📝 Informe Detallado")
            st.info(reporte)

            # Generacion y Descarga de PDF
            try:
                pdf_bytes = crear_pdf(reporte, url_input, score)
                st.download_button(
                    label="📩 Descargar Auditoria en PDF",
                    data=pdf_bytes,
                    file_name=f"Auditoria_NEXUS_{url_input.replace('https://','').replace('.','_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Error al generar archivo: {e}")
