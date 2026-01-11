import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e5e7eb;
        text-align: center;
        transition: all 0.3s;
        height: 100%;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    }
    .feature-card:hover {
        border-color: #667eea;
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.25);
    }
    .status-card {
        background: #f9fafb;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin: 1rem 0;
    }
    .cta-section {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">🎯 Nexus SEO Intelligence</h1>
    <h2 style="font-size: 1.8rem; font-weight: normal; opacity: 0.95; margin-bottom: 1.5rem;">
        AI-Powered SEO Analysis Platform
    </h2>
    <p style="font-size: 1.3rem; opacity: 0.9;">
        Analyze, Optimize, Dominate Search Rankings
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Start CTA
st.markdown("### 🚀 Ready to Boost Your SEO?")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="cta-section">
        <p style="font-size: 1.2rem; color: #4b5563; margin-bottom: 1.5rem;">
            Start your AI-powered website analysis in seconds
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧠 Start AI Analysis Now", use_container_width=True, type="primary", key="start_scan"):
        st.switch_page("pages/3_Advanced_Scanner.py")

st.markdown("---")

# System Status
st.markdown("### ⚙️ System Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="status-card">
        <h3>🗄️ DATABASE</h3>
        <h2 style="color: #10b981; margin: 0.5rem 0;">✓ Online</h2>
        <p style="color: #6b7280; margin: 0;">Supabase</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="status-card">
        <h3>💳 PAYMENTS</h3>
        <h2 style="color: #10b981; margin: 0.5rem 0;">✓ Active</h2>
        <p style="color: #6b7280; margin: 0;">Stripe</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="status-card">
        <h3>🤖 AI ENGINE</h3>
        <h2 style="color: #10b981; margin: 0.5rem 0;">✓ Ready</h2>
        <p style="color: #6b7280; margin: 0;">Gemini</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="status-card">
        <h3>📊 STATUS</h3>
        <h2 style="color: #10b981; margin: 0.5rem 0;">✓ Online</h2>
        <p style="color: #6b7280; margin: 0;">All Systems</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Features Grid
st.markdown("### ✨ Platform Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🧠</div>
        <h3>AI-Powered Scanner</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            Advanced analysis with automated solutions and actionable insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Start Scanning", key="scan1", use_container_width=True):
        st.switch_page("pages/3_Advanced_Scanner.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h3>Instant Fixes</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            AI implements solutions automatically with one-click optimization
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ View Solutions", key="fix1", use_container_width=True):
        st.switch_page("pages/3_Advanced_Scanner.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
        <h3>Growth Tracking</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            Monitor improvements, track rankings, and measure ROI over time
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ View Analytics", key="track1", use_container_width=True):
        st.switch_page("pages/3_Scan_Results.py")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
        <h3>Keyword Opportunities</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            AI identifies 100+ untapped keywords where you can rank easily
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Find Keywords", key="keywords1", use_container_width=True):
        st.switch_page("pages/3_Advanced_Scanner.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">💻</div>
        <h3>Code Generation</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            Get ready-to-use implementation code for all SEO fixes
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ Get Code", key="code1", use_container_width=True):
        st.switch_page("pages/3_Advanced_Scanner.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
        <h3>Detailed Reports</h3>
        <p style="color: #6b7280; margin: 1rem 0;">
            Export comprehensive PDF reports with all findings and solutions
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("→ View Sample", key="report1", use_container_width=True):
        st.switch_page("pages/3_Advanced_Scanner.py")

st.markdown("---")

# Quick Actions
st.markdown("### ⚡ Quick Actions")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("#### 🔍 Recent Scans")
        if 'scan_results' in st.session_state and st.session_state.scan_results:
            st.success(f"Last scan: {st.session_state.scan_results.get('url', 'N/A')}")
            st.info(f"Score: {st.session_state.scan_results.get('score', 0)}/100")
            if st.button("📊 View Last Results", use_container_width=True):
                st.switch_page("pages/3_Scan_Results.py")
        else:
            st.info("No scans yet. Start your first analysis!")
            if st.button("🚀 Start First Scan", use_container_width=True):
                st.switch_page("pages/3_Advanced_Scanner.py")

with col2:
    with st.container():
        st.markdown("#### 📈 Quick Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Scans Today", "0")
            st.metric("Issues Fixed", "0")
        with col_b:
            st.metric("Avg Score", "N/A")
            st.metric("Opportunities", "0")

st.markdown("---")

# Getting Started Guide
with st.expander("📚 Getting Started Guide", expanded=False):
    st.markdown("""
    ### How to Use Nexus SEO Intelligence
    
    **Step 1: Run Your First Scan**
    - Click "Start AI Analysis Now" above
    - Enter your website URL
    - Wait 30 seconds for AI analysis
    
    **Step 2: Review AI-Powered Solutions**
    - See detailed issues with severity levels
    - Get multiple AI-generated fix options
    - View implementation code for each fix
    
    **Step 3: Implement Fixes**
    - Click "Use" to select best solution
    - Click "Implement AI Fix" for automatic implementation
    - Or copy the code and implement manually
    
    **Step 4: Track Progress**
    - Export PDF reports
    - Monitor score improvements
    - Compare with previous scans
    
    **Step 5: Optimize Keywords**
    - Review keyword opportunities
    - See search volume and difficulty
    - Get content suggestions for each keyword
    """)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; color: #6b7280; padding: 2rem 0;">
        <p style="font-size: 1.1rem;"><strong>Nexus SEO Intelligence</strong></p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Powered by Advanced AI Technology</p>
        <p style="font-size: 0.85rem; opacity: 0.6;">© 2026 All rights reserved</p>
    </div>
    """, unsafe_allow_html=True)