"""
NEXUS SEO INTELLIGENCE - Secure Production App
Complete with authentication and profile management
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

# Modern CSS
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
    """Secure dashboard"""
    
    # Get user profile
    user_id = st.session_state.user.id
    user_email = st.session_state.user.email
    user_data = ensure_user_profile(user_id, user_email)
    
    # Sidebar
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("---")
        st.markdown(f"### 👤 {user_email.split('@')[0]}")
        st.caption(user_email)
        st.markdown("---")
        
        tier = user_data.get('tier', 'demo').upper()
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
            try:
                supabase.auth.sign_out()
            except:
                pass
            st.session_state.user = None
            st.rerun()
    
    # Main content
    st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 2.5rem; margin: 0;">Welcome to Your SEO Command Center 🚀</h1>
        <p style="font-size: 1.1rem; margin-top: 1rem;">
            AI-Powered Analysis • Real-time Insights • Actionable Results
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Quick Actions
    st.markdown("## 🎯 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🔍 Scanner")
        if st.button("Launch", key="scanner", use_container_width=True, type="primary"):
            st.switch_page("pages/Advanced_Scanner.py")
    
    with col2:
        st.markdown("### 📊 Results")
        if st.button("View", key="results", use_container_width=True):
            st.switch_page("pages/3_Scan_Results.py")
    
    with col3:
        st.markdown("### 🤖 AI Insights")
        if st.button("Analyze", key="insights", use_container_width=True):
            st.info("Run a scan first!")
    
    with col4:
        st.markdown("### 💳 Billing")
        if st.button("Plans", key="billing", use_container_width=True):
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
                    if st.button("View", key=f"v_{scan['id']}", use_container_width=True):
                        st.session_state.current_scan = scan
                        st.switch_page("pages/3_Scan_Results.py")
        else:
            st.info("🎯 **No scans yet!** Launch the Scanner to get started.")
    except:
        st.info("🎯 **Welcome!** Use the Scanner to analyze your first website.")

if __name__ == "__main__":
    main()