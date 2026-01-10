"""
NEXUS SEO INTELLIGENCE - AI Service Layer
Google Gemini PRO integration for advanced SEO analysis
"""

import os
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import logging
from supabase import Client

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Model configuration
MODEL_NAME = "gemini-1.5-pro"
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

# Safety settings (production-appropriate)
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Credit costs per operation (adjust based on token usage patterns)
CREDIT_COSTS = {
    'seo_audit': 100,           # Full comprehensive audit
    'keyword_research': 50,     # Keyword expansion and clustering
    'content_gap': 75,          # Content gap analysis
    'roadmap': 120,             # 30/60/90 day strategic roadmap
    'quick_suggestions': 25,    # Quick optimization tips
    'competitor_analysis': 150, # Deep competitor comparison
}


class AIService:
    """
    Manages all AI-powered SEO analysis using Google Gemini PRO.
    Handles credit tracking, structured prompts, and response formatting.
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )
    
    def check_credits(self, user_id: str, operation_type: str) -> Tuple[bool, int]:
        """
        Check if user has sufficient credits for operation.
        
        Returns:
            Tuple of (has_credits: bool, current_balance: int)
        """
        try:
            profile = self.supabase.table('profiles').select('credits_balance').eq('id', user_id).single().execute()
            
            if not profile.data:
                return False, 0
            
            balance = profile.data['credits_balance']
            required = CREDIT_COSTS.get(operation_type, 0)
            
            return balance >= required, balance
            
        except Exception as e:
            logger.error(f"Error checking credits: {e}")
            return False, 0
    
    def deduct_credits(
        self,
        user_id: str,
        amount: int,
        operation_type: str,
        scan_id: Optional[str] = None,
        tokens_used: int = 0
    ) -> bool:
        """
        Deduct credits from user balance and record usage.
        """
        try:
            # Get current balance
            profile = self.supabase.table('profiles').select('credits_balance').eq('id', user_id).single().execute()
            current_balance = profile.data['credits_balance']
            
            if current_balance < amount:
                logger.warning(f"Insufficient credits for user {user_id}: {current_balance} < {amount}")
                return False
            
            new_balance = current_balance - amount
            
            # Update profile
            self.supabase.table('profiles').update({
                'credits_balance': new_balance,
                'total_credits_used': self.supabase.rpc('increment', {'x': amount})
            }).eq('id', user_id).execute()
            
            # Create transaction record
            self.supabase.table('credit_transactions').insert({
                'user_id': user_id,
                'type': 'credit_usage',
                'amount': -amount,
                'balance_after': new_balance,
                'reference_id': scan_id,
                'reference_type': 'ai_operation',
                'description': f"AI credits used for {operation_type}"
            }).execute()
            
            logger.info(f"Deducted {amount} credits from user {user_id}. New balance: {new_balance}")
            return True
            
        except Exception as e:
            logger.error(f"Error deducting credits: {e}")
            return False
    
    def generate_seo_audit(
        self,
        user_id: str,
        scan_id: str,
        scan_data: Dict,
        user_tier: str
    ) -> Optional[Dict]:
        """
        Generate comprehensive SEO audit report using Gemini PRO.
        
        Args:
            user_id: User's unique ID
            scan_id: Scan record ID
            scan_data: Raw scan data from SEO engine
            user_tier: User's subscription tier (affects depth)
        
        Returns:
            Structured audit report or None if failed
        """
        operation = 'seo_audit'
        
        # Check credits
        has_credits, balance = self.check_credits(user_id, operation)
        if not has_credits:
            logger.warning(f"User {user_id} has insufficient credits: {balance}")
            return None
        
        try:
            # Build context-rich prompt
            prompt = self._build_audit_prompt(scan_data, user_tier)
            
            # Generate with Gemini
            start_time = datetime.utcnow()
            response = self.model.generate_content(prompt)
            end_time = datetime.utcnow()
            
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Parse and structure response
            audit_report = self._parse_audit_response(response.text)
            
            # Calculate token usage (approximate)
            input_tokens = len(prompt.split()) * 1.3  # Rough estimate
            output_tokens = len(response.text.split()) * 1.3
            total_tokens = int(input_tokens + output_tokens)
            
            # Deduct credits
            credits_used = CREDIT_COSTS[operation]
            if not self.deduct_credits(user_id, credits_used, operation, scan_id, total_tokens):
                logger.error(f"Failed to deduct credits after AI generation")
            
            # Log AI usage
            self._log_ai_usage(
                user_id=user_id,
                scan_id=scan_id,
                operation=operation,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                total_tokens=total_tokens,
                credits_used=credits_used,
                response_time_ms=response_time_ms,
                response_text=response.text,
                success=True
            )
            
            return audit_report
            
        except Exception as e:
            logger.error(f"Error generating SEO audit: {e}")
            
            # Log failed attempt
            self._log_ai_usage(
                user_id=user_id,
                scan_id=scan_id,
                operation=operation,
                success=False,
                error_message=str(e)
            )
            
            return None
    
    def _build_audit_prompt(self, scan_data: Dict, user_tier: str) -> str:
        """
        Build comprehensive audit prompt with scan data.
        """
        # Determine depth based on tier
        depth_instructions = {
            'demo': "Provide a concise overview with top 3 priorities only.",
            'pro': "Provide detailed analysis with actionable recommendations.",
            'agency': "Provide in-depth analysis with strategic insights and competitive positioning.",
            'elite': "Provide exhaustive analysis with advanced strategies, technical implementation details, and ROI projections."
        }
        
        depth = depth_instructions.get(user_tier, depth_instructions['pro'])
        
        prompt = f"""You are an expert SEO strategist analyzing a website. Provide a comprehensive SEO audit report.

WEBSITE ANALYZED:
URL: {scan_data.get('url')}
Domain: {scan_data.get('domain')}

CURRENT PERFORMANCE METRICS:
- Overall SEO Score: {scan_data.get('overall_score', 'N/A')}/100
- Technical Score: {scan_data.get('technical_score', 'N/A')}/100
- Content Score: {scan_data.get('content_score', 'N/A')}/100
- Performance Score: {scan_data.get('performance_score', 'N/A')}/100

PAGE CHARACTERISTICS:
- Title: {scan_data.get('title', 'N/A')}
- Meta Description: {scan_data.get('meta_description', 'N/A')}
- H1 Tags: {', '.join(scan_data.get('h1_tags', []))}
- Word Count: {scan_data.get('word_count', 'N/A')}
- Images: {scan_data.get('image_count', 'N/A')}
- Links: {scan_data.get('link_count', 'N/A')}

TECHNICAL DETAILS:
- Page Size: {scan_data.get('page_size_kb', 'N/A')} KB
- Load Time: {scan_data.get('load_time_ms', 'N/A')} ms
- Mobile Friendly: {scan_data.get('is_mobile_friendly', 'N/A')}
- SSL: {scan_data.get('has_ssl', 'N/A')}

ISSUES IDENTIFIED:
- Critical: {scan_data.get('critical_issues', 0)}
- High: {scan_data.get('high_issues', 0)}
- Medium: {scan_data.get('medium_issues', 0)}
- Low: {scan_data.get('low_issues', 0)}

ANALYSIS DEPTH: {depth}

Generate a comprehensive SEO audit report in the following structured format:

## EXECUTIVE SUMMARY
Provide a 2-3 sentence overview of the site's current SEO health and primary opportunities.

## CRITICAL FINDINGS
List the top 3-5 critical issues that need immediate attention. For each:
- Issue description
- SEO impact (high/medium/low)
- Specific fix instructions
- Expected improvement

## TECHNICAL SEO ANALYSIS
Analyze:
- Site speed and Core Web Vitals
- Mobile optimization
- Structured data
- XML sitemap and robots.txt
- Security (HTTPS, mixed content)
- Crawlability issues

## CONTENT OPTIMIZATION
Evaluate:
- Title tag optimization
- Meta description quality
- Header structure (H1-H6)
- Content depth and quality
- Keyword targeting
- Internal linking structure
- Image optimization (alt tags, file size)

## ON-PAGE FACTORS
Review:
- URL structure
- Canonical tags
- Schema markup opportunities
- Social meta tags
- Page load optimization

## COMPETITIVE INSIGHTS
Based on industry standards and common patterns:
- Where this site excels
- Where competitors likely have advantages
- Untapped opportunities

## PRIORITIZED ACTION PLAN
Create a phased implementation roadmap:

### PHASE 1: QUICK WINS (Week 1-2)
List 5-7 high-impact, low-effort fixes

### PHASE 2: FOUNDATION (Week 3-6)
List technical improvements and content updates

### PHASE 3: GROWTH (Month 2-3)
List strategic initiatives and content creation

## ESTIMATED IMPACT
Provide realistic projections:
- Expected organic traffic increase: X-Y%
- Timeline to see results: X-Y months
- Estimated SEO score improvement: X points

## NEXT STEPS
Provide 3-5 immediate next actions to take.

---
IMPORTANT: Be specific, actionable, and data-driven. Avoid generic advice. Focus on this specific site's context."""

        return prompt
    
    def _parse_audit_response(self, response_text: str) -> Dict:
        """
        Parse Gemini's response into structured format.
        """
        try:
            # Structure the response into sections
            sections = {}
            current_section = None
            current_content = []
            
            lines = response_text.split('\n')
            
            for line in lines:
                # Detect section headers (## SECTION NAME)
                if line.startswith('## '):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line.replace('##', '').strip()
                    current_content = []
                else:
                    current_content.append(line)
            
            # Add last section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            return {
                'full_text': response_text,
                'sections': sections,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error parsing audit response: {e}")
            return {
                'full_text': response_text,
                'sections': {},
                'generated_at': datetime.utcnow().isoformat()
            }
    
    def generate_keyword_research(
        self,
        user_id: str,
        primary_keyword: str,
        industry: str,
        target_audience: str
    ) -> Optional[Dict]:
        """
        Generate keyword expansion and clustering analysis.
        """
        operation = 'keyword_research'
        
        # Check credits
        has_credits, balance = self.check_credits(user_id, operation)
        if not has_credits:
            return None
        
        try:
            prompt = f"""You are an SEO keyword research expert. Analyze and expand the following seed keyword.

PRIMARY KEYWORD: "{primary_keyword}"
INDUSTRY: {industry}
TARGET AUDIENCE: {target_audience}

Provide a comprehensive keyword research report in JSON format:

{{
  "seed_keyword": "{primary_keyword}",
  "keyword_variations": [
    {{
      "keyword": "exact variation",
      "search_intent": "informational/transactional/navigational/commercial",
      "difficulty_estimate": "low/medium/high",
      "relevance_score": 0-10,
      "reasoning": "why this keyword matters"
    }}
  ],
  "long_tail_opportunities": [
    {{
      "keyword": "long-tail phrase",
      "search_intent": "...",
      "user_question": "what question does this answer",
      "content_format": "blog post/product page/guide/video"
    }}
  ],
  "semantic_clusters": [
    {{
      "cluster_name": "Topic Category",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "content_strategy": "how to approach this cluster"
    }}
  ],
  "competitor_keywords": [
    {{
      "keyword": "competitor focus keyword",
      "opportunity": "why you should target this",
      "difficulty": "low/medium/high"
    }}
  ],
  "content_gaps": [
    {{
      "topic": "underserved topic area",
      "opportunity": "what's missing in current content",
      "priority": "high/medium/low"
    }}
  ]
}}

Provide 10-15 variations, 8-10 long-tail opportunities, 3-5 semantic clusters, 5-7 competitor keywords, and 3-5 content gaps."""

            start_time = datetime.utcnow()
            response = self.model.generate_content(prompt)
            end_time = datetime.utcnow()
            
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Parse JSON response
            keyword_data = self._extract_json_from_response(response.text)
            
            # Calculate tokens
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(response.text.split()) * 1.3
            total_tokens = int(input_tokens + output_tokens)
            
            # Deduct credits
            credits_used = CREDIT_COSTS[operation]
            self.deduct_credits(user_id, credits_used, operation, None, total_tokens)
            
            # Log usage
            self._log_ai_usage(
                user_id=user_id,
                operation=operation,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                total_tokens=total_tokens,
                credits_used=credits_used,
                response_time_ms=response_time_ms,
                response_text=response.text,
                response_structured=keyword_data,
                success=True
            )
            
            return keyword_data
            
        except Exception as e:
            logger.error(f"Error generating keyword research: {e}")
            self._log_ai_usage(
                user_id=user_id,
                operation=operation,
                success=False,
                error_message=str(e)
            )
            return None
    
    def generate_seo_roadmap(
        self,
        user_id: str,
        scan_id: str,
        current_metrics: Dict,
        business_goals: str
    ) -> Optional[Dict]:
        """
        Generate 30/60/90 day SEO implementation roadmap.
        """
        operation = 'roadmap'
        
        has_credits, balance = self.check_credits(user_id, operation)
        if not has_credits:
            return None
        
        try:
            prompt = f"""You are a strategic SEO consultant. Create a detailed 30/60/90 day implementation roadmap.

CURRENT STATE:
- Overall SEO Score: {current_metrics.get('overall_score', 'N/A')}/100
- Monthly Organic Traffic: {current_metrics.get('traffic', 'N/A')}
- Technical Issues: {current_metrics.get('critical_issues', 0)} critical, {current_metrics.get('high_issues', 0)} high
- Domain: {current_metrics.get('domain')}

BUSINESS GOALS:
{business_goals}

Create a comprehensive roadmap with the following structure:

## 30-DAY SPRINT: FOUNDATION & QUICK WINS
### Week 1-2: Technical Fixes
- List specific technical tasks with priority
- Estimated hours per task
- Dependencies

### Week 3-4: Content Optimization
- On-page optimization tasks
- Content updates needed
- Quick content creation opportunities

### Expected Outcomes (30 Days)
- SEO score improvement: X points
- Issues resolved: X critical, Y high
- New rankings potential: X-Y keywords
- Traffic lift: X-Y%

## 60-DAY PHASE: GROWTH ACCELERATION
### Week 5-6: Content Strategy
- New content creation plan
- Keyword targeting
- Link building foundation

### Week 7-8: Technical Enhancements
- Advanced optimizations
- Schema implementation
- Performance tuning

### Expected Outcomes (60 Days)
- Additional score improvement
- New content indexed
- Backlink growth
- Organic visibility increase

## 90-DAY MILESTONE: SUSTAINABLE GROWTH
### Week 9-10: Authority Building
- Strategic content
- Competitive positioning
- Link building campaign

### Week 11-12: Optimization & Scale
- A/B testing
- Conversion optimization
- Reporting and adjustment

### Expected Outcomes (90 Days)
- Total SEO score: X/100
- Organic traffic growth: X-Y%
- Keyword rankings: X-Y new page 1 rankings
- Revenue impact: Estimated $X-Y increase

## RESOURCE REQUIREMENTS
- In-house hours needed
- External services recommended
- Budget allocation by phase
- Tools and subscriptions

## SUCCESS METRICS
Define KPIs for each phase with specific targets.

## RISK FACTORS & MITIGATION
Identify potential obstacles and solutions.

Be specific with tasks, timelines, and realistic expectations."""

            start_time = datetime.utcnow()
            response = self.model.generate_content(prompt)
            end_time = datetime.utcnow()
            
            response_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            roadmap_data = self._parse_audit_response(response.text)
            
            # Calculate tokens
            input_tokens = len(prompt.split()) * 1.3
            output_tokens = len(response.text.split()) * 1.3
            total_tokens = int(input_tokens + output_tokens)
            
            # Deduct credits
            credits_used = CREDIT_COSTS[operation]
            self.deduct_credits(user_id, credits_used, operation, scan_id, total_tokens)
            
            # Log usage
            self._log_ai_usage(
                user_id=user_id,
                scan_id=scan_id,
                operation=operation,
                input_tokens=int(input_tokens),
                output_tokens=int(output_tokens),
                total_tokens=total_tokens,
                credits_used=credits_used,
                response_time_ms=response_time_ms,
                response_text=response.text,
                success=True
            )
            
            return roadmap_data
            
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            self._log_ai_usage(
                user_id=user_id,
                scan_id=scan_id,
                operation=operation,
                success=False,
                error_message=str(e)
            )
            return None
    
    def _extract_json_from_response(self, text: str) -> Dict:
        """
        Extract JSON from Gemini response (handles markdown code blocks).
        """
        try:
            # Remove markdown code fences if present
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            
            return json.loads(text.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {'raw_text': text, 'parse_error': str(e)}
    
    def _log_ai_usage(
        self,
        user_id: str,
        operation: str,
        scan_id: Optional[str] = None,
        input_tokens: int = 0,
        output_tokens: int = 0,
        total_tokens: int = 0,
        credits_used: int = 0,
        response_time_ms: int = 0,
        response_text: Optional[str] = None,
        response_structured: Optional[Dict] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ):
        """
        Log AI usage to database for analytics and debugging.
        """
        try:
            self.supabase.table('ai_usage').insert({
                'user_id': user_id,
                'scan_id': scan_id,
                'operation_type': operation,
                'model_name': MODEL_NAME,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'total_tokens': total_tokens,
                'credits_consumed': credits_used,
                'response_time_ms': response_time_ms,
                'response_text': response_text,
                'response_structured': response_structured,
                'success': success,
                'error_message': error_message
            }).execute()
        except Exception as e:
            logger.error(f"Error logging AI usage: {e}")