"""
NEXUS SEO INTELLIGENCE - Main Streamlit Application
Production-grade multi-page Streamlit app with professional UI
"""

import streamlit as st
from supabase import create_client, Client
import os
from typing import Optional
import logging

# Page configuration
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://nexusseo.com/support',
        'Report a bug': 'https://nexusseo.com/report',
        'About': 'Nexus SEO Intelligence - Enterprise SEO Platform'
    }
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Modern color scheme inspired by Stripe/Linear */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f9fafb;
        --border-color: #e5e7eb;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global styling */
    .main {
        padding: 2rem;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .score-excellent {
        color: var(--success-color);
        font-weight: 600;
    }
    
    .score-good {
        color: #3b82f6;
        font-weight: 600;
    }
    
    .score-fair {
        color: var(--warning-color);
        font-weight: 600;
    }
    
    .score-poor {
        color: var(--danger-color);
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(99, 102, 241, 0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid var(--border-color);
        padding: 0.75rem;
    }
    
    /* Success message */
    .success-banner {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Warning message */
    .warning-banner {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase client
@st.cache_resource
def get_supabase_client() -> Client:
    """Initialize and cache Supabase client."""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        st.error("⚠️ Supabase credentials not configured")
        st.stop()
    
    return create_client(supabase_url, supabase_key)

supabase = get_supabase_client()

# Authentication utilities
def init_session_state():
    """Initialize session state variables."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'profile' not in st.session_state:
        st.session_state.profile = None

def get_current_user() -> Optional[dict]:
    """Get current authenticated user."""
    try:
        user = supabase.auth.get_user()
        return user if user else None
    except Exception as e:
        return None

def get_user_profile(user_id: str) -> Optional[dict]:
    """Get user profile from database."""
    try:
        result = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        return result.data if result.data else None
    except Exception as e:
        logging.error(f"Error fetching profile: {e}")
        return None

def logout():
    """Handle user logout."""
    try:
        supabase.auth.sign_out()
        st.session_state.user = None
        st.session_state.profile = None
        st.rerun()
    except Exception as e:
        st.error(f"Logout failed: {e}")

# Navigation
def render_sidebar():
    """Render sidebar navigation."""
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("### Intelligence Platform")
        
        if st.session_state.user:
            profile = st.session_state.profile
            
            # User info
            st.markdown("---")
            st.markdown(f"**{profile.get('full_name', 'User')}**")
            st.markdown(f"*{profile.get('tier', 'demo').upper()} Plan*")
            
            # Credits display
            credits = profile.get('credits_balance', 0)
            st.markdown(f"💎 **{credits:,}** credits")
            
            # Navigation
            st.markdown("---")
            st.markdown("### 📊 Dashboard")
            
            pages = {
                "🏠 Overview": "pages/1_Dashboard.py",
                "🔍 New Scan": "pages/2_New_Scan.py",
                "📈 Analytics": "pages/3_Analytics.py",
                "🤖 AI Insights": "pages/4_AI_Insights.py",
                "💳 Billing": "pages/5_Billing.py",
                "⚙️ Settings": "pages/6_Settings.py",
            }
            
            for page_name, page_path in pages.items():
                if st.button(page_name, use_container_width=True):
                    st.switch_page(page_path)
            
            # Admin section
            if profile.get('is_admin', False):
                st.markdown("---")
                st.markdown("### 🔧 Admin")
                if st.button("👥 User Management", use_container_width=True):
                    st.switch_page("pages/admin/Users.py")
                if st.button("📊 Analytics Dashboard", use_container_width=True):
                    st.switch_page("pages/admin/Analytics.py")
            
            # Logout
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                logout()
        else:
            st.markdown("### Welcome!")
            st.markdown("Sign in to access your SEO dashboard")

def render_tier_badge(tier: str) -> str:
    """Render tier badge HTML."""
    colors = {
        'demo': '#6b7280',
        'pro': '#6366f1',
        'agency': '#8b5cf6',
        'elite': '#f59e0b'
    }
    color = colors.get(tier, colors['demo'])
    return f'<span style="background:{color};color:white;padding:0.25rem 0.75rem;border-radius:12px;font-size:0.75rem;font-weight:600;">{tier.upper()}</span>'

def render_score_badge(score: int) -> str:
    """Render SEO score with color coding."""
    if score >= 90:
        css_class = "score-excellent"
        label = "Excellent"
    elif score >= 70:
        css_class = "score-good"
        label = "Good"
    elif score >= 50:
        css_class = "score-fair"
        label = "Fair"
    else:
        css_class = "score-poor"
        label = "Poor"
    
    return f'<span class="{css_class}" style="font-size:2rem;">{score}/100</span><br><small>{label}</small>'

# Main app
def main():
    """Main application entry point."""
    init_session_state()
    
    # Check authentication
    current_user = get_current_user()
    
    if current_user:
        user_id = current_user.user.id if hasattr(current_user, 'user') else current_user.get('id')
        st.session_state.user = current_user
        st.session_state.profile = get_user_profile(user_id)
        
        render_sidebar()
        
        # Default landing page
        st.title("🎯 Nexus SEO Intelligence")
        st.markdown("### Enterprise-Grade SEO Analysis Platform")
        
        profile = st.session_state.profile
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Plan",
                profile.get('tier', 'demo').upper(),
                delta=None
            )
        
        with col2:
            st.metric(
                "Credits Balance",
                f"{profile.get('credits_balance', 0):,}",
                delta=None
            )
        
        with col3:
            scans_used = profile.get('monthly_scans_used', 0)
            scan_limit = profile.get('monthly_scan_limit', 2)
            st.metric(
                "Scans This Month",
                f"{scans_used}/{scan_limit}",
                delta=None
            )
        
        with col4:
            total_scans = supabase.table('scans').select('id', count='exact').eq('user_id', user_id).execute()
            st.metric(
                "Total Scans",
                len(total_scans.data) if total_scans.data else 0,
                delta=None
            )
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 New SEO Scan", use_container_width=True):
                st.switch_page("pages/2_New_Scan.py")
        
        with col2:
            if st.button("🤖 AI Analysis", use_container_width=True):
                st.switch_page("pages/4_AI_Insights.py")
        
        with col3:
            if st.button("💳 Upgrade Plan", use_container_width=True):
                st.switch_page("pages/5_Billing.py")
        
        st.markdown("---")
        
        # Recent scans
        st.markdown("### 📊 Recent Scans")
        
        recent_scans = supabase.table('scans').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5).execute()
        
        if recent_scans.data:
            for scan in recent_scans.data:
                with st.expander(f"{scan['domain']} - {scan['created_at'][:10]}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**Overall Score**")
                        st.markdown(render_score_badge(scan.get('overall_score', 0)), unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**Technical**")
                        st.markdown(f"{scan.get('technical_score', 0)}/100")
                    
                    with col3:
                        st.markdown("**Content**")
                        st.markdown(f"{scan.get('content_score', 0)}/100")
                    
                    with col4:
                        st.markdown("**Performance**")
                        st.markdown(f"{scan.get('performance_score', 0)}/100")
                    
                    if st.button("View Details", key=f"view_{scan['id']}"):
                        st.switch_page("pages/3_Analytics.py")
        else:
            st.info("No scans yet. Create your first scan to get started!")
        
    else:
        # Login page
        render_login_page()

def render_login_page():
    """Render login/signup page."""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1 style="font-size: 3rem; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎯 Nexus SEO Intelligence
        </h1>
        <p style="font-size: 1.5rem; color: #6b7280;">Enterprise-Grade SEO Analysis Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        st.markdown("### Sign In to Your Account")
        
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Sign In", use_container_width=True):
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                if result:
                    st.success("✅ Signed in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with tab2:
        st.markdown("### Create Your Account")
        
        full_name = st.text_input("Full Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        
        if st.button("Create Account", use_container_width=True):
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
                    st.success("✅ Account created! Please check your email to verify.")
                else:
                    st.error("❌ Failed to create account")
            except Exception as e:
                st.error(f"❌ Error: {e}")

if __name__ == "__main__":
    main()