"""
NEXUS SEO INTELLIGENCE - Complete Modern App
With Login, Dashboard, and Navigation
"""

import streamlit as st
import os
from supabase import create_client

# Page config MUST be first
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 3rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def get_supabase_client():
    try:
        supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        supabase_key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    except:
        from dotenv import load_dotenv
        load_dotenv()
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Supabase credentials not configured")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

@st.cache_resource
def get_service_client():
    try:
        supabase_url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        service_key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    except:
        supabase_url = os.getenv('SUPABASE_URL')
        service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not service_key:
        return None
    
    return create_client(supabase_url, service_key)

supabase = get_supabase_client()
service_supabase = get_service_client()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    if st.session_state.user is None:
        render_login()
    else:
        render_dashboard()

def render_login():
    """Modern login page"""
    
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3rem; margin: 0;">🎯 Nexus SEO Intelligence</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem; opacity: 0.9;">
            AI-Powered SEO Analysis Platform
        </p>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.8;">
            Analyze • Optimize • Dominate Search Rankings
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Sign In", "✨ Sign Up"])
        
        with tab1:
            st.markdown("### Welcome Back!")
            email = st.text_input("📧 Email", key="login_email")
            password = st.text_input("🔒 Password", type="password", key="login_password")
            
            if st.button("Sign In", key="login_btn", use_container_width=True):
                if email and password:
                    try:
                        result = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        
                        if result:
                            st.session_state.user = result.user
                            st.success("✅ Welcome back!")
                            st.balloons()
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {str(e)}")
                else:
                    st.warning("Please enter email and password")
        
        with tab2:
            st.markdown("### Join Nexus SEO")
            full_name = st.text_input("👤 Full Name", key="signup_name")
            email = st.text_input("📧 Email", key="signup_email")
            password = st.text_input("🔒 Password (min 6 characters)", type="password", key="signup_password")
            
            if st.button("Create Account", key="signup_btn", use_container_width=True):
                if full_name and email and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            result = supabase.auth.sign_up({
                                "email": email,
                                "password": password,
                                "options": {
                                    "data": {
                                        "full_name": full_name
                                    }
                                }
                            })
                            
                            if result:
                                st.success("✅ Account created! Check your email to verify.")
                                st.balloons()
                        except Exception as e:
                            st.error(f"❌ Signup failed: {str(e)}")
                else:
                    st.warning("Please fill in all fields")

def render_dashboard():
    """Modern dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("---")
        
        user_email = st.session_state.user.email
        st.markdown(f"### 👤 {user_email.split('@')[0]}")
        st.caption(user_email)
        
        st.markdown("---")
        
        # Get user data
        user_data = None
        if service_supabase:
            try:
                user_id = st.session_state.user.id
                profile = service_supabase.table('profiles').select('*').eq('id', user_id).execute()
                if profile.data:
                    user_data = profile.data[0]
            except:
                pass
        
        if user_data:
            tier = user_data.get('tier', 'free').upper()
            st.markdown(f"**{tier} Plan**")
            
            st.markdown("---")
            
            credits = user_data.get('credits_balance', 0)
            scans_used = user_data.get('monthly_scans_used', 0)
            scan_limit = user_data.get('monthly_scan_limit', 50)
            
            st.metric("💎 Credits", f"{credits:,}")
            st.metric("📊 Scans", f"{scans_used}/{scan_limit}")
            
            progress = min(scans_used / scan_limit, 1.0) if scan_limit > 0 else 0
            st.progress(progress)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    
    # Main content
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5rem; margin: 0;">Welcome to Your SEO Command Center 🚀</h1>
        <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;">
            Powered by AI • Real-time Analysis • Actionable Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🗄️ Database", "✅ Online")
    with col2:
        st.metric("💳 Payments", "✅ Active")
    with col3:
        st.metric("🤖 AI Engine", "✅ Ready")
    with col4:
        st.metric("📊 Status", "🟢 Live")
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("## 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🔍 Advanced Scanner")
        st.caption("AI-powered deep analysis")
        if st.button("Launch Scanner", key="scanner", use_container_width=True, type="primary"):
            st.switch_page("pages/Advanced_Scanner.py")
    
    with col2:
        st.markdown("### 📊 Scan Results")
        st.caption("View detailed reports")
        if st.button("View Results", key="results", use_container_width=True):
            st.switch_page("pages/3_Scan_Results.py")
    
    with col3:
        st.markdown("### 🤖 AI Insights")
        st.caption("Smart recommendations")
        if st.button("Get Insights", key="insights", use_container_width=True):
            st.info("Run a scan first!")
    
    with col4:
        st.markdown("### 💳 Billing")
        st.caption("Manage subscription")
        if st.button("View Plans", key="billing", use_container_width=True):
            st.switch_page("pages/4_Billing.py")
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("## 📈 Recent Activity")
    
    if service_supabase and user_data:
        try:
            user_id = st.session_state.user.id
            recent_scans = service_supabase.table('seo_scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
            
            if recent_scans.data and len(recent_scans.data) > 0:
                for scan in recent_scans.data[:3]:
                    score = scan.get('overall_score', 0)
                    domain = scan.get('domain', 'Unknown')
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**🌐 {domain}**")
                    with col2:
                        icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                        st.markdown(f"{icon} **{score}/100**")
                    with col3:
                        if st.button("View", key=f"view_{scan['id']}", use_container_width=True):
                            st.session_state.current_scan = scan
                            st.switch_page("pages/3_Scan_Results.py")
            else:
                st.info("🎯 **No scans yet!** Launch the Advanced Scanner to get started.")
        except Exception as e:
            st.info("🎯 **Ready to start!** Use the Advanced Scanner above.")
    else:
        st.info("🎯 **Welcome!** Launch the Advanced Scanner to analyze your first website.")
    
    st.markdown("---")
    
    # Features
    st.markdown("## ✨ Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Advanced Scanner</h3>
            <p>Deep technical analysis with 50+ SEO checkpoints</p>
            <ul>
                <li>Technical SEO audit</li>
                <li>Content analysis</li>
                <li>Performance metrics</li>
                <li>Mobile optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Insights</h3>
            <p>Smart recommendations powered by AI</p>
            <ul>
                <li>Automated analysis</li>
                <li>Priority rankings</li>
                <li>Action plans</li>
                <li>Competitor intel</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Reports</h3>
            <p>Professional reports ready to share</p>
            <ul>
                <li>PDF export</li>
                <li>White-label ready</li>
                <li>Email delivery</li>
                <li>Custom branding</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()