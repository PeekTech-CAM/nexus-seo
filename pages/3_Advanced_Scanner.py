"""
NEXUS SEO INTELLIGENCE - Advanced AI Scanner
Multi-Agent Analysis with Plan-Based Features
"""

import streamlit as st
import os
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

st.set_page_config(page_title="Advanced AI Scanner", page_icon="🧠", layout="wide")

# Check login
if 'user' not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Get Supabase
try:
    from supabase import create_client
    supabase = create_client(
        st.secrets.get("SUPABASE_URL") or os.getenv('SUPABASE_URL'),
        st.secrets.get("SUPABASE_KEY") or os.getenv('SUPABASE_KEY')
    )
except:
    supabase = None

# Plan Configuration
PLAN_FEATURES = {
    'demo': {
        'name': 'Demo',
        'ai_agents': 1,  # Only basic analysis
        'export_pdf': False,
        'export_json': True,
        'competitors': 0,
        'action_plan_days': 0
    },
    'pro': {
        'name': 'Pro',
        'ai_agents': 2,  # Technical + Content
        'export_pdf': False,
        'export_json': True,
        'competitors': 3,
        'action_plan_days': 30
    },
    'agency': {
        'name': 'Agency',
        'ai_agents': 3,  # Technical + Content + Competitive
        'export_pdf': True,
        'export_json': True,
        'competitors': 5,
        'action_plan_days': 60
    },
    'elite': {
        'name': 'Elite',
        'ai_agents': 4,  # All agents including strategic planning
        'export_pdf': True,
        'export_json': True,
        'competitors': 10,
        'action_plan_days': 90
    }
}

# CSS
st.markdown("""
<style>
    .main { background: #f8fafc; padding: 2rem; }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; padding: 0.75rem 2rem;
        border-radius: 10px; font-weight: 600;
    }
    .score-card {
        background: white; padding: 2rem; border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center;
    }
    .score-excellent { color: #10b981; font-size: 3rem; font-weight: bold; }
    .score-good { color: #3b82f6; font-size: 3rem; font-weight: bold; }
    .score-warning { color: #f59e0b; font-size: 3rem; font-weight: bold; }
    .score-poor { color: #ef4444; font-size: 3rem; font-weight: bold; }
    .locked-feature {
        background: #f3f4f6; padding: 1rem; border-radius: 10px;
        border: 2px dashed #9ca3af; opacity: 0.6;
    }
    .plan-badge {
        display: inline-block; padding: 0.25rem 0.75rem;
        border-radius: 20px; font-weight: bold; font-size: 0.8rem;
    }
    .badge-demo { background: #6b7280; color: white; }
    .badge-pro { background: #3b82f6; color: white; }
    .badge-agency { background: #8b5cf6; color: white; }
    .badge-elite { background: #f59e0b; color: white; }
</style>
""", unsafe_allow_html=True)

# Get current plan
user_plan = st.session_state.get('user_plan', 'demo')
plan_features = PLAN_FEATURES.get(user_plan, PLAN_FEATURES['demo'])
scans_used = st.session_state.get('scans_used', 0)

# Functions
def get_ai():
    try:
        import google.generativeai as genai
        key = st.secrets.get("GEMINI_API_KEY") or os.getenv('GEMINI_API_KEY')
        if key:
            genai.configure(api_key=key.strip())
            return genai.GenerativeModel('gemini-1.5-pro')
    except:
        pass
    return None

def advanced_scrape(url):
    """Advanced website scraping"""
    if not url.startswith('http'):
        url = 'https://' + url
    
    try:
        start = time.time()
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        load_time = int((time.time() - start) * 1000)
        
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Extract comprehensive data
        title = soup.find('title')
        title = title.text.strip() if title else ''
        
        desc = soup.find('meta', attrs={'name': 'description'})
        desc = desc.get('content', '').strip() if desc else ''
        
        text = soup.get_text()
        words = len([w for w in text.split() if len(w) > 2])
        
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        
        links = soup.find_all('a', href=True)
        
        return {
            'url': url,
            'status_code': r.status_code,
            'load_time': load_time,
            'page_size': round(len(r.content) / 1024, 2),
            'title': title,
            'title_length': len(title),
            'description': desc,
            'description_length': len(desc),
            'word_count': words,
            'h1_count': len(h1_tags),
            'h1_texts': [h.get_text().strip() for h in h1_tags][:3],
            'h2_count': len(h2_tags),
            'images_total': len(images),
            'images_without_alt': len(images_without_alt),
            'links_total': len(links),
            'https': url.startswith('https'),
            'mobile_friendly': soup.find('meta', attrs={'name': 'viewport'}) is not None,
            'content_sample': text[:1000]
        }
    except Exception as e:
        st.error(f"Scraping error: {str(e)}")
        return None

def ai_technical_analysis(data, model):
    """AI Agent 1: Technical SEO Expert"""
    try:
        prompt = f"""You are a Technical SEO expert. Analyze:

URL: {data['url']}
Load Time: {data['load_time']}ms
Page Size: {data['page_size']}KB
HTTPS: {data['https']}
Mobile: {data['mobile_friendly']}

Provide JSON:
{{
    "technical_score": 85,
    "critical_issues": [{{"issue": "...", "severity": "high", "fix": "...", "impact": "..."}}],
    "recommendations": [{{"priority": "High", "action": "...", "implementation": "...", "result": "..."}}]
}}"""

        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except Exception as e:
        return {"technical_score": 0, "critical_issues": [], "recommendations": []}

def ai_content_analysis(data, model):
    """AI Agent 2: Content Strategy Expert"""
    try:
        prompt = f"""You are a Content SEO expert. Analyze:

Title: {data['title']} ({data['title_length']} chars)
Description: {data['description']} ({data['description_length']} chars)
Word Count: {data['word_count']}
H1: {data['h1_count']}, H2: {data['h2_count']}
Content: {data['content_sample'][:500]}

Provide JSON:
{{
    "content_score": 75,
    "keyword_opportunities": ["keyword1", "keyword2", "keyword3"],
    "content_gaps": ["gap1", "gap2"],
    "readability": "Good",
    "improvements": [{{"priority": "High", "action": "...", "why": "...", "how": "..."}}]
}}"""

        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except Exception as e:
        return {"content_score": 0, "keyword_opportunities": [], "content_gaps": [], "improvements": []}

def ai_competitive_analysis(data, model, num_competitors):
    """AI Agent 3: Competitive Intelligence (Agency+)"""
    try:
        prompt = f"""You are a competitive analyst. Based on:

URL: {data['url']}
Title: {data['title']}
Content: {data['content_sample'][:300]}

Provide JSON with top {num_competitors} competitors:
{{
    "competitive_score": 70,
    "main_competitors": ["comp1.com", "comp2.com", "comp3.com"],
    "competitive_advantages": ["advantage1", "advantage2"],
    "market_opportunities": ["opportunity1", "opportunity2"],
    "quick_wins": ["win1", "win2", "win3"]
}}"""

        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except Exception as e:
        return {"competitive_score": 0, "main_competitors": [], "competitive_advantages": [], "quick_wins": []}

def ai_strategic_plan(data, tech, content, comp, days):
    """AI Agent 4: Strategic Planner (Elite only)"""
    try:
        model = get_ai()
        if not model:
            return {}
        
        prompt = f"""Create a {days}-day action plan based on:

Technical Score: {tech.get('technical_score', 0)}
Content Score: {content.get('content_score', 0)}
Competitive Score: {comp.get('competitive_score', 0)}

Provide {days}-day plan as JSON:
{{
    "overall_strategy": "...",
    "estimated_improvement": "20-30%",
    "phase_1": [{{"task": "...", "effort": 5, "impact": "High", "timeline": "Week 1-2"}}],
    "phase_2": [{{"task": "...", "effort": 7, "impact": "Medium", "timeline": "Week 3-4"}}],
    "success_metrics": ["metric1", "metric2"]
}}"""

        response = model.generate_content(prompt)
        return json.loads(response.text.replace('```json', '').replace('```', '').strip())
    except Exception as e:
        return {}

# UI Header
st.title("🧠 Advanced AI-Powered Scanner")

# Plan info
plan_name = plan_features['name']
badge_class = f"badge-{user_plan}"
st.markdown(f'<span class="plan-badge {badge_class}">{plan_name} Plan</span> - **{plan_features["ai_agents"]} AI Agent{"s" if plan_features["ai_agents"] > 1 else ""}**', unsafe_allow_html=True)

st.markdown("---")

# Scan form
with st.form("scan_form"):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input("🌐 Website URL", placeholder="https://example.com")
    
    with col2:
        industry = st.selectbox("Industry", ["E-commerce", "SaaS", "Blog", "Local Business", "Other"])
    
    submit = st.form_submit_button("🚀 Start Advanced Analysis", use_container_width=True, type="primary")

if submit and url:
    model = get_ai()
    
    if not model:
        st.error("🔴 AI Engine not configured. Add GEMINI_API_KEY to secrets.")
        st.stop()
    
    # Progress
    progress = st.progress(0)
    status = st.empty()
    
    # Phase 1: Scrape
    status.markdown("### 🔍 Phase 1: Deep Website Analysis")
    progress.progress(20)
    
    with st.spinner("Extracting website data..."):
        data = advanced_scrape(url)
    
    if not data:
        st.stop()
    
    progress.progress(30)
    st.success("✅ Data extracted!")
    
    # Update scan count
    st.session_state.scans_used = scans_used + 1
    
    # Save to database
    if supabase and st.session_state.user.id != 'demo_user':
        try:
            supabase.table('scans').insert({
                'user_id': st.session_state.user.id,
                'url': url,
                'scan_data': data,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            supabase.table('profiles').update({
                'monthly_scans_used': scans_used + 1
            }).eq('id', st.session_state.user.id).execute()
        except:
            pass
    
    # Phase 2: AI Analysis
    status.markdown("### 🧠 Phase 2: Multi-Agent AI Analysis")
    
    # Agent 1: Technical (All plans)
    status.markdown("🤖 **Agent 1:** Technical SEO Expert analyzing...")
    progress.progress(40)
    tech_analysis = ai_technical_analysis(data, model)
    
    # Agent 2: Content (Pro+)
    if plan_features['ai_agents'] >= 2:
        status.markdown("📝 **Agent 2:** Content Strategy Expert analyzing...")
        progress.progress(55)
        content_analysis = ai_content_analysis(data, model)
    else:
        content_analysis = {"content_score": 0}
        st.info("🔒 Content analysis requires Pro plan or higher")
    
    # Agent 3: Competitive (Agency+)
    if plan_features['ai_agents'] >= 3:
        status.markdown("🎯 **Agent 3:** Competitive Intelligence analyzing...")
        progress.progress(70)
        comp_analysis = ai_competitive_analysis(data, model, plan_features['competitors'])
    else:
        comp_analysis = {"competitive_score": 0}
        st.info("🔒 Competitive analysis requires Agency plan or higher")
    
    # Agent 4: Strategic (Elite only)
    if plan_features['ai_agents'] >= 4 and plan_features['action_plan_days'] > 0:
        status.markdown("📋 **Agent 4:** Strategic Planner creating action plan...")
        progress.progress(85)
        strategic_plan = ai_strategic_plan(data, tech_analysis, content_analysis, comp_analysis, plan_features['action_plan_days'])
    else:
        strategic_plan = {}
        if user_plan != 'elite':
            st.info(f"🔒 {plan_features['action_plan_days'] or 90}-day strategic planning requires Elite plan")
    
    progress.progress(100)
    status.empty()
    progress.empty()
    
    st.success("✅ Advanced analysis complete!")
    time.sleep(0.5)
    
    # RESULTS
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Scores
    cols = st.columns(plan_features['ai_agents'] + 1)
    
    scores = [
        ("Technical", tech_analysis.get('technical_score', 0)),
        ("Content", content_analysis.get('content_score', 0)),
        ("Competitive", comp_analysis.get('competitive_score', 0))
    ]
    
    overall = sum([s[1] for s in scores if s[1] > 0]) / len([s for s in scores if s[1] > 0]) if any(s[1] > 0 for s in scores) else 0
    
    for i, (label, score) in enumerate(scores[:plan_features['ai_agents']]):
        with cols[i]:
            score_class = "score-excellent" if score >= 80 else "score-good" if score >= 60 else "score-warning" if score >= 40 else "score-poor"
            st.markdown(f'<div class="score-card"><h4>{label}</h4><div class="{score_class}">{score}</div></div>', unsafe_allow_html=True)
    
    with cols[plan_features['ai_agents']]:
        score_class = "score-excellent" if overall >= 80 else "score-good" if overall >= 60 else "score-warning" if overall >= 40 else "score-poor"
        st.markdown(f'<div class="score-card"><h4>Overall</h4><div class="{score_class}">{int(overall)}</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Technical Analysis
    with st.expander("🔧 Technical SEO Analysis", expanded=True):
        for issue in tech_analysis.get('critical_issues', [])[:5]:
            severity = issue.get('severity', 'medium')
            emoji = "🔴" if severity == 'high' else "🟡"
            st.error(f"{emoji} **{issue.get('issue')}**")
            st.markdown(f"**Fix:** {issue.get('fix')}")
            st.markdown(f"**Impact:** {issue.get('impact')}")
            st.markdown("---")
        
        st.markdown("#### Recommendations")
        for rec in tech_analysis.get('recommendations', [])[:3]:
            st.info(f"**{rec.get('action')}**\n\n{rec.get('implementation')}")
    
    # Content Analysis
    if plan_features['ai_agents'] >= 2:
        with st.expander("📝 Content Strategy Analysis", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔑 Keyword Opportunities")
                for kw in content_analysis.get('keyword_opportunities', []):
                    st.code(kw)
            
            with col2:
                st.markdown("#### 📈 Content Gaps")
                for gap in content_analysis.get('content_gaps', []):
                    st.warning(gap)
            
            st.markdown(f"**Readability:** {content_analysis.get('readability', 'N/A')}")
    
    # Competitive Analysis
    if plan_features['ai_agents'] >= 3:
        with st.expander("🎯 Competitive Intelligence", expanded=True):
            st.markdown("#### 🏆 Main Competitors")
            for comp in comp_analysis.get('main_competitors', []):
                st.markdown(f"• `{comp}`")
            
            st.markdown("#### ⚡ Quick Wins")
            for win in comp_analysis.get('quick_wins', []):
                st.success(f"✓ {win}")
    
    # Strategic Plan
    if strategic_plan:
        with st.expander(f"📋 {plan_features['action_plan_days']}-Day Action Plan", expanded=True):
            st.markdown(f"**Strategy:** {strategic_plan.get('overall_strategy', 'N/A')}")
            st.success(f"📈 **Expected Improvement:** {strategic_plan.get('estimated_improvement', 'N/A')}")
            
            st.markdown("### Phase 1")
            for task in strategic_plan.get('phase_1', [])[:3]:
                st.markdown(f"**{task.get('task')}**")
                st.markdown(f"Effort: {task.get('effort')}/10 | Impact: {task.get('impact')}")
    
    # Export
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    report = {
        'scan_data': data,
        'technical_analysis': tech_analysis,
        'content_analysis': content_analysis if plan_features['ai_agents'] >= 2 else {},
        'competitive_analysis': comp_analysis if plan_features['ai_agents'] >= 3 else {},
        'strategic_plan': strategic_plan if plan_features['ai_agents'] >= 4 else {},
        'timestamp': datetime.now().isoformat()
    }
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if plan_features['export_json']:
            st.download_button(
                "💾 Download JSON",
                json.dumps(report, indent=2),
                file_name=f"advanced_report_{urlparse(url).netloc}.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.markdown('<div class="locked-feature">🔒 JSON export requires Pro+</div>', unsafe_allow_html=True)
    
    with col2:
        if plan_features['export_pdf']:
            if st.button("📄 Generate PDF", use_container_width=True):
                st.info("PDF generation coming soon!")
        else:
            st.markdown('<div class="locked-feature">🔒 PDF export requires Agency+</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email delivery coming soon!")

# Back
st.markdown("---")
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")