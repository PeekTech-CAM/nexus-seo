"""
NEXUS SEO INTELLIGENCE - Advanced Dashboard
Modern, powerful, AI-driven SEO platform
"""

import streamlit as st
import os
from supabase import create_client
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Animated gradient background */
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
    
    /* Feature cards */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Stat cards with gradient */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Action cards */
    .action-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .action-card:hover {
        border-color: #667eea;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Progress bars */
    .progress-container {
        background: #f0f0f0;
        border-radius: 10px;
        height: 10px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animated {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def get_supabase_client():
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
    
    return create_client(supabase_url, supabase_key)

@st.cache_resource
def get_service_client():
    try:
        supabase_url = st.secrets["SUPABASE_URL"]
        service_key = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]
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
        render_advanced_dashboard()

def render_login():
    """Modern login page"""
    
    # Hero section
    st.markdown("""
    <div class="hero-section animated">
        <h1 style="font-size: 3rem; margin: 0;">🎯 Nexus SEO Intelligence</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem; opacity: 0.9;">
            AI-Powered SEO Analysis Platform
        </p>
        <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.8;">
            Analyze, Optimize, Dominate Search Rankings
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

def render_advanced_dashboard():
    """Advanced dashboard with AI insights"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("---")
        
        # User profile section
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
            # Plan badge
            tier = user_data.get('tier', 'free').upper()
            if tier == 'FREE':
                st.markdown("🆓 **Free Plan**")
            elif tier == 'PRO':
                st.markdown("⭐ **Pro Plan**")
            elif tier == 'AGENCY':
                st.markdown("🚀 **Agency Plan**")
            else:
                st.markdown(f"👑 **{tier} Plan**")
            
            st.markdown("---")
            
            # Stats
            credits = user_data.get('credits_balance', 0)
            scans_used = user_data.get('monthly_scans_used', 0)
            scan_limit = user_data.get('monthly_scan_limit', 50)
            
            st.metric("💎 Credits", f"{credits:,}")
            st.metric("📊 Scans This Month", f"{scans_used}/{scan_limit}")
            
            # Progress bar
            progress = min(scans_used / scan_limit, 1.0) if scan_limit > 0 else 0
            st.progress(progress)
            
            if scans_used >= scan_limit * 0.8:
                st.warning("⚠️ Almost at scan limit!")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    
    # Main content
    # Hero section
    st.markdown("""
    <div class="hero-section animated">
        <h1 style="font-size: 2.5rem; margin: 0;">Welcome to Your SEO Command Center 🚀</h1>
        <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.9;">
            Powered by AI • Real-time Analysis • Actionable Insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card animated">
            <div class="stat-label">🗄️ DATABASE</div>
            <div class="stat-value">✅</div>
            <div class="stat-label">Supabase</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card animated">
            <div class="stat-label">💳 PAYMENTS</div>
            <div class="stat-value">✅</div>
            <div class="stat-label">Stripe</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card animated">
            <div class="stat-label">🤖 AI ENGINE</div>
            <div class="stat-value">✅</div>
            <div class="stat-label">Gemini</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card animated">
            <div class="stat-label">📊 STATUS</div>
            <div class="stat-value">🟢</div>
            <div class="stat-label">Online</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## 🎯 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 **New SEO Scan**\n\nAnalyze any website", use_container_width=True, key="new_scan"):
            st.switch_page("pages/2_New_Scan.py")
    
    with col2:
        if st.button("🤖 **AI Insights**\n\nGet smart recommendations", use_container_width=True, key="ai_insights"):
            st.info("💡 Run a scan first to get AI insights!")
    
    with col3:
        if st.button("💳 **Upgrade Plan**\n\nUnlock premium features", use_container_width=True, key="upgrade", type="primary"):
            st.switch_page("pages/4_Billing.py")
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("## 📈 Recent Activity")
    
    if service_supabase and user_data:
        try:
            user_id = st.session_state.user.id
            recent_scans = service_supabase.table('scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
            
            if recent_scans.data and len(recent_scans.data) > 0:
                # Create visualization
                scans_data = recent_scans.data
                
                # Score trend chart
                scores = [scan.get('overall_score', 0) for scan in scans_data]
                dates = [scan.get('created_at', '')[:10] for scan in scans_data]
                domains = [scan.get('domain', 'Unknown') for scan in scans_data]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(scores)))[::-1],
                    y=scores[::-1],
                    mode='lines+markers',
                    name='SEO Score',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=10, color='#764ba2'),
                    fill='tozeroy',
                    fillcolor='rgba(102, 126, 234, 0.2)'
                ))
                
                fig.update_layout(
                    title="Your SEO Score Trend",
                    xaxis_title="Scans",
                    yaxis_title="Score",
                    height=300,
                    template="plotly_white",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recent scans table
                st.markdown("### 📋 Latest Scans")
                
                for scan in scans_data[:3]:
                    score = scan.get('overall_score', 0)
                    domain = scan.get('domain', 'Unknown')
                    created = scan.get('created_at', '')[:10]
                    
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        st.markdown(f"**🌐 {domain}**")
                    with col2:
                        st.markdown(f"**{score}/100**")
                    with col3:
                        st.markdown(f"📅 {created}")
                    with col4:
                        if st.button("View", key=f"view_{scan['id']}", use_container_width=True):
                            st.session_state.current_scan = scan
                            st.switch_page("pages/3_Scan_Results.py")
            
            else:
                st.info("🎯 **No scans yet!** Click 'New SEO Scan' above to get started.")
                
        except Exception as e:
            st.error(f"Could not load recent activity: {str(e)}")
    else:
        st.info("🎯 **Ready to start!** Run your first SEO scan above.")
    
    st.markdown("---")
    
    # Features showcase
    st.markdown("## ✨ Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Deep SEO Analysis</h3>
            <p>Comprehensive website audits with 50+ checkpoints</p>
            <ul>
                <li>Technical SEO</li>
                <li>On-page optimization</li>
                <li>Performance metrics</li>
                <li>Mobile-friendliness</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Insights</h3>
            <p>Smart recommendations powered by Google Gemini</p>
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
            <h3>📊 Beautiful Reports</h3>
            <p>Professional PDF reports ready to share</p>
            <ul>
                <li>White-label ready</li>
                <li>Client-friendly</li>
                <li>Email delivery</li>
                <li>Export options</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()