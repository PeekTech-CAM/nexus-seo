"""
AI Service for SEO Analysis
Clean, working version with gemini-1.5-flash
"""

import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, Optional

class AIAnalysisService:
    """Handle AI-powered SEO analysis using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini API"""
        self.model = None
        self.model_name = None
        
        try:
            # Get API Key
            api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                print("❌ Error: GOOGLE_API_KEY not found")
                return
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Use gemini-1.5-flash (latest working model)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.model_name = 'gemini-1.5-flash'
            print(f"✅ AI Service connected using model '{self.model_name}'")
            
        except Exception as e:
            print(f"❌ AI initialization error: {str(e)}")
            self.model = None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        """Generate AI-powered SEO recommendations"""
        if not self.model:
            return None
        
        try:
            prompt = self._create_analysis_prompt(scan_data)
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"AI analysis error: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, scan_data: Dict) -> str:
        """Create a detailed prompt for AI analysis"""
        
        url = scan_data.get('url', 'Unknown')
        overall_score = scan_data.get('overall_score', 0)
        technical_score = scan_data.get('technical_score', 0)
        content_score = scan_data.get('content_score', 0)
        
        issues = scan_data.get('issues_detail', {})
        critical_issues = issues.get('critical', [])
        high_issues = issues.get('high', [])
        
        prompt = f"""
You are an expert SEO consultant. Analyze this website audit and provide actionable recommendations.

WEBSITE: {url}
OVERALL SCORE: {overall_score}/100
TECHNICAL: {technical_score}/100
CONTENT: {content_score}/100

CRITICAL ISSUES:
{self._format_issues(critical_issues)}

HIGH PRIORITY:
{self._format_issues(high_issues)}

Provide:
1. Executive Summary (2-3 sentences)
2. Top 3 Priority Actions
3. Quick Wins (easy improvements)

Keep it concise and actionable. Use emojis.
"""
        return prompt
    
    def _format_issues(self, issues: list) -> str:
        """Format issues list"""
        if not issues:
            return "None detected"
        return "\n".join([f"- {issue}" for issue in issues[:5]])


# Global instance
_ai_service = None

def get_ai_service():
    """Get or create AI service singleton"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIAnalysisService()
    return _ai_service

def analyze_seo_with_ai(scan_data: Dict) -> Optional[str]:
    """Quick function to analyze SEO scan"""
    service = get_ai_service()
    return service.analyze_seo_scan(scan_data)