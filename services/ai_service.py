import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, List, Optional

class AIAnalysisService:
    """
    Servicio de análisis SEO con IA utilizando Google Gemini.
    Incluye sistema de 'fallback' automático para manejar errores de modelos.
    """
    
    def __init__(self):
        """Inicializa la API de Gemini con selección robusta de modelos"""
        self.model = None
        try:
            # 1. Obtener API Key de secrets o variables de entorno
            api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                print("❌ Error: No se encontró GOOGLE_API_KEY")
                return
            
            genai.configure(api_key=api_key)
            
            # 2. Lista de modelos a probar en orden de prioridad
            # Flash es más rápido y barato. Pro es más potente. El último es legacy.
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for model_name in models_to_try:
                try:
                    # Prueba de conexión (sin generar coste, solo instanciación)
                    test_model = genai.GenerativeModel(model_name)
                    self.model = test_model
                    self.model_name = model_name
                    print(f"✅ ÉXITO: AI Service conectado usando modelo '{model_name}'")
                    break
                except Exception as e:
                    print(f"⚠️ Aviso: El modelo '{model_name}' falló o no está disponible: {e}")
                    continue
            
            if not self.model:
                print("❌ ERROR CRÍTICO: Ningún modelo de Gemini pudo inicializarse.")
                
        except Exception as e:
            print(f"❌ Error fatal en inicialización de AI: {str(e)}")
            self.model = None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        """Genera recomendaciones SEO basadas en los datos del escaneo"""
        if not self.model:
            return "⚠️ El servicio de IA no está disponible. Revisa la configuración de la API Key."
        
        try:
            prompt = self._create_analysis_prompt(scan_data)
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error generando análisis SEO: {error_msg}")
            if "404" in error_msg:
                return "Error 404 de Google API. Por favor actualiza la librería: pip install -U google-generativeai"
            return "No se pudo generar el análisis debido a un error del servicio de IA."

    def generate_content_ideas(self, keyword: str, industry: str) -> Optional[str]:
        """Genera ideas de contenido para el blog"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            Actúa como un estratega de contenido SEO experto.
            Genera 5 ideas de artículos de blog atractivos para:
            
            Palabra clave: {keyword}
            Industria: {industry}
            
            Para cada idea incluye:
            - Título (H2)
            - Breve descripción
            - Intención de búsqueda (Informativa/Transaccional)
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error generando ideas de contenido: {str(e)}")
            return None

    def analyze_competitor(self, your_url: str, competitor_url: str, your_scan: Dict, competitor_scan: Dict) -> Optional[str]:
        """Compara tu sitio con el de un competidor"""
        if not self.model:
            return None
            
        try:
            prompt = f"""
            Compara estos dos sitios web desde una perspectiva SEO técnica y de contenido:
            
            MI SITIO ({your_url}):
            - Puntuación Global: {your_scan.get('overall_score', 0)}
            
            COMPETIDOR ({competitor_url}):
            - Puntuación Global: {competitor_scan.get('overall_score', 0)}
            
            Dame 3 acciones concretas para superar al competidor.
            """
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error en análisis de competencia: {str(e)}")
            return None

    def _create_analysis_prompt(self, scan_data: Dict) -> str:
        """Crea el prompt detallado para el análisis principal"""
        url = scan_data.get('url', 'URL Desconocida')
        score = scan_data.get('overall_score', 0)
        
        # Extracción segura de problemas
        issues_data = scan_data.get('issues_detail', {})
        critical = issues_data.get('critical', []) if isinstance(issues_data, dict) else []
        
        # Formatear lista de problemas para el prompt
        critical_text = "\n".join([f"- {i}" for i in critical[:5]]) if critical else "Ninguno detectado"
        
        return f"""
        Eres un consultor SEO Senior. Analiza los siguientes datos de auditoría web:
        
        Sitio Web: {url}
        Puntuación SEO: {score}/100
        
        Problemas Críticos Detectados:
        {critical_text}
        
        Por favor proporciona un informe ejecutivo que incluya:
        1. 🚦 Resumen del estado de salud del sitio (2 líneas)
        2. 🔧 Top 3 Prioridades Técnicas a arreglar hoy mismo
        3. 🚀 Estrategia rápida de contenido ("Quick Wins")
        
        Usa formato Markdown profesional. Sé conciso y directo.
        """

# --- Singleton Pattern ---
_ai_service_instance = None

def get_ai_service() -> AIAnalysisService:
    """Devuelve una instancia única del servicio para no reconectar constantemente"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIAnalysisService()
    return _ai_service_instance

# --- Funciones Puente (Bridge Functions) para compatibilidad ---
# Estas funciones permiten que el resto de tu app llame al servicio sin cambiar código

def analyze_seo_with_ai(scan_data: Dict) -> Optional[str]:
    return get_ai_service().analyze_seo_scan(scan_data)

def generate_content_ideas_ai(keyword: str, industry: str) -> Optional[str]:
    return get_ai_service().generate_content_ideas(keyword, industry)

def compare_with_competitor_ai(your_url: str, competitor_url: str, your_scan: Dict, competitor_scan: Dict) -> Optional[str]:
    return get_ai_service().analyze_competitor(your_url, competitor_url, your_scan, competitor_scan)