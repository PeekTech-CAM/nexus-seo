"""
AI Service for SEO Analysis
Fixed version with proper Gemini API handling
"""

import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, List, Optional

class AIAnalysisService:
    """Handle AI-powered SEO analysis using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini API"""
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("Google API key not found")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"AI Service initialization error: {str(e)}")
            self.model = None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        """
        Generate AI-powered SEO recommendations
        
        Args:
            scan_data: Dictionary containing scan results
            
        Returns:
            String with AI recommendations or None if failed
        """
        if not self.model:
            return None
        
        try:
            # Prepare prompt
            prompt = self._create_analysis_prompt(scan_data)
            
            # Generate response
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
        performance_score = scan_data.get('performance_score', 0)
        
        issues = scan_data.get('issues_detail', {})
        critical_issues = issues.get('critical', [])
        high_issues = issues.get('high', [])
        medium_issues = issues.get('medium', [])
        
        prompt = f"""
You are an expert SEO consultant analyzing a website audit. Provide actionable recommendations.

WEBSITE: {url}

SCORES:
- Overall SEO Score: {overall_score}/100
- Technical SEO: {technical_score}/100
- Content Quality: {content_score}/100
- Performance: {performance_score}/100

CRITICAL ISSUES:
{self._format_issues(critical_issues)}

HIGH PRIORITY ISSUES:
{self._format_issues(high_issues)}

MEDIUM PRIORITY ISSUES:
{self._format_issues(medium_issues)}

Please provide:
1. **Executive Summary** (2-3 sentences about overall site health)
2. **Top 3 Priority Actions** (what to fix first and why)
3. **Quick Wins** (easy improvements with high impact)
4. **Long-term Strategy** (ongoing optimization recommendations)

Keep it concise, actionable, and client-friendly. Use emojis for visual appeal.
"""
        return prompt
    
    def _format_issues(self, issues: List[str]) -> str:
        """Format issues list for prompt"""
        if not issues:
            return "None detected"
        
        return "\n".join([f"- {issue}" for issue in issues[:5]])  # Limit to top 5
    
    def generate_content_ideas(self, keyword: str, industry: str) -> Optional[str]:
        """
        Generate content ideas based on keyword and industry
        
        Args:
            keyword: Target keyword
            industry: Business industry
            
        Returns:
            String with content ideas or None if failed
        """
        if not self.model:
            return None
        
        try:
            prompt = f"""
As an SEO content strategist, generate 5 compelling blog post ideas for:

Keyword: {keyword}
Industry: {industry}

For each idea, provide:
- Catchy title
- Brief description (1-2 sentences)
- Target audience
- SEO potential (1-5 stars)

Make them engaging and SEO-optimized.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Content generation error: {str(e)}")
            return None
    
    def analyze_competitor(self, your_url: str, competitor_url: str, your_scan: Dict, competitor_scan: Dict) -> Optional[str]:
        """
        Compare your site with competitor
        
        Args:
            your_url: Your website URL
            competitor_url: Competitor's URL
            your_scan: Your scan results
            competitor_scan: Competitor's scan results
            
        Returns:
            Comparison analysis or None if failed
        """
        if not self.model:
            return None
        
        try:
            prompt = f"""
Compare these two websites from an SEO perspective:

YOUR SITE: {your_url}
- Overall Score: {your_scan.get('overall_score', 0)}/100
- Technical: {your_scan.get('technical_score', 0)}/100
- Content: {your_scan.get('content_score', 0)}/100
- Performance: {your_scan.get('performance_score', 0)}/100

COMPETITOR: {competitor_url}
- Overall Score: {competitor_scan.get('overall_score', 0)}/100
- Technical: {competitor_scan.get('technical_score', 0)}/100
- Content: {competitor_scan.get('content_score', 0)}/100
- Performance: {competitor_scan.get('performance_score', 0)}/100

Provide:
1. **Strengths vs Weaknesses** (what you do better/worse)
2. **Gap Analysis** (what they have that you don't)
3. **Actionable Steps** (how to outrank them)

Be specific and strategic.
"""
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Competitor analysis error: {str(e)}")
            return None


# Singleton instance
_ai_service_instance = None

def get_ai_service() -> AIAnalysisService:
    """Get or create AI service singleton"""
    global _ai_service_instance
    
    if _ai_service_instance is None:
        _ai_service_instance = AIAnalysisService()
    
    return _ai_service_instance


# Convenience functions
def analyze_seo_with_ai(scan_data: Dict) -> Optional[str]:
    """Quick function to analyze SEO scan"""
    service = get_ai_service()
    return service.analyze_seo_scan(scan_data)

def generate_content_ideas_ai(keyword: str, industry: str) -> Optional[str]:
    """Quick function to generate content ideas"""
    service = get_ai_service()
    return service.generate_content_ideas(keyword, industry)

def compare_with_competitor_ai(your_url: str, competitor_url: str, your_scan: Dict, competitor_scan: Dict) -> Optional[str]:
    """Quick function to compare with competitor"""
    service = get_ai_service()
    return service.analyze_competitor(your_url, competitor_url, your_scan, competitor_scan)