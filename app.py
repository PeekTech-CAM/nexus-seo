"""
NEXUS SEO INTELLIGENCE - Secure Production App
Complete with authentication and profile management
Enhanced with powerful navigation system
"""

import streamlit as st

# Page config MUST be first
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
from supabase import create_client

# Enhanced Modern CSS with Navigation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
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
    
    /* Navigation styles */
    .nav-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .nav-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar navigation */
    .sidebar-nav-btn {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .sidebar-nav-btn:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: transparent;
        transform: translateX(5px);
    }
    
    /* Current page indicator */
    .current-page {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem 1rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def get_supabase_client():
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
        if not url or not key:
            st.error("⚠️ Supabase credentials not configured")
            st.stop()
        return create_client(url, key)
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        st.stop()

@st.cache_resource
def get_service_client():
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if key:
            return create_client(url, key)
    except:
        pass
    return None

supabase = get_supabase_client()
service_supabase = get_service_client()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def ensure_user_profile(user_id, email):
    """Ensure user profile exists, create if not"""
    try:
        client = service_supabase or supabase
        
        # Try to get existing profile
        result = client.table('profiles').select('*').eq('id', user_id).execute()
        
        if not result.data:
            # Create new profile
            new_profile = {
                'id': user_id,
                'email': email,
                'tier': 'demo',
                'credits_balance': 1000,
                'monthly_scans_used': 0,
                'monthly_scan_limit': 50
            }
            client.table('profiles').insert(new_profile).execute()
            return new_profile
        
        return result.data[0]
    except Exception as e:
        print(f"Profile creation error: {str(e)}")
        # Return default profile
        return {
            'tier': 'demo',
            'credits_balance': 1000,
            'monthly_scans_used': 0,
            'monthly_scan_limit': 50
        }

def render_sidebar_navigation(user_email, user_data):
    """Enhanced sidebar with navigation"""
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🎯 Nexus SEO
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"### 👤 {user_email.split('@')[0]}")
        st.caption(user_email)
        
        tier = user_data.get('tier', 'demo').upper()
        tier_color = "🟢" if tier == "PRO" else "🔵" if tier == "DEMO" else "⚪"
        st.markdown(f"**{tier_color} {tier} Plan**")
        
        st.markdown("---")
        
        # Credits and usage
        credits = user_data.get('credits_balance', 0)
        scans_used = user_data.get('monthly_scans_used', 0)
        scan_limit = user_data.get('monthly_scan_limit', 50)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💎 Credits", f"{credits:,}")
        with col2:
            st.metric("📊 Scans", f"{scans_used}/{scan_limit}")
        
        progress = min(scans_used / scan_limit, 1.0) if scan_limit > 0 else 0
        st.progress(progress)
        
        if progress >= 0.8:
            st.warning("⚠️ Nearing scan limit!")
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 🧭 Navigation")
        
        # Home button (always visible)
        if st.button("🏠 Home Dashboard", use_container_width=True, key="nav_home", 
                    type="primary" if st.session_state.current_page == 'home' else "secondary"):
            st.session_state.current_page = 'home'
            st.rerun()
        
        st.markdown("**📍 Quick Actions**")
        
        # Scanner
        if st.button("🔍 Advanced Scanner", use_container_width=True, key="nav_scanner"):
            st.session_state.current_page = 'scanner'
            st.switch_page("pages/Advanced_Scanner.py")
        
        # Results
        if st.button("📊 Scan Results", use_container_width=True, key="nav_results"):
            st.session_state.current_page = 'results'
            st.switch_page("pages/3_Scan_Results.py")
        
        # Billing
        if st.button("💳 Billing & Plans", use_container_width=True, key="nav_billing"):
            st.session_state.current_page = 'billing'
            st.switch_page("pages/4_Billing.py")
        
        # Check Prices (if this page exists)
        if st.button("💰 Check Prices", use_container_width=True, key="nav_prices"):
            st.session_state.current_page = 'prices'
            st.switch_page("pages/5_Check_Prices.py")
        
        st.markdown("---")
        
        # Debug/Admin section (if needed)
        with st.expander("🔧 Debug Tools"):
            if st.button("🧪 Quick Test", use_container_width=True, key="nav_test"):
                st.session_state.current_page = 'test'
                st.switch_page("pages/6_Quick_Test.py")
            
            if st.button("🔐 Debug Secrets", use_container_width=True, key="nav_secrets"):
                st.switch_page("pages/7_Debug_Secrets.py")
            
            if st.button("💳 Debug Stripe", use_container_width=True, key="nav_stripe"):
                st.switch_page("pages/8_Debug_Stripe.py")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="primary", key="logout_btn"):
            try:
                supabase.auth.sign_out()
            except:
                pass
            st.session_state.user = None
            st.session_state.current_page = 'home'
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("🎯 Nexus SEO Intelligence v2.0")
        st.caption("© 2025 All rights reserved")

def main():
    if st.session_state.user is None:
        render_login()
    else:
        render_dashboard()

def render_login():
    """Secure login page"""
    
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3rem; margin: 0;">🎯 Nexus SEO Intelligence</h1>
        <p style="font-size: 1.3rem; margin-top: 1rem; opacity: 0.9;">
            AI-Powered SEO Analysis Platform
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
                        
                        if result and result.user:
                            st.session_state.user = result.user
                            st.session_state.current_page = 'home'
                            # Ensure profile exists
                            ensure_user_profile(result.user.id, email)
                            st.success("✅ Welcome back!")
                            st.balloons()
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: Invalid credentials")
                else:
                    st.warning("Please enter email and password")
        
        with tab2:
            st.markdown("### Join Nexus SEO")
            full_name = st.text_input("👤 Full Name", key="signup_name")
            email = st.text_input("📧 Email", key="signup_email")
            password = st.text_input("🔒 Password (min 6 chars)", type="password", key="signup_password")
            
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
                            
                            if result and result.user:
                                # Create profile immediately
                                ensure_user_profile(result.user.id, email)
                                st.success("✅ Account created! Check your email to verify.")
                                st.balloons()
                        except Exception as e:
                            st.error(f"❌ Signup failed: {str(e)}")
                else:
                    st.warning("Please fill in all fields")

def render_dashboard():
    """Enhanced dashboard with navigation"""
    
    # Get user profile
    user_id = st.session_state.user.id
    user_email = st.session_state.user.email
    user_data = ensure_user_profile(user_id, user_email)
    
    # Render enhanced sidebar
    render_sidebar_navigation(user_email, user_data)
    
    # Main content
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5rem; margin: 0;">Welcome to Your SEO Command Center 🚀</h1>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            AI-Powered Analysis • Real-time Insights • Actionable Results
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current page indicator (if not home)
    if st.session_state.current_page != 'home':
        st.info(f"📍 Current Page: **{st.session_state.current_page.title()}** | Click 🏠 Home in sidebar to return to dashboard")
    
    # Stats
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
    
    # Quick Actions with enhanced cards
    st.markdown("## 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        with st.container():
            st.markdown("### 🔍 Scanner")
            st.caption("Analyze any website")
            if st.button("Launch Scanner →", key="scanner_card", use_container_width=True, type="primary"):
                st.session_state.current_page = 'scanner'
                st.switch_page("pages/Advanced_Scanner.py")
    
    with col2:
        with st.container():
            st.markdown("### 📊 Results")
            st.caption("View past scans")
            if st.button("View Results →", key="results_card", use_container_width=True):
                st.session_state.current_page = 'results'
                st.switch_page("pages/3_Scan_Results.py")
    
    with col3:
        with st.container():
            st.markdown("### 🤖 AI Insights")
            st.caption("Get recommendations")
            if st.button("Get Insights →", key="insights_card", use_container_width=True):
                st.info("💡 Run a scan first to get AI insights!")
    
    with col4:
        with st.container():
            st.markdown("### 💳 Upgrade")
            st.caption("Unlock Pro features")
            if st.button("View Plans →", key="billing_card", use_container_width=True):
                st.session_state.current_page = 'billing'
                st.switch_page("pages/4_Billing.py")
    
    st.markdown("---")
    
    # Recent Activity
    st.markdown("## 📈 Recent Activity")
    
    try:
        client = service_supabase or supabase
        recent = client.table('seo_scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
        
        if recent.data and len(recent.data) > 0:
            for scan in recent.data[:3]:
                score = scan.get('overall_score', 0)
                domain = scan.get('domain', 'Unknown')
                icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**🌐 {domain}**")
                with col2:
                    st.markdown(f"{icon} **{score}/100**")
                with col3:
                    if st.button("View →", key=f"v_{scan['id']}", use_container_width=True):
                        st.session_state.current_scan = scan
                        st.session_state.current_page = 'results'
                        st.switch_page("pages/3_Scan_Results.py")
        else:
            st.info("🎯 **No scans yet!** Launch the Scanner to get started.")
            if st.button("🚀 Start Your First Scan", type="primary"):
                st.session_state.current_page = 'scanner'
                st.switch_page("pages/Advanced_Scanner.py")
    except Exception as e:
        st.info("🎯 **Welcome!** Use the Scanner to analyze your first website.")
        if st.button("🚀 Launch Scanner Now", type="primary"):
            st.session_state.current_page = 'scanner'
            st.switch_page("pages/Advanced_Scanner.py")
    
    # Usage tips
    st.markdown("---")
    st.markdown("## 💡 Quick Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔍 Scanner Tips**
        - Enter any URL to analyze
        - Get instant SEO scores
        - View detailed reports
        """)
    
    with col2:
        st.success("""
        **💎 Credit System**
        - Demo: 1000 free credits
        - Each scan uses credits
        - Upgrade for unlimited
        """)
    
    with col3:
        st.warning("""
        **🚀 Pro Features**
        - Unlimited scans
        - Priority support
        - Advanced analytics
        """)

if __name__ == "__main__":
    main()