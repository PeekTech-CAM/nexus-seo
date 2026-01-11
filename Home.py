"""
SEO Tools Dashboard - Main Home Page
Professional SEO analysis and monitoring platform
"""

import streamlit as st

# Page config
st.set_page_config(
    page_title="SEO Tools Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Sidebar
st.markdown("""
<style>
    /* Advanced Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }
    
    [data-testid="stSidebar"] h1 {
        color: white;
        font-size: 1.5rem;
        padding: 1rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    [data-testid="stSidebar"] .sidebar-section {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 1rem 1rem 0.5rem 1rem;
        margin-top: 1rem;
    }
    
    /* Sidebar buttons */
    [data-testid="stSidebar"] button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(102, 126, 234, 0.2) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 🚀 SEO Tools Pro")
    st.caption("Advanced SEO Analysis Platform")
    st.markdown("---")
    
    # Quick Action
    if st.button("🔍 New Scan", use_container_width=True, type="primary"):
        st.info("Scanner page - Add your scanner page path")
    
    # Main Features
    st.markdown('<div class="sidebar-section">📊 Main Features</div>', unsafe_allow_html=True)
    
    if st.button("🏠 Dashboard", use_container_width=True, key="sb_home"):
        st.rerun()
    
    if st.button("🎯 Competitor Analysis", use_container_width=True, key="sb_comp"):
        st.switch_page("pages/1_🎯_Competitor_Analysis.py")
    
    if st.button("🔗 Backlink Monitor", use_container_width=True, key="sb_back"):
        st.switch_page("pages/2_🔗_Backlink_Monitor.py")
    
    if st.button("🔑 Keyword Tracker", use_container_width=True, key="sb_key"):
        st.switch_page("pages/3_🔑_Keyword_Tracker.py")
    
    # Agency Features
    st.markdown('<div class="sidebar-section">💼 Agency Features</div>', unsafe_allow_html=True)
    
    if st.button("👥 Client Management", use_container_width=True, key="sb_client"):
        st.switch_page("pages/4_👥_Client_Management.py")
    
    if st.button("📄 White Label Reports", use_container_width=True, key="sb_reports"):
        st.switch_page("pages/5_📄_White_Label_Reports.py")
    
    if st.button("⏰ Scheduled Scans", use_container_width=True, key="sb_sched"):
        st.switch_page("pages/6_⏰_Scheduled_Scans.py")
    
    # Elite Features
    st.markdown('<div class="sidebar-section">💎 Elite Features</div>', unsafe_allow_html=True)
    
    if st.button("🤖 Custom AI Training", use_container_width=True, key="sb_ai"):
        st.switch_page("pages/7_🤖_Custom_AI_Training.py")
    
    if st.button("🔌 API Management", use_container_width=True, key="sb_api"):
        st.switch_page("pages/8_🔌_API_Management.py")
    
    if st.button("📊 Advanced Analytics", use_container_width=True, key="sb_analytics"):
        st.switch_page("pages/9_📊_Advanced_Analytics.py")
    
    # Tools
    st.markdown('<div class="sidebar-section">⚙️ Tools</div>', unsafe_allow_html=True)
    
    if st.button("💳 Billing", use_container_width=True, key="sb_billing"):
        st.info("Billing page coming soon")
    
    if st.button("⚙️ Settings", use_container_width=True, key="sb_settings"):
        st.info("Settings page coming soon")
    
    # Stats
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Scans", "12", "+3")
    with col2:
        st.metric("Keywords", "234", "+18")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Backlinks", "1.4K", "+45")
    with col2:
        st.metric("Clients", "8", "+2")
    
    # User
    st.markdown("---")
    st.markdown("**👤 John Doe**")
    st.caption("Pro Plan • Active")
    
    st.markdown("---")
    st.caption("© 2026 SEO Tools Pro v2.0")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-section {
        margin-top: 3rem;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        font-size: 0.95rem;
        color: #666;
        margin-bottom: 1.5rem;
    }
    .feature-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .feature-button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .stats-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🏠 Home Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Welcome to your SEO command center</div>', unsafe_allow_html=True)

# Quick stats
st.markdown("""
<div class="stats-container">
    <h2 style="margin: 0; margin-bottom: 1rem;">📊 Quick Overview</h2>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem;">
        <div>
            <div style="font-size: 2rem; font-weight: 700;">234</div>
            <div style="opacity: 0.9;">Keywords Tracked</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: 700;">1,456</div>
            <div style="opacity: 0.9;">Backlinks</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: 700;">45,234</div>
            <div style="opacity: 0.9;">Monthly Traffic</div>
        </div>
        <div>
            <div style="font-size: 2rem; font-weight: 700;">67</div>
            <div style="opacity: 0.9;">Domain Authority</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Features Section
st.markdown('<div class="feature-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">🎯 Main Features</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">Competitor Analysis</div>
        <div class="feature-description">Compare with competitors</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Analyze →", key="competitor", use_container_width=True):
        st.switch_page("pages/1_🎯_Competitor_Analysis.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔗</div>
        <div class="feature-title">Backlink Monitor</div>
        <div class="feature-description">Track your backlinks</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Monitor →", key="backlink", use_container_width=True):
        st.switch_page("pages/2_🔗_Backlink_Monitor.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔑</div>
        <div class="feature-title">Keyword Tracker</div>
        <div class="feature-description">Track rankings</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Track →", key="keyword", use_container_width=True):
        st.switch_page("pages/3_🔑_Keyword_Tracker.py")

st.markdown('</div>', unsafe_allow_html=True)

# Agency Features Section
st.markdown('<div class="feature-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">💼 Agency Features</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <div class="feature-title">Client Management</div>
        <div class="feature-description">Manage client accounts</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Manage →", key="client", use_container_width=True):
        st.switch_page("pages/4_👥_Client_Management.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📄</div>
        <div class="feature-title">White Label Reports</div>
        <div class="feature-description">Custom branded reports</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Create →", key="reports", use_container_width=True):
        st.switch_page("pages/5_📄_White_Label_Reports.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⏰</div>
        <div class="feature-title">Scheduled Scans</div>
        <div class="feature-description">Automate scanning</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Schedule →", key="scheduled", use_container_width=True):
        st.switch_page("pages/6_⏰_Scheduled_Scans.py")

st.markdown('</div>', unsafe_allow_html=True)

# Elite Features Section
st.markdown('<div class="feature-section">', unsafe_allow_html=True)
st.markdown('<div class="section-header">💎 Elite Features</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">Custom AI Training</div>
        <div class="feature-description">Train custom models</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Configure →", key="ai", use_container_width=True):
        st.switch_page("pages/7_🤖_Custom_AI_Training.py")

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔌</div>
        <div class="feature-title">API Management</div>
        <div class="feature-description">Manage API access</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("API Docs →", key="api", use_container_width=True):
        st.switch_page("pages/8_🔌_API_Management.py")

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Advanced Analytics</div>
        <div class="feature-description">Deep insights</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Analytics →", key="analytics", use_container_width=True):
        st.switch_page("pages/9_📊_Advanced_Analytics.py")

st.markdown('</div>', unsafe_allow_html=True)

# Recent Activity
st.markdown("---")
st.markdown("### 📈 Recent Activity")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 www.google.com</h4>
        <p style="color: #666;">Last scanned: 2 hours ago</p>
        <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">61/100</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 www.letous.com</h4>
        <p style="color: #666;">Last scanned: 5 hours ago</p>
        <div style="font-size: 1.5rem; font-weight: 700; color: #f59e0b;">76/100</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>🌐 www.example.com</h4>
        <p style="color: #666;">Last scanned: 1 day ago</p>
        <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">85/100</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("💡 **Quick Tip:** Use the sidebar to navigate between features or click the buttons above to get started!")