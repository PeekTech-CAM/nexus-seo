import streamlit as st
from firecrawl import Firecrawl
from google import genai

# ==========================================
# 🛑 ZONA DE LLAVES (MODIFICA SOLO ESTO) 🛑
# ==========================================

# 1. Tu llave de Firecrawl (Debe empezar por 'fc-')
# Ejemplo: "fc-123456789..."
KEY_FIRECRAWL = "fc-efe0d7105f984708b6eb39615d5570eb" 

# 2. Tu llave de Google (Debe empezar por 'AIza')
# Ejemplo: "AIzaSyD..."
KEY_GOOGLE = "AIzaSyD5Wl90R6cYtD2Kvb8KM79HGJDCrOp7G-0"

# ==========================================

st.set_page_config(page_title="NEXUS Agent", page_icon="⚡", layout="wide")

st.title("⚡ NEXUS: Agente SEO Autónomo")
st.markdown("### Tu competencia usa ChatSEO. Tú usas Agentes Autónomos.")

def analizar_web(url):
    # Usamos las llaves que escribiste arriba
    try:
        app = Firecrawl(api_key=KEY_FIRECRAWL)
        client = genai.Client(api_key=KEY_GOOGLE)
    except Exception as e:
        return f"Error de configuración: {e}"

    with st.status("🕵️‍♂️ Agente Nexus trabajando...", expanded=True) as status:
        st.write("👀 Escaneando sitio web...")
        try:
            # Intentamos conectar
            respuesta = app.scrape(url)
            
            # Buscamos el texto markdown
            if hasattr(respuesta, 'markdown'): contenido = respuesta.markdown
            elif isinstance(respuesta, dict) and 'markdown' in respuesta: contenido = respuesta['markdown']
            elif isinstance(respuesta, dict) and 'data' in respuesta: contenido = respuesta['data']['markdown']
            else: contenido = str(respuesta)
            
        except Exception as e:
            status.update(label="❌ Error de Firecrawl", state="error")
            return f"Error leyendo la web: {e}. (Verifica que tu API Key empiece por 'fc-')"

        st.write("🧠 Analizando estrategia con Gemini...")
        
        prompt = f"""
        Actúa como NEXUS, experto en SEO. Analiza esto:
        {contenido[:15000]}
        
        Genera un reporte con:
        1. 3 Errores Críticos.
        2. 3 Títulos H1 Nuevos.
        3. Reescribe el primer párrafo.
        """
        
        # Lista de modelos a probar (Auto-reparación)
        modelos = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-1.5-pro", "gemini-2.0-flash-exp"]

        for modelo in modelos:
            try:
                st.write(f"🔌 Probando motor: {modelo}...")
                response = client.models.generate_content(model=modelo, contents=prompt)
                status.update(label="✅ ¡Éxito!", state="complete")
                return response.text
            except:
                continue # Si falla, prueba el siguiente
        
        status.update(label="❌ Error de Google", state="error")
        return "Error: Ningún modelo de IA respondió. Verifica tu API Key de Google (AIza...)."

# Interfaz
url = st.text_input("URL a analizar:", "https://apple.com")

if st.button("🚀 AUDITAR AHORA", type="primary"):
    if "PEGAR_AQUI" in KEY_FIRECRAWL or "PEGAR_AQUI" in KEY_GOOGLE:
        st.error("⚠️ ¡Oye! No has puesto tus llaves reales en el código (líneas 11 y 15).")
    else:
        resultado = analizar_web(url)
        if "Error" in resultado and len(resultado) < 200:
            st.error(resultado)
        else:
            st.balloons()
            st.markdown("---")
            st.markdown(resultado)