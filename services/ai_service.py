"""
AI Service for SEO Analysis
Clean, working version with gemini-1.5-flash
"""

import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, Optional
import json

class AIAnalysisService:
    """Handle AI-powered SEO analysis using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini API"""
        self.model = None
        self.model_name = None
        
        try:
            # Get API Key from Streamlit secrets or environment
            api_key = None
            if hasattr(st, 'secrets'):
                api_key = st.secrets.get("GOOGLE_API_KEY")
            if not api_key:
                api_key = os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                print("❌ Error: GOOGLE_API_KEY not found in secrets or environment")
                return
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Use gemini-1.5-flash (latest stable model)
            self.model_name = 'gemini-1.5-flash'
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ AI Service initialized with model '{self.model_name}'")
            
        except Exception as e:
            print(f"❌ AI initialization error: {str(e)}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.model is not None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        """Generate AI-powered SEO recommendations"""
        if not self.model:
            return None
        
        try:
            prompt = self._create_analysis_prompt(scan_data)
            
            # Generate content with safety settings
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.8,
                    'top_k': 40,
                    'max_output_tokens': 2048,
                }
            )
            
            return response.text
            
        except Exception as e:
            print(f"❌ AI analysis error: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, scan_data: Dict) -> str:
        """Create a detailed prompt for AI analysis"""
        
        url = scan_data.get('url', 'Unknown')
        overall_score = scan_data.get('overall_score', 0)
        technical_score = scan_data.get('technical_score', 0)
        content_score = scan_data.get('content_score', 0)
        performance_score = scan_data.get('performance_score', 0)
        
        # Extract metadata
        title = scan_data.get('title', 'N/A')
        meta_desc = scan_data.get('meta_description', 'N/A')
        word_count = scan_data.get('word_count', 0)
        load_time = scan_data.get('load_time_ms', 0)
        has_ssl = scan_data.get('has_ssl', False)
        
        # Extract issues
        issues = scan_data.get('issues_detail', {})
        critical_issues = issues.get('critical', [])
        high_issues = issues.get('high', [])
        medium_issues = issues.get('medium', [])
        
        prompt = f"""You are an expert SEO consultant analyzing a website audit. Provide clear, actionable recommendations.

🌐 WEBSITE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
URL: {url}
Overall Score: {overall_score}/100

📊 SCORE BREAKDOWN:
• Technical SEO: {technical_score}/100
• Content Quality: {content_score}/100
• Performance: {performance_score}/100

📝 CURRENT STATUS:
• Title: {title[:100]}
• Meta Description: {meta_desc[:150]}
• Word Count: {word_count}
• Load Time: {load_time}ms
• HTTPS: {'✅' if has_ssl else '❌'}

🚨 ISSUES DETECTED:

CRITICAL ({len(critical_issues)}):
{self._format_issues(critical_issues) if critical_issues else '✅ None'}

HIGH PRIORITY ({len(high_issues)}):
{self._format_issues(high_issues) if high_issues else '✅ None'}

MEDIUM PRIORITY ({len(medium_issues)}):
{self._format_issues(medium_issues) if medium_issues else '✅ None'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please provide:

## 📋 Executive Summary
Brief 2-3 sentence overview of the website's SEO health.

## 🎯 Top 3 Priority Actions
1. [Most critical fix]
2. [Second priority]
3. [Third priority]

## ⚡ Quick Wins
List 3-5 easy improvements that can be done immediately.

## 💡 Long-term Recommendations
2-3 strategic improvements for sustained growth.

Keep it concise, actionable, and easy to understand. Use emojis for better readability."""

        return prompt
    
    def _format_issues(self, issues: list) -> str:
        """Format issues list"""
        if not issues:
            return "None detected ✅"
        
        formatted = []
        for i, issue in enumerate(issues[:5], 1):
            formatted.append(f"  {i}. {issue}")
        
        if len(issues) > 5:
            formatted.append(f"  ... and {len(issues) - 5} more")
        
        return "\n".join(formatted)
    
    def generate_quick_tip(self, score: int) -> str:
        """Generate a quick tip based on score"""
        if not self.model:
            return "Improve your SEO by fixing the critical issues first."
        
        try:
            prompt = f"""Give one actionable SEO tip for a website with a score of {score}/100. 
Keep it under 20 words. Start with an emoji."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Focus on the highest priority issues to improve your score."


# ══════════════════════════════════════════════════════════════════
# Global instance and helper functions
# ══════════════════════════════════════════════════════════════════

_ai_service = None

def get_ai_service() -> AIAnalysisService:
    """Get or create AI service singleton"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIAnalysisService()
    return _ai_service

def analyze_seo_with_ai(scan_data: Dict) -> Optional[str]:
    """Quick function to analyze SEO scan with AI"""
    service = get_ai_service()
    if not service.is_available():
        return None
    return service.analyze_seo_scan(scan_data)

def is_ai_available() -> bool:
    """Check if AI service is available"""
    service = get_ai_service()
    return service.is_available()

def get_quick_tip(score: int) -> str:
    """Get a quick SEO tip based on score"""
    service = get_ai_service()
    return service.generate_quick_tip(score)