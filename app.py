"""
NEXUS SEO INTELLIGENCE - Clean & Powerful Platform
"""

import streamlit as st
import os
from supabase import create_client

# Page config
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 2rem;
        background: #f8fafc;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }
    
    /* Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        text-align: center;
        transition: all 0.3s;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    /* Stats card */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def get_supabase_client():
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
    except:
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Database not configured")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

supabase = get_supabase_client()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    if st.session_state.user is None:
        render_login()
    else:
        render_dashboard()

def render_login():
    """Clean login page"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #6366f1; font-size: 3rem; margin: 0;">🎯</h1>
            <h1 style="margin: 0;">Nexus SEO Intelligence</h1>
            <p style="color: #6b7280;">AI-Powered SEO Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit and email and password:
                    try:
                        result = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        if result:
                            st.session_state.user = result.user
                            st.success("✅ Signed in successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {str(e)}")
        
        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name", key="signup_name")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password (min 6 characters)", type="password", key="signup_password")
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit and name and email and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            result = supabase.auth.sign_up({
                                "email": email,
                                "password": password,
                                "options": {"data": {"full_name": name}}
                            })
                            if result:
                                st.success("✅ Account created! Check your email.")
                        except Exception as e:
                            st.error(f"❌ Signup failed: {str(e)}")

def render_dashboard():
    """Clean dashboard"""
    
    # Sidebar
    with st.sidebar:
        # Logo in sidebar
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0; margin-bottom: 1rem;">
            <h2 style="color: #6366f1; margin: 0;">🎯</h2>
            <h3 style="margin: 0.5rem 0;">Nexus SEO</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"**{st.session_state.user.email}**")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            try:
                supabase.auth.sign_out()
            except:
                pass
            st.session_state.user = None
            st.rerun()
    
    # Main content
    st.title("Welcome to Nexus SEO Intelligence! 🚀")
    st.markdown("### Your AI-Powered SEO Command Center")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("## 📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Plan</div>
            <div class="stat-number">PRO</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Credits</div>
            <div class="stat-number">0</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Scans This Month</div>
            <div class="stat-number">0/50</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total Scans</div>
            <div class="stat-number">0</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Features - CLEAN, NO REPETITION
    st.markdown("## 🚀 Main Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2 style="font-size: 3rem; margin: 0;">🧠</h2>
            <h3>AI SEO Scanner</h3>
            <p style="color: #6b7280;">Advanced multi-agent AI analysis with comprehensive insights</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Start New Scan", use_container_width=True, key="scan_btn"):
            st.switch_page("pages/2_New_Scan.py")
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2 style="font-size: 3rem; margin: 0;">📊</h2>
            <h3>Scan History</h3>
            <p style="color: #6b7280;">View and manage your previous SEO analysis reports</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📂 View History", use_container_width=True, key="history_btn"):
            st.info("Scan history coming soon!")
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2 style="font-size: 3rem; margin: 0;">💳</h2>
            <h3>Upgrade Plan</h3>
            <p style="color: #6b7280;">Get more scans and unlock advanced features</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Upgrade Now", use_container_width=True, type="primary", key="upgrade_btn"):
            st.switch_page("pages/4_Billing.py")
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("## ✨ What You Can Do")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Advanced AI Analysis
        - **4 AI Agents** working together
        - Technical SEO deep dive
        - Content strategy recommendations
        - Competitive intelligence
        - 90-day action plans
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Comprehensive Reports
        - Real-time scoring system
        - Priority-based recommendations
        - Export to JSON/PDF
        - Email delivery
        - Track progress over time
        """)

if __name__ == "__main__":
    main()