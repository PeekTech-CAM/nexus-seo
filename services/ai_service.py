"""
Enhanced AI Service for SEO Analysis
Shows CLEAR value with actionable, personalized recommendations
"""

import google.generativeai as genai
import os
import streamlit as st
from typing import Dict, Optional

class AIAnalysisService:
    """AI-powered SEO consultant using Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini API"""
        self.model = None
        self.model_name = None
        
        try:
            # Get API Key
            api_key = None
            if hasattr(st, 'secrets'):
                api_key = st.secrets.get("GOOGLE_API_KEY")
            if not api_key:
                api_key = os.getenv("GOOGLE_API_KEY")
            
            if not api_key:
                print("❌ GOOGLE_API_KEY not configured")
                return
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            self.model_name = 'gemini-1.5-flash'
            self.model = genai.GenerativeModel(self.model_name)
            print(f"✅ AI Service ready with {self.model_name}")
            
        except Exception as e:
            print(f"❌ AI initialization error: {str(e)}")
            self.model = None
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.model is not None
    
    def analyze_seo_scan(self, scan_data: Dict) -> Optional[str]:
        """Generate AI-powered SEO recommendations with CLEAR value"""
        if not self.model:
            return None
        
        try:
            prompt = self._create_expert_prompt(scan_data)
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.8,
                    'top_p': 0.9,
                    'max_output_tokens': 3000,
                }
            )
            
            return response.text
            
        except Exception as e:
            print(f"❌ AI analysis error: {str(e)}")
            return None
    
    def _create_expert_prompt(self, scan_data: Dict) -> str:
        """Create expert-level prompt showing AI value"""
        
        url = scan_data.get('url', 'Unknown')
        overall = scan_data.get('overall_score', 0)
        technical = scan_data.get('technical_score', 0)
        content = scan_data.get('content_score', 0)
        performance = scan_data.get('performance_score', 0)
        
        title = scan_data.get('title', '')
        meta_desc = scan_data.get('meta_description', '')
        word_count = scan_data.get('word_count', 0)
        h1_count = scan_data.get('h1_count', 0)
        load_time = scan_data.get('load_time_ms', 0)
        has_ssl = scan_data.get('has_ssl', False)
        
        issues = scan_data.get('issues_detail', {})
        critical = issues.get('critical', [])
        high = issues.get('high', [])
        medium = issues.get('medium', [])
        
        prompt = f"""You are an EXPERT SEO consultant analyzing a website. Provide ACTIONABLE, SPECIFIC recommendations that show CLEAR VALUE beyond basic SEO scanning.

🌐 WEBSITE AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**URL:** {url}
**Overall SEO Score:** {overall}/100

📊 DETAILED SCORES:
• Technical SEO: {technical}/100 {'🔴' if technical < 60 else '🟡' if technical < 80 else '🟢'}
• Content Quality: {content}/100 {'🔴' if content < 60 else '🟡' if content < 80 else '🟢'}
• Performance: {performance}/100 {'🔴' if performance < 60 else '🟡' if performance < 80 else '🟢'}

📋 CURRENT STATE:
• Title: "{title[:80]}..." ({len(title)} chars)
• Meta Desc: "{meta_desc[:80]}..." ({len(meta_desc)} chars)
• Content: {word_count} words
• H1 Tags: {h1_count}
• Load Time: {load_time}ms
• HTTPS: {'Yes ✅' if has_ssl else 'No ❌'}

🚨 DETECTED ISSUES:
**Critical ({len(critical)}):**
{self._format_list(critical) if critical else '✅ None'}

**High Priority ({len(high)}):**
{self._format_list(high) if high else '✅ None'}

**Medium Priority ({len(medium)}):**
{self._format_list(medium) if medium else '✅ None'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your task: Provide EXPERT analysis that goes BEYOND basic scanning. Show clear value by:

## 🎯 1. STRATEGIC ASSESSMENT (2-3 sentences)
- What's the BIGGEST opportunity being missed?
- What's the competitive advantage/disadvantage?
- Industry-specific insights

## 🔥 2. TOP 3 PRIORITY FIXES (Ranked by ROI)
For each fix:
- **What to do:** Specific action
- **Why it matters:** Business impact (traffic, conversions, rankings)
- **How to implement:** Step-by-step (30-50 words)
- **Expected impact:** Quantify if possible

Example format:
### 1. 🎯 [Specific Issue]
**Impact:** High - Could increase organic traffic by 20-40%
**Action:** [Detailed implementation steps]
**Timeline:** [Hours/Days needed]

## ⚡ 3. QUICK WINS (Do TODAY)
List 3-5 changes that take <30 minutes each but have immediate impact:
- ✅ [Specific change] → [Expected result]
- ✅ [Specific change] → [Expected result]

## 🚀 4. ADVANCED OPTIMIZATIONS
2-3 advanced strategies that competitors likely aren't doing:
- Advanced schema markup opportunities
- Content gap analysis vs competitors
- User intent optimization strategies

## 💡 5. CONTENT STRATEGY
- What content is missing based on the current page?
- What keywords should be targeted?
- What internal linking opportunities exist?

## 📈 6. COMPETITIVE POSITIONING
- Where does this page stand vs typical competitors?
- What's the path to ranking in top 3?

## ⚠️ 7. RISK ASSESSMENT
- What could hurt rankings in the next algorithm update?
- Any penalties or manual action risks?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT GUIDELINES:
✅ BE SPECIFIC - No generic advice like "improve content"
✅ QUANTIFY IMPACT - Use numbers when possible
✅ PROVIDE CONTEXT - Explain WHY, not just WHAT
✅ PRIORITIZE BY ROI - Focus on high-impact, low-effort first
✅ BE ACTIONABLE - Include exact steps
✅ SHOW EXPERTISE - Go beyond what basic tools say
✅ BE HONEST - Don't oversell if the site is already good

Use emojis for readability. Write in a confident, expert tone."""

        return prompt
    
    def _format_list(self, items: list) -> str:
        """Format list items"""
        if not items:
            return "None"
        return "\n".join([f"  • {item}" for item in items[:5]])
    
    def generate_competitive_insights(self, scan_data: Dict) -> Optional[str]:
        """Generate competitive positioning insights"""
        if not self.model:
            return None
        
        try:
            url = scan_data.get('url', '')
            score = scan_data.get('overall_score', 0)
            
            prompt = f"""As an SEO expert, analyze this website's competitive position:

URL: {url}
Current Score: {score}/100

Provide:
1. **Industry Benchmark:** Where does {score}/100 stand in their industry?
2. **Competitive Gap:** What are competitors likely doing better?
3. **Differentiation Strategy:** How can they stand out?

Keep it under 150 words, be specific and actionable."""

            response = self.model.generate_content(prompt)
            return response.text
        except:
            return None
    
    def generate_content_suggestions(self, scan_data: Dict) -> Optional[str]:
        """Generate content improvement suggestions"""
        if not self.model:
            return None
        
        try:
            title = scan_data.get('title', '')
            word_count = scan_data.get('word_count', 0)
            
            prompt = f"""As a content strategist, analyze this page:

Title: {title}
Word Count: {word_count}

Suggest:
1. **Missing Topics:** 3 topics that should be covered
2. **Content Gaps:** What questions aren't being answered?
3. **Engagement Hooks:** 2 ways to improve user engagement

Keep it actionable and specific (under 200 words)."""

            response = self.model.generate_content(prompt)
            return response.text
        except:
            return None


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
    """Main function: Get comprehensive AI analysis"""
    service = get_ai_service()
    if not service.is_available():
        return None
    return service.analyze_seo_scan(scan_data)

def is_ai_available() -> bool:
    """Check if AI is configured"""
    service = get_ai_service()
    return service.is_available()

def get_competitive_insights(scan_data: Dict) -> Optional[str]:
    """Get competitive positioning insights"""
    service = get_ai_service()
    return service.generate_competitive_insights(scan_data)

def get_content_suggestions(scan_data: Dict) -> Optional[str]:
    """Get content improvement suggestions"""
    service = get_ai_service()
    return service.generate_content_suggestions(scan_data)
