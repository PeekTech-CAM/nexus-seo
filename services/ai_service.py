import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, List, Optional

class AIAnalysisService:
    """Handle AI-powered SEO analysis using Google Gemini with Auto-Fallback"""
    
    def __init__(self):
        """Initialize Gemini API with robust model selection"""
        self.model = None
        try:
            # 1. Obtener API Key
            api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                print("❌ Error: No se encontró GOOGLE_API_KEY")
                return
            
            genai.configure(api_key=api_key)
            
            # 2. Intentar cargar modelos en orden de preferencia (Barato/Rápido -> Potente -> Viejo)
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
            
            for model_name in models_to_try:
                try:
                    # Prueba simple para ver si el modelo responde
                    print(f"🔄 Intentando conectar con modelo: {model_name}...")
                    test_model = genai.GenerativeModel(model_name)
                    # No generamos contenido aún, solo instanciamos
                    self.model = test_model
                    self.model_name = model_name
                    print(f"✅ ÉXITO: Usando modelo {model_name}")
                    break
                except Exception as e:
                    print(f"⚠️ Falló modelo {model_name}: {e}")
                    continue
            
            if not self.model:
                print("❌ ERROR CRÍTICO: Ningún modelo de Gemini funcionó.")
                
        except Exception as e:
            print(f"❌ Error de inicialización general: {str(e)}")
            self.model = None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        if not self.model:
            return "Error: AI Service not initialized. Check terminal logs."
        
        try:
            prompt = self._create_analysis_prompt(scan_data)
            # Añadimos un catch específico para la generación
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error generando análisis: {error_msg}")
            
            # Si el error es 404/Not Found, sugerir actualizar librería
            if "404" in error_msg or "not found" in error_msg.lower():
                return ("Error de API de Google (404). Por favor, actualiza la librería ejecutando: "
                        "pip install -U google-generativeai")
            
            return f"Error durante el análisis de IA: {error_msg}"

    def _create_analysis_prompt(self, scan_data: Dict) -> str:
        # (Mantén tu lógica de prompt original aquí, era buena)
        url = scan_data.get('url', 'Unknown')
        overall_score = scan_data.get('overall_score', 0)
        critical_issues = scan_data.get('issues_detail', {}).get('critical', [])
        
        return f"""
        Act as an SEO Expert. Analyze this website scan:
        URL: {url}
        Score: {overall_score}/100
        Critical Issues: {critical_issues}
        
        Provide:
        1. 3 Quick Wins
        2. Main Technical Fixes
        3. Content Strategy
        
        Keep it professional and concise.
        """

    # ... (Resto de tus métodos auxiliares) ...

# Singleton
_ai_service_instance = None

def get_ai_service():
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIAnalysisService()
    return _ai_service_instance

# Funciones puente
def analyze_seo_with_ai(scan_data):
    return get_ai_service().analyze_seo_scan(scan_data)