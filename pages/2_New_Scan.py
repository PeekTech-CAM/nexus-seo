"""
NEXUS SEO INTELLIGENCE - Smart SEO Scanner Page
FIXED VERSION - No more API key errors!
"""

import streamlit as st
import os
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Page config
st.set_page_config(
    page_title="Smart SEO Scanner",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .metric-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .score-excellent { color: #10b981; font-size: 2rem; font-weight: bold; }
    .score-good { color: #3b82f6; font-size: 2rem; font-weight: bold; }
    .score-warning { color: #f59e0b; font-size: 2rem; font-weight: bold; }
    .score-poor { color: #ef4444; font-size: 2rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Check login
if 'user' not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Initialize Gemini ONLY when needed (lazy loading)
def get_gemini_model():
    """Get Gemini model with proper error handling"""
    try:
        import google.generativeai as genai
        
        # Try to get API key from multiple sources
        api_key = None
        
        # Method 1: Direct from secrets
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except:
            pass
        
        # Method 2: From secrets dict
        if not api_key:
            try:
                api_key = st.secrets.get("GEMINI_API_KEY")
            except:
                pass
        
        # Method 3: Environment variable
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
        
        # Validate and configure
        if api_key and len(api_key) > 20:
            genai.configure(api_key=api_key.strip())
            return genai.GenerativeModel('gemini-1.5-pro')
        
        return None
    except Exception as e:
        st.error(f"Gemini initialization error: {str(e)}")
        return None

# Scraping function
def scrape_website(url):
    """Scrape website and extract SEO data"""
    try:
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
        title = soup.find('title')
        title = title.text.strip() if title else ''
        
        description = ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '').strip()
        
        text_content = soup.get_text()
        word_count = len([w for w in text_content.split() if len(w) > 2])
        
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        links = soup.find_all('a', href=True)
        
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        mobile_friendly = viewport is not None
        
        page_size = len(response.content) / 1024
        https_enabled = url.startswith('https')
        
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
            'images_total': len(images),
            'images_without_alt': len(images_without_alt),
            'links_total': len(links),
            'mobile_friendly': mobile_friendly,
            'content_sample': text_content[:500]
        }
    except Exception as e:
        st.error(f"Error scraping website: {str(e)}")
        return None

# Analysis functions
def analyze_technical(data):
    """Basic technical SEO analysis"""
    issues = []
    warnings = []
    score = 100
    
    if not data['https']:
        issues.append("🔴 Not using HTTPS - Critical security issue")
        score -= 15
    
    if data['load_time'] > 3000:
        issues.append(f"🔴 Slow load time ({data['load_time']}ms)")
        score -= 10
    elif data['load_time'] > 1500:
        warnings.append(f"🟡 Load time could be improved ({data['load_time']}ms)")
        score -= 5
    
    if not data['mobile_friendly']:
        issues.append("🔴 Not mobile-friendly")
        score -= 15
    
    if data['images_without_alt'] > 0:
        warnings.append(f"🟡 {data['images_without_alt']} images missing alt text")
        score -= 5
    
    return {'score': max(0, score), 'issues': issues, 'warnings': warnings}

def analyze_content(data):
    """Basic content analysis"""
    issues = []
    warnings = []
    score = 100
    
    if not data['title']:
        issues.append("🔴 Missing page title")
        score -= 20
    elif data['title_length'] < 30 or data['title_length'] > 70:
        warnings.append(f"🟡 Title length not optimal ({data['title_length']} chars)")
        score -= 5
    
    if not data['description']:
        issues.append("🔴 Missing meta description")
        score -= 15
    
    if data['h1_count'] == 0:
        issues.append("🔴 Missing H1 tag")
        score -= 15
    elif data['h1_count'] > 1:
        warnings.append(f"🟡 Multiple H1 tags ({data['h1_count']})")
        score -= 5
    
    if data['word_count'] < 300:
        warnings.append(f"🟡 Thin content ({data['word_count']} words)")
        score -= 10
    
    return {'score': max(0, score), 'issues': issues, 'warnings': warnings}

def ai_analysis(data, model):
    """AI-powered analysis"""
    if not model:
        return None
    
    try:
        prompt = f"""Analyze this website for SEO:

URL: {data['url']}
Title: {data['title']}
Description: {data['description']}
Word Count: {data['word_count']}
Load Time: {data['load_time']}ms

Provide 5 specific, actionable recommendations to improve SEO. Be concise and prioritize by impact.

Format as JSON:
{{
    "recommendations": [
        {{"priority": "High", "action": "...", "impact": "..."}}
    ],
    "quick_wins": ["...", "..."],
    "estimated_improvement": "..."
}}"""
        
        response = model.generate_content(prompt)
        result = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(result)
    except Exception as e:
        st.warning(f"AI analysis failed: {str(e)}")
        return None

# Main UI
st.title("🧠 Smart SEO Scanner")
st.markdown("### AI-Powered Website Analysis")
st.markdown("---")

# Scan form
with st.form("scan_form"):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input("🌐 Website URL", placeholder="example.com or https://example.com")
    
    with col2:
        use_ai = st.checkbox("🤖 Enable AI Analysis", value=True, help="Uses Gemini AI for advanced insights")
    
    submit = st.form_submit_button("🚀 Start Analysis", use_container_width=True)

if submit and url:
    # Step 1: Scrape website
    with st.spinner("🔍 Scanning website..."):
        scan_data = scrape_website(url)
    
    if not scan_data:
        st.error("Failed to scan website. Please check the URL and try again.")
        st.stop()
    
    st.success("✅ Website scanned successfully!")
    
    # Step 2: Basic analysis
    with st.spinner("📊 Analyzing SEO..."):
        technical = analyze_technical(scan_data)
        content = analyze_content(scan_data)
    
    # Step 3: AI analysis (if enabled)
    ai_result = None
    if use_ai:
        with st.spinner("🧠 Running AI analysis..."):
            model = get_gemini_model()
            
            if model:
                ai_result = ai_analysis(scan_data, model)
                if ai_result:
                    st.success("✅ AI analysis complete!")
            else:
                st.warning("⚠️ AI analysis skipped - API key not configured")
                st.info("Add GEMINI_API_KEY to Streamlit secrets to enable AI features")
    
    # Display Results
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Scores
    col1, col2, col3 = st.columns(3)
    
    overall_score = (technical['score'] + content['score']) / 2
    
    with col1:
        score_class = "score-excellent" if technical['score'] >= 80 else "score-good" if technical['score'] >= 60 else "score-warning" if technical['score'] >= 40 else "score-poor"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Technical SEO</h4>
            <div class="{score_class}">{technical['score']}/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        score_class = "score-excellent" if content['score'] >= 80 else "score-good" if content['score'] >= 60 else "score-warning" if content['score'] >= 40 else "score-poor"
        st.markdown(f"""
        <div class="metric-card">
            <h4>Content Quality</h4>
            <div class="{score_class}">{content['score']}/100</div>
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
    
    # Technical Issues
    with st.expander("🔧 Technical SEO", expanded=True):
        if technical['issues']:
            st.markdown("#### Critical Issues")
            for issue in technical['issues']:
                st.error(issue)
        
        if technical['warnings']:
            st.markdown("#### Warnings")
            for warning in technical['warnings']:
                st.warning(warning)
        
        if not technical['issues'] and not technical['warnings']:
            st.success("✅ No technical issues found!")
    
    # Content Issues
    with st.expander("📝 Content Analysis", expanded=True):
        if content['issues']:
            st.markdown("#### Critical Issues")
            for issue in content['issues']:
                st.error(issue)
        
        if content['warnings']:
            st.markdown("#### Warnings")
            for warning in content['warnings']:
                st.warning(warning)
        
        if not content['issues'] and not content['warnings']:
            st.success("✅ Content is well-optimized!")
    
    # AI Insights
    if ai_result:
        with st.expander("🤖 AI-Powered Insights", expanded=True):
            st.markdown("#### 🎯 Priority Recommendations")
            for rec in ai_result.get('recommendations', [])[:5]:
                priority = rec.get('priority', 'Medium')
                emoji = "🔴" if priority == "High" else "🟡" if priority == "Medium" else "🟢"
                st.markdown(f"""
                **{emoji} {priority} Priority**  
                **Action:** {rec.get('action')}  
                **Impact:** {rec.get('impact')}
                """)
                st.markdown("---")
            
            if ai_result.get('quick_wins'):
                st.markdown("#### ⚡ Quick Wins")
                for win in ai_result['quick_wins']:
                    st.success(f"✓ {win}")
            
            if ai_result.get('estimated_improvement'):
                st.info(f"📈 **Estimated Improvement:** {ai_result['estimated_improvement']}")
    
    # Basic Stats
    with st.expander("📊 Detailed Metrics"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Load Time", f"{scan_data['load_time']}ms")
            st.metric("Page Size", f"{scan_data['page_size']}KB")
            st.metric("Word Count", scan_data['word_count'])
            st.metric("Images", scan_data['images_total'])
        
        with col2:
            st.metric("Links", scan_data['links_total'])
            st.metric("H1 Tags", scan_data['h1_count'])
            st.metric("H2 Tags", scan_data['h2_count'])
            st.metric("HTTPS", "✅" if scan_data['https'] else "❌")
    
    # Export
    st.markdown("---")
    report_data = {
        'scan_data': scan_data,
        'technical_analysis': technical,
        'content_analysis': content,
        'ai_insights': ai_result,
        'timestamp': datetime.now().isoformat()
    }
    
    st.download_button(
        label="💾 Download Full Report (JSON)",
        data=json.dumps(report_data, indent=2),
        file_name=f"seo_report_{url.replace('https://', '').replace('/', '_')}.json",
        mime="application/json"
    )

# Back button
st.markdown("---")
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")