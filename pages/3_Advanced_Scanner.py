import streamlit as st
import time
from datetime import datetime
from fpdf import FPDF
import io
import base64

# Page config
st.set_page_config(
    page_title="AI SEO Scanner - Nexus Intelligence",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS (same as before)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    .issue-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .critical { border-left-color: #ef4444; }
    .warning { border-left-color: #f59e0b; }
    .info { border-left-color: #3b82f6; }
    .solution-box {
        background: #f0fdf4;
        padding: 1.2rem;
        border-radius: 10px;
        border: 2px solid #86efac;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# PDF Generation Function
def generate_pdf_report(results):
    """Generate PDF report from scan results"""
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font('Arial', 'B', 24)
        pdf.cell(0, 20, 'SEO Intelligence Report', ln=True, align='C')
        
        # Metadata
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"URL: {results['url']}", ln=True)
        pdf.cell(0, 10, f"Scan Date: {results['timestamp']}", ln=True)
        pdf.ln(10)
        
        # Score
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, f"SEO Health Score: {results['score']}/100", ln=True)
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, f"Improvement: +{results['score'] - results['previous_score']} points", ln=True)
        pdf.ln(10)
        
        # Issues Summary
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Issues Found:', ln=True)
        pdf.set_font('Arial', '', 12)
        
        for issue in results['issues']:
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 10, f"{issue['severity'].upper()}: {issue['title']}")
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 8, f"Impact: {issue['impact']}")
            
            if 'steps' in issue:
                pdf.multi_cell(0, 8, "Implementation Steps:")
                for i, step in enumerate(issue['steps'], 1):
                    pdf.multi_cell(0, 6, f"  {i}. {step}")
        
        # Generate PDF bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        return pdf_bytes
    except Exception as e:
        st.error(f"PDF generation error: {str(e)}")
        return None

# Download button helper
def create_download_link(pdf_bytes, filename):
    """Create a download link for PDF"""
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}" class="download-button">📥 Download PDF Report</a>'

# Initialize session state
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'scan_url' not in st.session_state:
    st.session_state.scan_url = ""
if 'selected_solutions' not in st.session_state:
    st.session_state.selected_solutions = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 AI-Powered SEO Intelligence Scanner</h1>
    <p style="font-size: 1.2rem; margin-top: 0.5rem;">
        Advanced analysis with automated solutions and actionable insights
    </p>
</div>
""", unsafe_allow_html=True)

# Scanner Section
if st.session_state.scan_results is None:
    col1, col2 = st.columns([4, 1])
    
    with col1:
        url = st.text_input(
            "Website URL",
            placeholder="https://example.com",
            value=st.session_state.scan_url,
            label_visibility="collapsed"
        )
    
    with col2:
        scan_btn = st.button("🚀 Analyze", use_container_width=True, type="primary")
    
    # Feature highlights
    st.markdown("### ✨ What You'll Get")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("⚡ **Instant AI Fixes** - One-click implementation")
    with col2:
        st.info("🧠 **Smart Analysis** - Deep learning insights")
    with col3:
        st.info("📈 **Growth Tracking** - Monitor improvements")
    
    # Run analysis
    if scan_btn and url:
        st.session_state.scan_url = url
        
        with st.spinner("🤖 AI is analyzing your website..."):
            progress_bar = st.progress(0)
            status = st.empty()
            
            stages = [
                "🔍 Crawling website structure...",
                "📝 Analyzing meta tags and content...",
                "⚡ Checking page speed and performance...",
                "🔧 Scanning for technical SEO issues...",
                "🎯 Identifying keyword opportunities...",
                "✨ Generating AI-powered solutions..."
            ]
            
            for i, stage in enumerate(stages):
                status.info(stage)
                progress_bar.progress((i + 1) / len(stages))
                time.sleep(0.5)
            
            # Generate results (same mock data as before)
            st.session_state.scan_results = {
                "url": url,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "score": 68,
                "previous_score": 52,
                "issues_found": 5,
                "issues": [
                    {
                        "id": 1,
                        "severity": "critical",
                        "category": "Meta Tags",
                        "title": "Missing Meta Description",
                        "impact": "High - Reduces click-through rates by up to 40%",
                        "pages_affected": 12,
                        "explanation": "Meta descriptions are crucial for search visibility and user engagement.",
                        "solutions": [
                            "Discover premium organic coffee beans sourced directly from sustainable farms. Free shipping on orders over $50. Shop now!",
                            "Award-winning specialty coffee roasted fresh daily. 100% organic beans from ethical farms worldwide.",
                            "Transform your morning with artisan coffee beans. Ethically sourced, expertly roasted."
                        ],
                        "code": '''<meta name="description" content="Your optimized description">''',
                        "steps": [
                            "AI analyzes your page content and target audience",
                            "Generates 3 unique descriptions (150-160 characters)",
                            "Includes target keywords naturally",
                            "Adds compelling call-to-action"
                        ]
                    },
                    {
                        "id": 2,
                        "severity": "critical",
                        "category": "Performance",
                        "title": "Slow Page Load Speed (4.2s)",
                        "impact": "Critical - 53% of users abandon sites loading over 3 seconds",
                        "current_state": "First Contentful Paint: 4.2s (Target: <1.8s)",
                        "explanation": "Page speed directly impacts SEO rankings and user experience.",
                        "automated_fixes": [
                            {"action": "Compress 47 images", "savings": "2.3MB → 340KB", "impact": "-1.8s load time"},
                            {"action": "Enable Brotli compression", "savings": "890KB → 156KB", "impact": "-0.6s load time"},
                            {"action": "Defer non-critical CSS", "savings": "Block: 380ms → 45ms", "impact": "-0.4s load time"}
                        ],
                        "steps": [
                            "Automatically compress and convert images to WebP",
                            "Implement lazy loading for below-fold content",
                            "Minify and bundle CSS, JS files"
                        ]
                    },
                    {
                        "id": 3,
                        "severity": "warning",
                        "category": "Content",
                        "title": "Thin Content on Key Pages",
                        "impact": "Medium - Reduces topical authority",
                        "current_state": "Average: 287 words (Recommended: 1,200+)",
                        "explanation": "Comprehensive content signals expertise and provides value.",
                        "steps": [
                            "AI analyzes top-ranking competitor content",
                            "Identifies content gaps and missing topics",
                            "Generates SEO-optimized expansions"
                        ]
                    },
                    {
                        "id": 4,
                        "severity": "warning",
                        "category": "Technical",
                        "title": "Missing Schema Markup",
                        "impact": "Medium - Missing rich snippets opportunities",
                        "current_state": "No structured data detected",
                        "explanation": "Schema markup helps search engines understand your content.",
                        "code": '''<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Your Product",
  "offers": {
    "@type": "Offer",
    "price": "24.99"
  }
}
</script>''',
                        "steps": [
                            "AI identifies page type automatically",
                            "Generates appropriate JSON-LD schema",
                            "Validates against Google requirements"
                        ]
                    },
                    {
                        "id": 5,
                        "severity": "info",
                        "category": "Keywords",
                        "title": "147 Keyword Opportunities Detected",
                        "impact": "High Potential - Untapped ranking opportunities",
                        "current_state": "Ranking for 23 keywords",
                        "explanation": "AI identified high-value keywords where you can rank easily.",
                        "opportunities": [
                            {"keyword": "organic coffee beans online", "volume": "14.8K/mo", "difficulty": "Medium", "potential": 3},
                            {"keyword": "best coffee subscription", "volume": "8.1K/mo", "difficulty": "Low", "potential": 8},
                            {"keyword": "fair trade coffee", "volume": "6.2K/mo", "difficulty": "Low", "potential": 5}
                        ],
                        "steps": [
                            "AI integrates keywords naturally into content",
                            "Generates new content briefs",
                            "Optimizes existing pages"
                        ]
                    }
                ]
            }
            
            status.empty()
            progress_bar.empty()
            st.success("✅ Analysis complete!")
            st.rerun()

# Results Section
else:
    results = st.session_state.scan_results
    
    # Score card with metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h1 style="font-size: 3rem; margin: 0;">{results['score']}</h1>
            <p style="margin: 0.5rem 0;">SEO Score</p>
            <p style="opacity: 0.8;">↗ +{results['score'] - results['previous_score']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Pages Analyzed", "47", delta="12")
    
    with col3:
        st.metric("Keywords", "23", delta="5")
    
    with col4:
        st.metric("Opportunities", "147", delta="31")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 New Scan", use_container_width=True):
            st.session_state.scan_results = None
            st.session_state.selected_solutions = {}
            st.rerun()
    
    with col2:
        if st.button("📥 Generate PDF Report", use_container_width=True, type="primary"):
            with st.spinner("📄 Generating PDF report..."):
                pdf_bytes = generate_pdf_report(results)
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_bytes,
                        file_name=f"seo_report_{results['url'].replace('https://', '').replace('/', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
    
    with col3:
        if st.button("🤖 Auto-Fix All Issues", use_container_width=True):
            with st.spinner("AI is implementing all fixes..."):
                time.sleep(2)
            st.success("✅ All fixes implemented successfully!")
    
    st.markdown("---")
    st.markdown("## 🔍 Issues & AI-Powered Solutions")
    
    # Issues
    for issue in results['issues']:
        severity_emoji = "🔴" if issue['severity'] == "critical" else "🟡" if issue['severity'] == "warning" else "🔵"
        
        with st.expander(f"{severity_emoji} **{issue['title']}** - {issue['category']}", expanded=False):
            st.markdown(f"""
            <div class="issue-card {issue['severity']}">
                <p><strong>💥 Impact:</strong> {issue['impact']}</p>
                {f"<p><strong>📊 Current State:</strong> {issue.get('current_state', 'N/A')}</p>" if 'current_state' in issue else ""}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🧠 AI Analysis")
            st.info(issue['explanation'])
            
            if 'steps' in issue:
                st.markdown("### 📋 Implementation Steps")
                for i, step in enumerate(issue['steps'], 1):
                    st.markdown(f"{i}. {step}")
            
            if 'solutions' in issue:
                st.markdown("### ✨ AI-Generated Solutions")
                for i, solution in enumerate(issue['solutions'], 1):
                    col1, col2 = st.columns([5, 1])
                    with col1:
                        st.markdown(f"""
                        <div class="solution-box">
                            <strong>Option {i}:</strong> {solution}
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        if st.button(f"✅ Use", key=f"use_{issue['id']}_{i}"):
                            st.session_state.selected_solutions[issue['id']] = i
                            st.success("Applied!")
            
            if 'automated_fixes' in issue:
                st.markdown("### ⚡ Automated Optimizations")
                for fix in issue['automated_fixes']:
                    col1, col2, col3 = st.columns([3, 2, 2])
                    with col1:
                        st.write(f"**{fix['action']}**")
                    with col2:
                        st.write(f"💾 {fix['savings']}")
                    with col3:
                        st.success(fix['impact'])
            
            if 'opportunities' in issue:
                st.markdown("### 🎯 Keyword Opportunities")
                for opp in issue['opportunities']:
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.write(opp['keyword'])
                    with col2:
                        st.write(f"📊 {opp['volume']}")
                    with col3:
                        st.write(f"{opp['difficulty']}")
                    with col4:
                        st.write(f"#{opp['potential']}")
            
            if 'code' in issue:
                st.markdown("### 💻 Implementation Code")
                st.code(issue['code'], language='html')
                if st.button(f"📋 Copy Code", key=f"copy_{issue['id']}"):
                    st.success("✅ Code copied!")
            
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🤖 Implement This Fix", key=f"implement_{issue['id']}", type="primary", use_container_width=True):
                    with st.spinner("Implementing..."):
                        time.sleep(1)
                    st.success("✅ Implemented!")
            with col2:
                if st.button(f"📤 Export Issue", key=f"export_{issue['id']}", use_container_width=True):
                    st.info("📄 Exported!")