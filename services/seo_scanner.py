"""
NEXUS SEO INTELLIGENCE - Smart SEO Scanner Module
Advanced AI-Powered Website Analysis System
"""

import os
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import google.generativeai as genai

class SmartSEOScanner:
    """
    Advanced SEO Scanner with AI-powered analysis
    Features: Multi-agent AI system, competitive intelligence, action plans
    """
    
    def __init__(self, gemini_api_key=None):
        """Initialize the scanner with AI capabilities"""
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.ai_model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.ai_model = None
            print("⚠️ Warning: Gemini API key not found. AI features will be disabled.")
    
    def scan_website(self, url, include_ai=True):
        """
        Perform comprehensive website scan
        
        Args:
            url (str): Website URL to scan
            include_ai (bool): Whether to include AI analysis
            
        Returns:
            dict: Complete scan results with AI insights
        """
        print(f"🔍 Starting scan for: {url}")
        
        # Step 1: Scrape basic data
        scan_data = self._scrape_website(url)
        
        if not scan_data:
            return {"error": "Failed to scrape website"}
        
        # Step 2: Technical analysis
        technical_analysis = self._analyze_technical(scan_data)
        
        # Step 3: Content analysis
        content_analysis = self._analyze_content(scan_data)
        
        # Step 4: AI-powered insights (if enabled)
        if include_ai and self.ai_model:
            print("🧠 Running AI analysis...")
            
            ai_insights = {
                'technical_ai': self._ai_technical_analysis(scan_data),
                'content_ai': self._ai_content_analysis(scan_data),
                'competitive_ai': self._ai_competitive_analysis(scan_data),
                'action_plan': self._ai_generate_action_plan(scan_data)
            }
        else:
            ai_insights = {}
        
        # Combine all results
        result = {
            'url': url,
            'scan_timestamp': datetime.now().isoformat(),
            'basic_data': scan_data,
            'technical_analysis': technical_analysis,
            'content_analysis': content_analysis,
            'ai_insights': ai_insights,
            'overall_score': self._calculate_overall_score(technical_analysis, content_analysis)
        }
        
        print("✅ Scan completed!")
        return result
    
    def _scrape_website(self, url):
        """Scrape website and extract data"""
        try:
            # Normalize URL
            if not url.startswith('http'):
                url = 'https://' + url
            
            # Fetch website
            start_time = time.time()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
            load_time = int((time.time() - start_time) * 1000)
            
            if response.status_code != 200:
                print(f"⚠️ Warning: Status code {response.status_code}")
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract metadata
            title = soup.find('title')
            title = title.text.strip() if title else ''
            
            description = ''
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '').strip()
            
            # Extract content metrics
            text_content = soup.get_text()
            word_count = len([word for word in text_content.split() if len(word) > 2])
            
            h1_tags = soup.find_all('h1')
            h2_tags = soup.find_all('h2')
            h3_tags = soup.find_all('h3')
            
            images = soup.find_all('img')
            images_without_alt = [img for img in images if not img.get('alt')]
            
            links = soup.find_all('a', href=True)
            internal_links = []
            external_links = []
            
            base_domain = urlparse(url).netloc
            
            for link in links:
                href = link.get('href', '')
                if href.startswith('http'):
                    if base_domain in href:
                        internal_links.append(href)
                    else:
                        external_links.append(href)
                elif href.startswith('/'):
                    internal_links.append(urljoin(url, href))
            
            # Check technical elements
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            mobile_friendly = viewport is not None
            
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            has_canonical = canonical is not None
            
            # Check for structured data
            structured_data = soup.find_all('script', attrs={'type': 'application/ld+json'})
            has_schema = len(structured_data) > 0
            
            # Page size
            page_size = len(response.content) / 1024  # KB
            
            # HTTPS check
            https_enabled = url.startswith('https')
            
            # Open Graph tags
            og_tags = {}
            for tag in soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')}):
                og_tags[tag.get('property')] = tag.get('content')
            
            return {
                'url': url,
                'status_code': response.status_code,
                'load_time': load_time,
                'page_size': round(page_size, 2),
                'https': https_enabled,
                'title': title,
                'title_length': len(title),
                'description': description,
                'description_length': len(description),
                'word_count': word_count,
                'h1_count': len(h1_tags),
                'h1_texts': [h1.get_text().strip() for h1 in h1_tags][:3],
                'h2_count': len(h2_tags),
                'h3_count': len(h3_tags),
                'images_total': len(images),
                'images_without_alt': len(images_without_alt),
                'internal_links': len(internal_links),
                'external_links': len(external_links),
                'mobile_friendly': mobile_friendly,
                'has_canonical': has_canonical,
                'has_schema': has_schema,
                'og_tags': og_tags,
                'content_sample': text_content[:500]
            }
            
        except requests.Timeout:
            print("❌ Error: Request timeout")
            return None
        except requests.RequestException as e:
            print(f"❌ Error: {str(e)}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
            return None
    
    def _analyze_technical(self, data):
        """Analyze technical SEO aspects"""
        issues = []
        warnings = []
        good_practices = []
        score = 100
        
        # HTTPS
        if not data['https']:
            issues.append("Site not using HTTPS - critical security issue")
            score -= 15
        else:
            good_practices.append("✓ HTTPS enabled")
        
        # Load time
        if data['load_time'] > 3000:
            issues.append(f"Slow load time ({data['load_time']}ms) - should be under 3000ms")
            score -= 10
        elif data['load_time'] > 1500:
            warnings.append(f"Load time could be improved ({data['load_time']}ms)")
            score -= 5
        else:
            good_practices.append(f"✓ Fast load time ({data['load_time']}ms)")
        
        # Page size
        if data['page_size'] > 3000:
            issues.append(f"Large page size ({data['page_size']}KB) - should be under 3MB")
            score -= 10
        elif data['page_size'] > 1500:
            warnings.append(f"Page size could be optimized ({data['page_size']}KB)")
            score -= 5
        else:
            good_practices.append(f"✓ Optimized page size ({data['page_size']}KB)")
        
        # Mobile friendly
        if not data['mobile_friendly']:
            issues.append("Missing viewport meta tag - not mobile-friendly")
            score -= 15
        else:
            good_practices.append("✓ Mobile-friendly viewport")
        
        # Canonical
        if not data['has_canonical']:
            warnings.append("Missing canonical URL tag")
            score -= 5
        else:
            good_practices.append("✓ Canonical URL set")
        
        # Structured data
        if not data['has_schema']:
            warnings.append("No structured data (Schema.org) found")
            score -= 5
        else:
            good_practices.append("✓ Structured data implemented")
        
        # Images alt text
        if data['images_without_alt'] > 0:
            warnings.append(f"{data['images_without_alt']} images missing alt text")
            score -= min(data['images_without_alt'] * 2, 10)
        
        return {
            'score': max(0, score),
            'issues': issues,
            'warnings': warnings,
            'good_practices': good_practices
        }
    
    def _analyze_content(self, data):
        """Analyze content quality"""
        issues = []
        warnings = []
        good_practices = []
        score = 100
        
        # Title
        if not data['title']:
            issues.append("Missing page title")
            score -= 20
        elif data['title_length'] < 30:
            warnings.append(f"Title too short ({data['title_length']} chars) - recommended 50-60")
            score -= 5
        elif data['title_length'] > 70:
            warnings.append(f"Title too long ({data['title_length']} chars) - may be truncated")
            score -= 5
        else:
            good_practices.append(f"✓ Well-optimized title ({data['title_length']} chars)")
        
        # Description
        if not data['description']:
            issues.append("Missing meta description")
            score -= 15
        elif data['description_length'] < 120:
            warnings.append(f"Description too short ({data['description_length']} chars) - recommended 150-160")
            score -= 5
        elif data['description_length'] > 170:
            warnings.append(f"Description too long ({data['description_length']} chars) - may be truncated")
            score -= 5
        else:
            good_practices.append(f"✓ Well-optimized description ({data['description_length']} chars)")
        
        # H1 tags
        if data['h1_count'] == 0:
            issues.append("Missing H1 tag")
            score -= 15
        elif data['h1_count'] > 1:
            warnings.append(f"Multiple H1 tags ({data['h1_count']}) - should have only one")
            score -= 5
        else:
            good_practices.append("✓ Proper H1 structure")
        
        # Word count
        if data['word_count'] < 300:
            warnings.append(f"Thin content ({data['word_count']} words) - recommended 500+ words")
            score -= 10
        elif data['word_count'] > 500:
            good_practices.append(f"✓ Good content length ({data['word_count']} words)")
        
        # Images
        if data['images_total'] == 0:
            warnings.append("No images found - consider adding visual content")
            score -= 5
        
        # Links
        if data['internal_links'] == 0:
            warnings.append("No internal links found")
            score -= 5
        
        return {
            'score': max(0, score),
            'issues': issues,
            'warnings': warnings,
            'good_practices': good_practices
        }
    
    def _ai_technical_analysis(self, data):
        """AI-powered technical SEO analysis"""
        if not self.ai_model:
            return {}
        
        prompt = f"""You are an expert Technical SEO consultant. Analyze this website data:

URL: {data['url']}
Load Time: {data['load_time']}ms
Page Size: {data['page_size']}KB
HTTPS: {data['https']}
Mobile Friendly: {data['mobile_friendly']}
Has Schema: {data['has_schema']}

Provide a technical SEO analysis in JSON format:
{{
    "score": 85,
    "critical_issues": ["issue1", "issue2"],
    "recommendations": [
        {{
            "priority": "High",
            "issue": "Specific technical issue",
            "solution": "Detailed solution",
            "impact": "Expected improvement",
            "implementation_time": "Estimated time to fix"
        }}
    ],
    "performance_insights": "Brief analysis of performance"
}}

Focus on actionable, specific recommendations. Be concise but detailed."""
        
        try:
            response = self.ai_model.generate_content(prompt)
            result = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(result)
        except Exception as e:
            print(f"AI Analysis Error: {str(e)}")
            return {}
    
    def _ai_content_analysis(self, data):
        """AI-powered content quality analysis"""
        if not self.ai_model:
            return {}
        
        prompt = f"""You are a content SEO expert. Analyze this content:

Title: {data['title']}
Description: {data['description']}
Word Count: {data['word_count']}
H1 Tags: {data['h1_count']} - {data['h1_texts']}
Content Sample: {data['content_sample']}

Provide content analysis in JSON format:
{{
    "score": 75,
    "content_quality": "Brief assessment",
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "keyword_opportunities": ["keyword1", "keyword2"],
    "content_strategy": [
        "Specific action 1",
        "Specific action 2"
    ],
    "tone_analysis": "Professional/Casual/Technical etc."
}}

Be specific and actionable."""
        
        try:
            response = self.ai_model.generate_content(prompt)
            result = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(result)
        except Exception as e:
            print(f"AI Analysis Error: {str(e)}")
            return {}
    
    def _ai_competitive_analysis(self, data):
        """AI-powered competitive intelligence"""
        if not self.ai_model:
            return {}
        
        prompt = f"""You are a competitive intelligence expert. Based on this website:

URL: {data['url']}
Title: {data['title']}
Content: {data['content_sample']}

Provide competitive analysis in JSON format:
{{
    "likely_competitors": ["competitor1.com", "competitor2.com"],
    "market_positioning": "Brief positioning statement",
    "competitive_advantages": ["advantage1", "advantage2"],
    "differentiation_opportunities": ["opportunity1", "opportunity2"],
    "quick_wins": [
        "Specific tactic to outrank competitors"
    ]
}}

Be strategic and specific."""
        
        try:
            response = self.ai_model.generate_content(prompt)
            result = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(result)
        except Exception as e:
            print(f"AI Analysis Error: {str(e)}")
            return {}
    
    def _ai_generate_action_plan(self, data):
        """AI-powered 30-day action plan"""
        if not self.ai_model:
            return {}
        
        prompt = f"""You are a strategic SEO consultant. Create a 30-day action plan for this website:

URL: {data['url']}
Current Performance:
- Load Time: {data['load_time']}ms
- Word Count: {data['word_count']}
- Technical Score: Basic audit needed

Create a prioritized plan in JSON format:
{{
    "estimated_traffic_increase": "15-25%",
    "week_1_quick_wins": [
        {{"task": "Specific task", "impact": "High/Medium/Low", "effort": "1-10", "details": "How to do it"}}
    ],
    "week_2_3_improvements": [
        {{"task": "Specific task", "impact": "High/Medium/Low", "effort": "1-10", "details": "How to do it"}}
    ],
    "week_4_strategy": [
        {{"task": "Specific task", "impact": "High/Medium/Low", "effort": "1-10", "details": "How to do it"}}
    ],
    "success_metrics": ["metric1", "metric2"],
    "budget_estimate": "If paid tools/services needed"
}}

Prioritize by ROI. Be specific and actionable."""
        
        try:
            response = self.ai_model.generate_content(prompt)
            result = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(result)
        except Exception as e:
            print(f"AI Analysis Error: {str(e)}")
            return {}
    
    def _calculate_overall_score(self, technical, content):
        """Calculate overall SEO score"""
        tech_score = technical.get('score', 0)
        content_score = content.get('score', 0)
        
        # Weighted average (technical = 60%, content = 40%)
        overall = (tech_score * 0.6) + (content_score * 0.4)
        
        return {
            'overall': round(overall, 1),
            'technical': tech_score,
            'content': content_score,
            'grade': self._get_grade(overall)
        }
    
    def _get_grade(self, score):
        """Convert score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def export_report(self, scan_result, format='json', filename=None):
        """Export scan results to file"""
        if not filename:
            domain = urlparse(scan_result['url']).netloc
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"seo_report_{domain}_{timestamp}.{format}"
        
        if format == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(scan_result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Report saved: {filename}")
        return filename


# CLI Usage Example
if __name__ == "__main__":
    # Initialize scanner
    scanner = SmartSEOScanner()
    
    # Example scan
    url = "https://example.com"
    
    print(f"\n{'='*60}")
    print(f"NEXUS SEO INTELLIGENCE - Smart Scanner")
    print(f"{'='*60}\n")
    
    # Perform scan
    results = scanner.scan_website(url, include_ai=True)
    
    # Display results
    if results and 'error' not in results:
        print(f"\n📊 SCAN RESULTS")
        print(f"{'='*60}")
        print(f"URL: {results['url']}")
        print(f"Overall Score: {results['overall_score']['overall']}/100 (Grade: {results['overall_score']['grade']})")
        print(f"Technical Score: {results['overall_score']['technical']}/100")
        print(f"Content Score: {results['overall_score']['content']}/100")
        
        # Export
        filename = scanner.export_report(results)
        print(f"\n✅ Full report saved to: {filename}")
    else:
        print("\n❌ Scan failed!")