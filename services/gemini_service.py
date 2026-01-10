"""
Gemini AI Service - Updated for google-genai package
Provides AI-powered SEO analysis using Google Gemini Pro
"""

try:
    from google import genai
    NEW_API = True
except ImportError:
    try:
        import google.generativeai as genai
        NEW_API = False
    except ImportError:
        raise ImportError("Please install: pip install google-genai")

import json
from typing import Dict, List
import os

class GeminiSEOAnalyzer:
    """AI-powered SEO analyzer using Gemini Pro"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
        # Try multiple key names for compatibility
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("No API key provided. Set GEMINI_API_KEY or GOOGLE_API_KEY")
        
        print(f"🤖 Initializing Gemini with key: {api_key[:10]}...")
        print(f"📦 Using {'NEW' if NEW_API else 'OLD'} API")
        
        if NEW_API:
            # New google-genai package
            client = genai.Client(api_key=api_key)
            self.model = client.models.generate_content
            self.model_name = 'gemini-2.0-flash-exp'
        else:
            # Old google.generativeai package (deprecated)
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        
        print("✅ Gemini initialized successfully")
    
    def analyze_seo(self, scan_results: Dict) -> Dict:
        """
        Analyze SEO scan results with AI
        Returns enhanced analysis with AI recommendations
        """
        print("🤖 Starting AI analysis...")
        
        try:
            # Build prompt from scan results
            prompt = self._build_analysis_prompt(scan_results)
            
            print("📝 Sending prompt to Gemini...")
            
            # Get AI response
            if NEW_API:
                response = self.model(
                    model=self.model_name,
                    contents=prompt
                )
                response_text = response.text
            else:
                response = self.model.generate_content(prompt)
                response_text = response.text
            
            print("✅ Received response from Gemini")
            
            # Parse AI recommendations
            ai_analysis = self._parse_ai_response(response_text)
            
            print(f"✅ Parsed {len(ai_analysis.get('recommendations', []))} recommendations")
            
            return {
                'success': True,
                'ai_recommendations': ai_analysis.get('recommendations', []),
                'ai_priority_issues': ai_analysis.get('priority_issues', []),
                'ai_summary': ai_analysis.get('summary', ''),
                'ai_score_breakdown': ai_analysis.get('score_breakdown', {}),
                'raw_response': response_text
            }
            
        except Exception as e:
            print(f"❌ AI Analysis error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_analysis_prompt(self, results: Dict) -> str:
        """Build detailed prompt for Gemini"""
        
        meta = results.get('meta_tags', {})
        headings = results.get('headings', {})
        content = results.get('content', {})
        technical = results.get('technical', {})
        images = results.get('images', {})
        mobile = results.get('mobile', {})
        
        prompt = f"""
You are an expert SEO consultant analyzing a website. Provide detailed, actionable recommendations.

**WEBSITE:** {results.get('url', 'Unknown')}

**CURRENT SEO DATA:**

Meta Tags:
- Title: "{meta.get('title', 'Missing')}" ({meta.get('title_length', 0)} chars)
- Description: "{meta.get('description', 'Missing')}" ({meta.get('description_length', 0)} chars)
- Has Canonical: {bool(meta.get('canonical'))}

Content Structure:
- H1 Count: {headings.get('h1_count', 0)}
- Total Headings: {headings.get('total_count', 0)}
- Word Count: {content.get('word_count', 0)}
- Paragraphs: {content.get('paragraph_count', 0)}

Images:
- Total: {images.get('total', 0)}
- With Alt Text: {images.get('with_alt', 0)}
- Missing Alt Text: {images.get('without_alt', 0)}

Technical:
- HTTPS: {technical.get('has_ssl', False)}
- Load Time: {technical.get('load_time', 0)} seconds
- Page Size: {technical.get('page_size', 0)} bytes

Mobile:
- Has Viewport: {mobile.get('has_viewport', False)}
- Is Responsive: {mobile.get('is_responsive', False)}

Current Issues:
{self._format_issues(results.get('issues', []))}

**PROVIDE ANALYSIS IN THIS JSON FORMAT:**

{{
  "summary": "Brief 2-3 sentence overview of the site's SEO health",
  "score_breakdown": {{
    "technical_seo": 85,
    "content_quality": 70,
    "user_experience": 90,
    "mobile_optimization": 95
  }},
  "priority_issues": [
    {{
      "severity": "critical",
      "title": "Issue title",
      "description": "Detailed explanation",
      "how_to_fix": "Step-by-step fix",
      "impact": "What improves when fixed"
    }}
  ],
  "recommendations": [
    {{
      "category": "content",
      "title": "Recommendation title",
      "description": "Detailed recommendation",
      "priority": "high",
      "estimated_impact": "Expected improvement",
      "implementation_difficulty": "easy"
    }}
  ],
  "keyword_suggestions": [
    "suggested keyword 1",
    "suggested keyword 2"
  ],
  "content_suggestions": [
    "Content improvement suggestion 1",
    "Content improvement suggestion 2"
  ]
}}

Provide ONLY the JSON response, no additional text.
"""
        
        return prompt
    
    def _format_issues(self, issues: List[Dict]) -> str:
        """Format issues for prompt"""
        if not issues:
            return "No critical issues detected"
        
        formatted = []
        for issue in issues:
            formatted.append(f"- [{issue.get('type', 'issue').upper()}] {issue.get('title', 'Unknown')}: {issue.get('description', '')}")
        
        return "\n".join(formatted)
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response (handles both JSON and text)"""
        try:
            # Try to extract JSON from response
            clean_text = response_text.strip()
            if clean_text.startswith('```json'):
                clean_text = clean_text[7:]
            if clean_text.startswith('```'):
                clean_text = clean_text[3:]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-3]
            
            clean_text = clean_text.strip()
            
            # Parse JSON
            data = json.loads(clean_text)
            return data
            
        except json.JSONDecodeError:
            print("⚠️ Failed to parse JSON, using fallback format")
            # If JSON parsing fails, return basic structure
            return {
                'summary': response_text[:500] if len(response_text) > 500 else response_text,
                'recommendations': [
                    {
                        'category': 'general',
                        'title': 'AI Analysis',
                        'description': response_text,
                        'priority': 'medium',
                        'estimated_impact': 'See full analysis',
                        'implementation_difficulty': 'medium'
                    }
                ],
                'priority_issues': [],
                'score_breakdown': {}
            }
    
    def generate_content_suggestions(self, url: str, current_content: str, target_keywords: List[str] = None) -> Dict:
        """Generate AI content improvement suggestions"""
        
        prompt = f"""
As an SEO content expert, analyze this content and provide improvement suggestions.

**URL:** {url}
**Current Content Preview:** 
{current_content[:1000]}...

**Target Keywords:** {', '.join(target_keywords) if target_keywords else 'Not specified'}

Provide suggestions for:
1. Content structure improvements
2. Keyword optimization
3. Readability enhancements
4. Additional sections to add
5. Internal linking opportunities

Format as JSON with actionable recommendations.
"""
        
        try:
            if NEW_API:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                response_text = response.text
            else:
                response = self.model.generate_content(prompt)
                response_text = response.text
            
            return {
                'success': True,
                'suggestions': response_text
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


# Helper function for easy use
def analyze_with_ai(scan_results: Dict, api_key: str = None) -> Dict:
    """
    Convenience function to analyze scan results with AI
    Usage: ai_analysis = analyze_with_ai(scan_results, gemini_api_key)
    
    If api_key is None, will try to get from environment variables
    """
    try:
        # Try to get key from multiple sources
        if not api_key:
            import os
            api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ No API key found in parameters or environment")
            return {
                'success': False,
                'error': 'No API key provided. Set GEMINI_API_KEY or GOOGLE_API_KEY'
            }
        
        print(f"🔑 Using API key: {api_key[:10]}...{api_key[-5:]}")
        
        analyzer = GeminiSEOAnalyzer(api_key)
        result = analyzer.analyze_seo(scan_results)
        
        return result
        
    except Exception as e:
        print(f"❌ analyze_with_ai error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return {
            'success': False,
            'error': f'Failed to initialize AI analyzer: {str(e)}'
        }