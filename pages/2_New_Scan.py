"""
NEXUS SEO INTELLIGENCE - SMART AI-POWERED PLATFORM
Advanced SEO Analysis with Multi-Agent AI System
"""

import streamlit as st
import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai
from supabase import create_client
import time

# Page config
st.set_page_config(
    page_title="Smart SEO Analysis",
    page_icon="🧠",
    layout="wide"
)

# Initialize Supabase
@st.cache_resource
def get_supabase_client():
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
    except:
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except:
            pass
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Supabase credentials not configured")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

supabase = get_supabase_client()

# Initialize Gemini AI
@st.cache_resource
def get_gemini_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            return genai.GenerativeModel('gemini-1.5-pro')
        return None
    except:
        return None

gemini_model = get_gemini_client()

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .analysis-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    .insight-box {
        background: #f8fafc;
        border-left: 4px solid #6366f1;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
    }
    .metric-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .score-excellent {
        color: #10b981;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-good {
        color: #3b82f6;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-warning {
        color: #f59e0b;
        font-size: 2rem;
        font-weight: bold;
    }
    .score-poor {
        color: #ef4444;
        font-size: 2rem;
        font-weight: bold;
    }
    .ai-thinking {
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-weight: bold;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

# Check login
if 'user' not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# AI Analysis Functions
class SmartSEOAnalyzer:
    """Advanced Multi-Agent AI System for SEO Analysis"""
    
    def __init__(self, model):
        self.model = model
        
    def analyze_technical_seo(self, data):
        """Technical SEO Analysis Agent"""
        prompt = f"""You are an expert Technical SEO analyst. Analyze this website data and provide detailed insights:

URL: {data.get('url')}
Load Time: {data.get('load_time')}ms
Page Size: {data.get('page_size')}KB
HTTPS: {data.get('https')}
Mobile Friendly: {data.get('mobile_friendly')}

Provide:
1. Technical SEO Score (0-100)
2. Critical issues found
3. Performance bottlenecks
4. Specific recommendations with priority (High/Medium/Low)
5. Expected impact of each fix

Format as JSON:
{{
    "score": 85,
    "critical_issues": ["issue1", "issue2"],
    "recommendations": [
        {{"priority": "High", "issue": "...", "solution": "...", "impact": "..."}}
    ]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"score": 0, "critical_issues": [], "recommendations": []}
    
    def analyze_content_quality(self, data):
        """Content Quality Analysis Agent"""
        prompt = f"""You are a content SEO expert. Analyze this content:

Title: {data.get('title', 'No title')}
Description: {data.get('description', 'No description')}
Word Count: {data.get('word_count', 0)}
H1 Tags: {data.get('h1_count', 0)}
H2 Tags: {data.get('h2_count', 0)}

Provide:
1. Content Quality Score (0-100)
2. Content gaps and missing elements
3. Keyword optimization opportunities
4. Readability analysis
5. Specific content improvements

Format as JSON:
{{
    "score": 75,
    "strengths": ["strength1", "strength2"],
    "weaknesses": ["weakness1", "weakness2"],
    "content_strategy": ["action1", "action2"],
    "keyword_opportunities": ["keyword1", "keyword2"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"score": 0, "strengths": [], "weaknesses": [], "content_strategy": [], "keyword_opportunities": []}
    
    def analyze_competitor_strategy(self, url, industry):
        """Competitive Analysis Agent"""
        prompt = f"""You are a competitive intelligence expert. Based on this website:

URL: {url}
Industry: {industry}

Provide:
1. Likely competitors in this niche
2. Competitive advantages to leverage
3. Market positioning strategy
4. Differentiation opportunities
5. Quick wins to outrank competitors

Format as JSON:
{{
    "competitors": ["competitor1.com", "competitor2.com"],
    "competitive_advantages": ["advantage1", "advantage2"],
    "positioning_strategy": "...",
    "quick_wins": ["win1", "win2"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"competitors": [], "competitive_advantages": [], "positioning_strategy": "", "quick_wins": []}
    
    def generate_action_plan(self, technical, content, competitive):
        """Strategy Synthesis Agent - Creates actionable plan"""
        prompt = f"""You are a strategic SEO consultant. Synthesize these analyses into a 30-day action plan:

Technical Analysis: {json.dumps(technical)}
Content Analysis: {json.dumps(content)}
Competitive Analysis: {json.dumps(competitive)}

Create a prioritized 30-day action plan with:
1. Week 1 priorities (quick wins)
2. Week 2-3 priorities (medium-term improvements)
3. Week 4 priorities (strategic initiatives)
4. Success metrics to track
5. Estimated traffic impact

Format as JSON:
{{
    "week_1": [{{"task": "...", "impact": "High/Medium/Low", "effort": "1-10"}}],
    "week_2_3": [...],
    "week_4": [...],
    "success_metrics": ["metric1", "metric2"],
    "estimated_traffic_increase": "20-30%"
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text.replace('```json', '').replace('```', '').strip())
        except:
            return {"week_1": [], "week_2_3": [], "week_4": [], "success_metrics": [], "estimated_traffic_increase": "0%"}

def scrape_website(url):
    """Scrape website data"""
    try:
        # Add https if not present
        if not url.startswith('http'):
            url = 'https://' + url
        
        start_time = time.time()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        load_time = int((time.time() - start_time) * 1000)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data
        title = soup.find('title').text if soup.find('title') else ''
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        
        word_count = len(soup.get_text().split())
        h1_count = len(soup.find_all('h1'))
        h2_count = len(soup.find_all('h2'))
        images = len(soup.find_all('img'))
        links = len(soup.find_all('a'))
        
        page_size = len(response.content) / 1024  # KB
        https = url.startswith('https')
        
        # Check mobile-friendly (basic check)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        mobile_friendly = viewport is not None
        
        return {
            'url': url,
            'title': title,
            'description': description,
            'word_count': word_count,
            'h1_count': h1_count,
            'h2_count': h2_count,
            'images': images,
            'links': links,
            'load_time': load_time,
            'page_size': round(page_size, 2),
            'https': https,
            'mobile_friendly': mobile_friendly,
            'status_code': response.status_code
        }
    except Exception as e:
        st.error(f"Error scraping website: {str(e)}")
        return None

# Main UI
st.title("🧠 Smart SEO Intelligence Platform")
st.markdown("### AI-Powered Multi-Agent SEO Analysis System")
st.markdown("---")

# Scan form
with st.form("smart_scan_form"):
    st.markdown("### 🎯 Enter Website Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        url = st.text_input("🌐 Website URL", placeholder="example.com", help="Enter the URL to analyze")
    
    with col2:
        industry = st.selectbox(
            "🏢 Industry/Niche",
            ["E-commerce", "SaaS", "Blog/Content", "Local Business", "Agency", "Healthcare", "Finance", "Education", "Real Estate", "Other"]
        )
    
    scan_depth = st.select_slider(
        "🔍 Analysis Depth",
        options=["Quick Scan", "Standard", "Deep Analysis", "Comprehensive"],
        value="Standard",
        help="Deeper analysis uses more AI processing and credits"
    )
    
    submit = st.form_submit_button("🚀 Start Smart Analysis", use_container_width=True)

if submit and url:
    if not gemini_model:
        st.error("❌ AI Engine not configured. Please add GEMINI_API_KEY to your secrets.")
        st.stop()
    
    # Progress tracking
    progress_bar = st.progress(0)
    status = st.empty()
    
    # Step 1: Scrape website
    status.markdown('<div class="ai-thinking">🔍 Scanning website...</div>', unsafe_allow_html=True)
    progress_bar.progress(20)
    
    scan_data = scrape_website(url)
    
    if not scan_data:
        st.error("Failed to scan website. Please check the URL and try again.")
        st.stop()
    
    # Step 2: AI Analysis
    status.markdown('<div class="ai-thinking">🧠 AI Agent 1: Analyzing technical SEO...</div>', unsafe_allow_html=True)
    progress_bar.progress(40)
    
    analyzer = SmartSEOAnalyzer(gemini_model)
    technical_analysis = analyzer.analyze_technical_seo(scan_data)
    
    status.markdown('<div class="ai-thinking">📝 AI Agent 2: Evaluating content quality...</div>', unsafe_allow_html=True)
    progress_bar.progress(60)
    
    content_analysis = analyzer.analyze_content_quality(scan_data)
    
    status.markdown('<div class="ai-thinking">🎯 AI Agent 3: Analyzing competition...</div>', unsafe_allow_html=True)
    progress_bar.progress(80)
    
    competitive_analysis = analyzer.analyze_competitor_strategy(url, industry)
    
    status.markdown('<div class="ai-thinking">📋 AI Agent 4: Creating action plan...</div>', unsafe_allow_html=True)
    progress_bar.progress(90)
    
    action_plan = analyzer.generate_action_plan(technical_analysis, content_analysis, competitive_analysis)
    
    # Save to database
    try:
        scan_result = {
            'user_id': st.session_state.user.id,
            'url': url,
            'industry': industry,
            'scan_data': scan_data,
            'technical_analysis': technical_analysis,
            'content_analysis': content_analysis,
            'competitive_analysis': competitive_analysis,
            'action_plan': action_plan,
            'created_at': datetime.now().isoformat()
        }
        
        supabase.table('scans').insert(scan_result).execute()
    except Exception as e:
        st.warning(f"Note: Could not save to database: {str(e)}")
    
    progress_bar.progress(100)
    status.markdown('<div class="ai-thinking">✅ Analysis complete!</div>', unsafe_allow_html=True)
    time.sleep(1)
    status.empty()
    progress_bar.empty()
    
    # Display Results
    st.markdown("---")
    st.markdown("## 📊 Smart Analysis Results")
    
    # Overall Scores
    st.markdown("### 🎯 Overall SEO Health Score")
    col1, col2, col3 = st.columns(3)
    
    tech_score = technical_analysis.get('score', 0)
    content_score = content_analysis.get('score', 0)
    overall_score = (tech_score + content_score) / 2
    
    with col1:
        score_class = "score-excellent" if tech_score >= 80 else "score-good" if tech_score >= 60 else "score-warning" if tech_score >= 40 else "score-poor"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Technical SEO</h4>
            <div class="{score_class}">{tech_score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        score_class = "score-excellent" if content_score >= 80 else "score-good" if content_score >= 60 else "score-warning" if content_score >= 40 else "score-poor"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Content Quality</h4>
            <div class="{score_class}">{content_score}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        score_class = "score-excellent" if overall_score >= 80 else "score-good" if overall_score >= 60 else "score-warning" if overall_score >= 40 else "score-poor"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Overall Score</h4>
            <div class="{score_class}">{int(overall_score)}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Details
    with st.expander("🔧 Technical SEO Analysis", expanded=True):
        st.markdown("#### Critical Issues")
        for issue in technical_analysis.get('critical_issues', []):
            st.error(f"🔴 {issue}")
        
        st.markdown("#### Recommendations")
        for rec in technical_analysis.get('recommendations', [])[:5]:
            priority_emoji = "🔴" if rec.get('priority') == 'High' else "🟡" if rec.get('priority') == 'Medium' else "🟢"
            st.markdown(f"""
            <div class="insight-box">
                <strong>{priority_emoji} {rec.get('priority')} Priority</strong><br/>
                <strong>Issue:</strong> {rec.get('issue')}<br/>
                <strong>Solution:</strong> {rec.get('solution')}<br/>
                <strong>Impact:</strong> {rec.get('impact')}
            </div>
            """, unsafe_allow_html=True)
    
    # Content Analysis
    with st.expander("📝 Content Quality Analysis", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Strengths")
            for strength in content_analysis.get('strengths', []):
                st.success(f"✓ {strength}")
        
        with col2:
            st.markdown("#### ⚠️ Weaknesses")
            for weakness in content_analysis.get('weaknesses', []):
                st.warning(f"• {weakness}")
        
        st.markdown("#### 📈 Content Strategy")
        for strategy in content_analysis.get('content_strategy', []):
            st.info(f"💡 {strategy}")
        
        st.markdown("#### 🔑 Keyword Opportunities")
        keywords = content_analysis.get('keyword_opportunities', [])
        if keywords:
            st.markdown(", ".join([f"`{kw}`" for kw in keywords]))
    
    # Competitive Analysis
    with st.expander("🎯 Competitive Intelligence", expanded=True):
        st.markdown("#### 🏆 Main Competitors")
        for comp in competitive_analysis.get('competitors', []):
            st.markdown(f"• `{comp}`")
        
        st.markdown("#### 💪 Your Competitive Advantages")
        for adv in competitive_analysis.get('competitive_advantages', []):
            st.success(f"✓ {adv}")
        
        st.markdown("#### 🎲 Positioning Strategy")
        st.info(competitive_analysis.get('positioning_strategy', 'Analyzing...'))
        
        st.markdown("#### ⚡ Quick Wins")
        for win in competitive_analysis.get('quick_wins', []):
            st.markdown(f"🚀 {win}")
    
    # 30-Day Action Plan
    with st.expander("📋 30-Day Action Plan", expanded=True):
        st.markdown(f"#### 📈 Estimated Traffic Increase: {action_plan.get('estimated_traffic_increase', 'N/A')}")
        
        st.markdown("### Week 1: Quick Wins")
        for task in action_plan.get('week_1', []):
            impact_color = "🔴" if task.get('impact') == 'High' else "🟡" if task.get('impact') == 'Medium' else "🟢"
            st.markdown(f"{impact_color} **{task.get('task')}** (Effort: {task.get('effort')}/10)")
        
        st.markdown("### Week 2-3: Strategic Improvements")
        for task in action_plan.get('week_2_3', [])[:3]:
            impact_color = "🔴" if task.get('impact') == 'High' else "🟡" if task.get('impact') == 'Medium' else "🟢"
            st.markdown(f"{impact_color} **{task.get('task')}** (Effort: {task.get('effort')}/10)")
        
        st.markdown("### Week 4: Long-term Strategy")
        for task in action_plan.get('week_4', [])[:3]:
            impact_color = "🔴" if task.get('impact') == 'High' else "🟡" if task.get('impact') == 'Medium' else "🟢"
            st.markdown(f"{impact_color} **{task.get('task')}** (Effort: {task.get('effort')}/10)")
        
        st.markdown("### 📊 Success Metrics to Track")
        for metric in action_plan.get('success_metrics', []):
            st.markdown(f"📍 {metric}")
    
    # Export Options
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download PDF Report", use_container_width=True):
            st.info("🚧 PDF generation coming soon!")
    
    with col2:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("🚧 Email feature coming soon!")
    
    with col3:
        # JSON export
        report_json = {
            'scan_data': scan_data,
            'technical_analysis': technical_analysis,
            'content_analysis': content_analysis,
            'competitive_analysis': competitive_analysis,
            'action_plan': action_plan
        }
        st.download_button(
            label="💾 Download JSON",
            data=json.dumps(report_json, indent=2),
            file_name=f"seo_report_{url.replace('https://', '').replace('/', '_')}.json",
            mime="application/json",
            use_container_width=True
        )

# Back button
st.markdown("---")
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")