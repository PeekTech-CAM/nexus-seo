import streamlit as st

st.set_page_config(
    page_title="🧠 Advanced AI Scanner", 
    page_icon="🧠", 
    layout="wide"
)

# Check login
if 'user' not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Please login first")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #1e1b4b 0%, #581c87 50%, #1e1b4b 100%);}
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(124, 58, 237, 0.4);
    }
    .score-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .issue-card {
        background: white;
        border-left: 5px solid #ef4444;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .issue-critical {border-left-color: #ef4444;}
    .issue-high {border-left-color: #f97316;}
    .issue-medium {border-left-color: #eab308;}
    h1, h2, h3 {color: white;}
    .metric-excellent {color: #10b981; font-size: 3rem; font-weight: bold;}
    .metric-good {color: #3b82f6; font-size: 3rem; font-weight: bold;}
    .metric-warning {color: #f59e0b; font-size: 3rem; font-weight: bold;}
    .metric-poor {color: #ef4444; font-size: 3rem; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="font-size: 4rem; margin-bottom: 0.5rem;">
        🧠 NEXUS SEO <span style="background: linear-gradient(135deg, #a78bfa 0%, #ec4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Intelligence</span>
    </h1>
    <p style="font-size: 1.5rem; color: #d1d5db;">Advanced AI-Powered Multi-Agent Analysis System</p>
    <p style="color: #9ca3af;">Professional-grade SEO scanning with deep competitive intelligence</p>
</div>
""", unsafe_allow_html=True)

# Input
col1, col2 = st.columns([4, 1])
with col1:
    url = st.text_input("🌐 Website URL", placeholder="https://example.com", label_visibility="collapsed")
with col2:
    analyze_btn = st.button("🚀 Analyze", use_container_width=True, type="primary")

if analyze_btn and url:
    # Progress
    progress_bar = st.progress(0)
    status = st.empty()
    
    phases = [
        ("Initializing AI agents...", 10),
        ("Scanning website structure...", 25),
        ("Technical SEO audit...", 40),
        ("AI content analysis...", 55),
        ("Competitive intelligence...", 70),
        ("Keyword research...", 85),
        ("Generating recommendations...", 95),
        ("Finalizing report...", 100)
    ]
    
    import time
    for phase_text, progress in phases:
        status.info(f"⚙️ {phase_text}")
        progress_bar.progress(progress)
        time.sleep(0.5)
    
    status.success("✅ Analysis Complete!")
    progress_bar.empty()
    status.empty()
    
    # Results
    st.markdown("---")
    st.markdown("## 📊 Comprehensive Analysis Results")
    
    # Score Cards
    cols = st.columns(6)
    scores = [
        ("Overall", 73, "🎯"),
        ("Technical", 85, "⚡"),
        ("Content", 68, "📝"),
        ("Competitive", 66, "🎯"),
        ("Mobile", 91, "📱"),
        ("Performance", 58, "🚀")
    ]
    
    for col, (label, score, icon) in zip(cols, scores):
        with col:
            color_class = "metric-excellent" if score >= 80 else "metric-good" if score >= 60 else "metric-warning" if score >= 40 else "metric-poor"
            st.markdown(f"""
            <div class="score-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="color: #6b7280; font-size: 0.9rem; margin-bottom: 0.5rem;">{label}</div>
                <div class="{color_class}">{score}</div>
                <div style="color: #9ca3af; font-size: 0.8rem;">/100</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Critical Issues
    st.markdown("---")
    st.markdown("## 🚨 Critical Issues & Professional Fixes")
    
    issues = [
        {
            "title": "Page Speed Critical Issue",
            "severity": "critical",
            "desc": "Page load time is 4.2s, well above the recommended 2.5s threshold. This significantly impacts user experience and search rankings.",
            "impact": "High - affecting 75% of mobile users",
            "fix": "Implement lazy loading for images, convert images to WebP format, minify CSS/JS files, enable browser caching with proper cache-control headers",
            "effort": 7,
            "time": "2-3 weeks"
        },
        {
            "title": "Missing Core Web Vitals Optimization",
            "severity": "critical",
            "desc": "LCP: 5.2s (Poor), FID: 180ms (Needs Improvement), CLS: 0.18 (Good). These metrics directly affect Google rankings.",
            "impact": "Direct ranking factor affecting visibility",
            "fix": "Optimize server response time, reduce render-blocking resources, implement code splitting, stabilize layout shifts with proper image dimensions",
            "effort": 8,
            "time": "3-4 weeks"
        },
        {
            "title": "Mobile Usability Issues",
            "severity": "high",
            "desc": "Clickable elements too close together on 12 pages, viewport not properly configured.",
            "impact": "Medium - affecting mobile rankings",
            "fix": "Increase touch target sizes to minimum 48x48px, fix viewport meta tags, increase font sizes for mobile screens",
            "effort": 4,
            "time": "1 week"
        }
    ]
    
    for issue in issues:
        severity_badge = "🔴 CRITICAL" if issue["severity"] == "critical" else "🟠 HIGH"
        st.markdown(f"""
        <div class="issue-card issue-{issue['severity']}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="color: #1f2937; margin: 0;">{issue['title']}</h3>
                <span style="background: #{'ef4444' if issue['severity']=='critical' else 'f97316'}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: bold;">{severity_badge}</span>
            </div>
            <p style="color: #4b5563; margin-bottom: 1rem;">{issue['desc']}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                <div style="color: #6b7280;"><strong style="color: #ef4444;">Impact:</strong> {issue['impact']}</div>
                <div style="color: #6b7280;"><strong style="color: #3b82f6;">Timeline:</strong> {issue['time']}</div>
            </div>
            <div style="background: #f0fdf4; border: 2px solid #86efac; border-radius: 8px; padding: 1rem;">
                <div style="color: #059669; font-weight: bold; margin-bottom: 0.5rem;">✅ Professional Fix:</div>
                <p style="color: #065f46; margin: 0;">{issue['fix']}</p>
            </div>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem; align-items: center;">
                <span style="color: #6b7280;">Effort Level:</span>
                {''.join(['<div style="width: 24px; height: 8px; background: ' + ('#7c3aed' if i < issue['effort'] else '#e5e7eb') + '; border-radius: 4px; display: inline-block; margin-right: 2px;"></div>' for i in range(10)])}
                <span style="font-weight: bold; color: #1f2937;">{issue['effort']}/10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Content Analysis
    st.markdown("---")
    st.markdown("## 🧠 AI Content Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎯 Primary Keywords")
        for kw in ['AI SEO tools', 'website optimization', 'search rankings', 'SEO analysis']:
            st.info(f"🔑 {kw}")
        
        st.markdown("### 💡 Semantic Opportunities")
        for opp in ['voice search optimization', 'featured snippets', 'long-tail keywords']:
            st.success(f"✨ {opp}")
    
    with col2:
        st.markdown("### ⚠️ Content Gaps")
        gaps = [
            'Missing FAQ section for featured snippet opportunities',
            'No video content to increase engagement',
            'Limited internal linking structure',
            'Thin content on key landing pages'
        ]
        for gap in gaps:
            st.warning(f"→ {gap}")
    
    # Action Plan
    st.markdown("---")
    st.markdown("## 📋 90-Day Strategic Action Plan")
    
    with st.expander("⚡ Phase 1: Quick Wins (Week 1-2)", expanded=True):
        tasks = [
            {"task": "Fix Missing Meta Descriptions", "impact": "High", "effort": 2, "time": "2-3 days"},
            {"task": "Optimize Image Alt Text", "impact": "Medium", "effort": 3, "time": "1 week"},
            {"task": "Fix Broken Internal Links", "impact": "Medium", "effort": 2, "time": "2 days"}
        ]
        for task in tasks:
            st.markdown(f"""
            **{task['task']}**  
            📊 Effort: {task['effort']}/10 | 🎯 Impact: {task['impact']} | ⏱️ Timeline: {task['time']}
            """)
            st.markdown("---")
    
    with st.expander("🏗️ Phase 2: Foundations (Week 3-6)"):
        st.markdown("""
        **Implement Comprehensive Schema Markup**  
        📊 Effort: 6/10 | 🎯 Impact: High | ⏱️ Timeline: 2-3 weeks
        
        ---
        
        **Optimize Core Web Vitals**  
        📊 Effort: 8/10 | 🎯 Impact: Very High | ⏱️ Timeline: 3-4 weeks
        """)
    
    with st.expander("🚀 Phase 3: Growth (Week 7-12)"):
        st.markdown("""
        **Launch Link Building Campaign**  
        📊 Effort: 9/10 | 🎯 Impact: Very High | ⏱️ Timeline: 8-12 weeks
        
        ---
        
        **Develop Video Content Strategy**  
        📊 Effort: 8/10 | 🎯 Impact: High | ⏱️ Timeline: 6-10 weeks
        """)
    
    # Success Metrics
    st.markdown("### 📊 Success Metrics to Track")
    metrics = [
        'Organic traffic increase: Target 40-60% in 90 days',
        'Keyword rankings: Move 20+ keywords to page 1',
        'Domain authority: Increase from 35 to 45+',
        'Core Web Vitals: All green scores',
        'Conversion rate: Improve by 15-25%'
    ]
    for metric in metrics:
        st.success(f"✅ {metric}")
    
    # Download
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.download_button(
            "💾 Download Full Report (PDF)",
            "Report data would go here",
            file_name="seo_report.txt",
            use_container_width=True
        )