"""
NEXUS SEO INTELLIGENCE - Complete SaaS Platform
Fixed: Demo users only see Scanner and Results (no admin features)
"""

import streamlit as st
import os
from supabase import create_client
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PLAN CONFIGURATION
PLANS = {
    'demo': {
        'name': 'Demo',
        'scans_per_month': 2,
        'credits': 0,
        'features': ['basic_scan'],
        'price': 0,
        'description': 'Try our platform with limited features'
    },
    'pro': {
        'name': 'Pro',
        'scans_per_month': 50,
        'credits': 100000,
        'features': ['basic_scan', 'ai_analysis', 'export_json', 'priority_support'],
        'price_monthly': 49,
        'price_yearly': 2457,
        'description': 'Perfect for freelancers and small businesses'
    },
    'agency': {
        'name': 'Agency',
        'scans_per_month': 200,
        'credits': 500000,
        'features': ['basic_scan', 'ai_analysis', 'export_json', 'export_pdf', 'white_label', 'api_access', 'priority_support', 'team_collaboration'],
        'price_monthly': 149,
        'price_yearly': 1430,
        'description': 'For agencies managing multiple clients'
    },
    'elite': {
        'name': 'Elite',
        'scans_per_month': -1,  # Unlimited
        'credits': 10000000,
        'features': ['basic_scan', 'ai_analysis', 'export_json', 'export_pdf', 'white_label', 'api_access', 'priority_support', 'team_collaboration', 'custom_ai_training', 'dedicated_manager', 'custom_integrations'],
        'price_monthly': 399,
        'price_yearly': 43000,
        'description': 'Enterprise solution with all features'
    }
}

# ADMIN EMAILS - Only these can access admin panel
ADMIN_EMAILS = [
    "moroccoboy1990@gmail.com",
    "admin@nexusseo.com"
]

# CSS - Enhanced styling
st.markdown("""
<style>
    .main { 
        background: #f8fafc; 
        padding: 2rem; 
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    }
    
    /* Logo in sidebar */
    [data-testid="stSidebar"] img {
        display: block;
        margin: 1rem auto;
        border-radius: 10px;
    }
    
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
    
    .plan-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .badge-demo { background: #6b7280; color: white; }
    .badge-pro { background: #3b82f6; color: white; }
    .badge-agency { background: #8b5cf6; color: white; }
    .badge-elite { background: #f59e0b; color: white; }
    
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
    
    /* Demo banner */
    .demo-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Supabase
@st.cache_resource
def get_supabase():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        st.error("⚠️ Database not configured")
        st.stop()
    
    return create_client(url, key)

supabase = get_supabase()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = 'demo'
if 'scans_used' not in st.session_state:
    st.session_state.scans_used = 0

# Helper functions
def is_admin():
    """Check if current user is admin"""
    if st.session_state.user:
        return st.session_state.user.email in ADMIN_EMAILS
    return False

def is_demo_user():
    """Check if current user is demo user"""
    if st.session_state.user:
        return st.session_state.user.id == 'demo_user' or st.session_state.user_plan == 'demo'
    return False

def has_feature(feature):
    user_plan = st.session_state.user_plan
    return feature in PLANS.get(user_plan, {}).get('features', [])

def get_scans_limit():
    limit = PLANS.get(st.session_state.user_plan, {}).get('scans_per_month', 2)
    return limit if limit > 0 else float('inf')

def can_scan():
    if st.session_state.user_plan == 'elite':
        return True
    return st.session_state.scans_used < get_scans_limit()

def load_user_data():
    try:
        if st.session_state.user.id == 'demo_user':
            st.session_state.user_plan = 'demo'
            st.session_state.scans_used = 0
            return
        
        profile = supabase.table('profiles').select('*').eq('id', st.session_state.user.id).execute()
        
        if profile.data:
            user_data = profile.data[0]
            st.session_state.user_plan = user_data.get('tier', 'demo')
            st.session_state.scans_used = user_data.get('monthly_scans_used', 0)
    except:
        st.session_state.user_plan = 'demo'
        st.session_state.scans_used = 0

# Main app
def main():
    if st.session_state.user is None:
        render_login()
    else:
        load_user_data()
        
        # Admin users see admin panel
        if is_admin():
            render_admin_dashboard()
        # Demo users see simplified dashboard
        elif is_demo_user():
            render_demo_dashboard()
        # Regular paid users see full dashboard
        else:
            render_user_dashboard()

def render_login():
    """Login page"""
    
    # Logo in sidebar
    with st.sidebar:
        try:
            st.image("logo.png", width=120)
        except:
            st.markdown('<h1 style="color: #6366f1; font-size: 2.5rem; text-align: center;">🎯</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            <h3 style="margin: 0;">Nexus SEO</h3>
            <p style="color: #6b7280; font-size: 0.8rem;">Intelligence Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="margin: 0;">Nexus SEO Intelligence</h1>
            <p style="color: #6b7280; margin-top: 0.5rem;">AI-Powered SEO Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Demo Access Button
        if st.button("🎮 Try Demo (No Signup Required)", use_container_width=True, type="primary"):
            st.session_state.user = type('User', (), {
                'id': 'demo_user',
                'email': 'demo@demo.com'
            })()
            st.session_state.user_plan = 'demo'
            st.session_state.scans_used = 0
            st.success("✅ Demo mode activated! You have 2 free scans.")
            st.rerun()
        
        st.markdown("<p style='text-align: center; color: #6b7280; margin: 1rem 0;'>OR</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Sign In", use_container_width=True)
                
                if submit and email and password:
                    try:
                        result = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        if result:
                            st.session_state.user = result.user
                            st.success("✅ Signed in!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Login failed: {str(e)}")
        
        with tab2:
            with st.form("signup_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password (min 6 chars)", type="password")
                
                st.info("💡 New accounts start with **Demo** plan (2 free scans)")
                
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit and name and email and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            result = supabase.auth.sign_up({
                                "email": email,
                                "password": password,
                                "options": {
                                    "data": {
                                        "full_name": name,
                                        "plan": "demo"
                                    }
                                }
                            })
                            if result:
                                st.success("✅ Account created! Check email to verify.")
                        except Exception as e:
                            st.error(f"❌ Signup failed: {str(e)}")

def render_demo_dashboard():
    """
    CLEAN DEMO DASHBOARD
    Only shows: Scanner and Results (NO admin features)
    """
    
    with st.sidebar:
        # Logo
        try:
            st.image("logo.png", width=80)
            st.markdown("<h3 style='text-align: center; margin-top: 0.5rem;'>Nexus SEO</h3>", unsafe_allow_html=True)
        except:
            st.markdown("<h2 style='text-align: center; color: #6366f1;'>🎯</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Nexus SEO</h3>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Demo badge
        st.markdown('<span class="plan-badge badge-demo">Demo Plan</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Scans remaining
        scans_left = 2 - st.session_state.scans_used
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; background: #f3f4f6; border-radius: 10px;">
            <div style="font-size: 2rem; font-weight: bold; color: #6366f1;">{scans_left}/2</div>
            <div style="font-size: 0.9rem; color: #6b7280;">Free Scans Left</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # ONLY show logout button (NO admin features for demo)
        if st.button("🚪 Exit Demo", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Main content
    st.title("🎮 Demo Mode")
    
    # Demo banner
    st.markdown(f"""
    <div class="demo-banner">
        <h3 style="margin: 0;">🎯 Welcome to Demo Mode!</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">You have {2 - st.session_state.scans_used} free scans remaining. Upgrade for unlimited access!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ONLY 2 FEATURES FOR DEMO
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); text-align: center; min-height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="font-size: 5rem; margin-bottom: 1.5rem;">🧠</div>
                <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.8rem;">AI Scanner</h2>
                <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.6;">Advanced AI-powered SEO analysis with real-time insights and recommendations</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if can_scan():
            if st.button("🚀 Start Scan", use_container_width=True, type="primary", key="demo_scan"):
                st.switch_page("pages/3_Advanced_Scanner.py")
        else:
            st.error("❌ No scans remaining")
            if st.button("⚡ Upgrade to Continue", use_container_width=True, key="demo_upgrade1"):
                st.switch_page("pages/4_Billing.py")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 3rem 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3); text-align: center; min-height: 350px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="font-size: 5rem; margin-bottom: 1.5rem;">📊</div>
                <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.8rem;">Scan Results</h2>
                <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; line-height: 1.6;">View your previous scan reports and track your SEO improvements over time</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("📂 View Results", use_container_width=True, key="demo_results"):
            st.switch_page("pages/3_Scan_Results.py")
    
    st.markdown("---")
    
    # Upgrade CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2rem; border-radius: 15px; text-align: center; margin-top: 2rem;">
        <h2 style="color: white; margin: 0 0 1rem 0;">Ready for More? 🚀</h2>
        <p style="color: rgba(255,255,255,0.95); font-size: 1.1rem; margin: 0 0 1.5rem 0;">Upgrade to Pro and get unlimited scans, advanced AI features, and priority support!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⚡ View Plans & Pricing", use_container_width=True, type="primary", key="demo_pricing"):
        st.switch_page("pages/4_Billing.py")

def render_admin_dashboard():
    """Admin-only dashboard"""
    
    with st.sidebar:
        # Logo
        try:
            st.image("logo.png", width=160)
        except:
            st.markdown("<h2 style='text-align: center; color: #6366f1;'>🎯</h2>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; margin-top: 0.5rem;'>Nexus SEO</h3>", unsafe_allow_html=True)
        
        st.markdown("## 🔐 ADMIN PANEL")
        st.markdown("---")
        st.markdown(f"**{st.session_state.user.email}**")
        st.markdown("---")
        
        page = st.radio("Admin Menu", [
            "👥 User Management",
            "📊 Analytics",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    st.title("🔐 Admin Dashboard")
    
    if page == "👥 User Management":
        st.markdown("## 👥 User Management")
        
        try:
            users = supabase.table('profiles').select('*').execute()
            
            if users.data:
                st.metric("Total Users", len(users.data))
                
                col1, col2, col3, col4 = st.columns(4)
                
                demo_count = len([u for u in users.data if u.get('tier') == 'demo'])
                pro_count = len([u for u in users.data if u.get('tier') == 'pro'])
                agency_count = len([u for u in users.data if u.get('tier') == 'agency'])
                elite_count = len([u for u in users.data if u.get('tier') == 'elite'])
                
                with col1:
                    st.metric("Demo", demo_count)
                with col2:
                    st.metric("Pro", pro_count)
                with col3:
                    st.metric("Agency", agency_count)
                with col4:
                    st.metric("Elite", elite_count)
                
                st.markdown("---")
                st.markdown("### All Users")
                
                for user in users.data:
                    with st.expander(f"{user.get('email', 'Unknown')} - {user.get('tier', 'demo').upper()}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Email:** {user.get('email')}")
                            st.write(f"**Plan:** {user.get('tier', 'demo')}")
                            st.write(f"**Credits:** {user.get('credits_balance', 0):,}")
                        
                        with col2:
                            st.write(f"**Scans Used:** {user.get('monthly_scans_used', 0)}")
                            st.write(f"**Total Scans:** {user.get('total_scans', 0)}")
                        
                        new_plan = st.selectbox("Change Plan", ['demo', 'pro', 'agency', 'elite'], key=f"plan_{user.get('id')}")
                        if st.button("Update Plan", key=f"update_{user.get('id')}"):
                            supabase.table('profiles').update({'tier': new_plan}).eq('id', user.get('id')).execute()
                            st.success(f"Plan updated to {new_plan}!")
                            st.rerun()
            else:
                st.info("No users yet")
        except Exception as e:
            st.error(f"Error: {e}")
    
    elif page == "📊 Analytics":
        st.markdown("## 📊 Platform Analytics")
        st.warning("🚧 Analytics coming soon!")
    
    elif page == "⚙️ Settings":
        st.markdown("## ⚙️ Settings")
        st.warning("🚧 Settings coming soon!")

def render_user_dashboard():
    """Regular user dashboard (Pro/Agency/Elite)"""
    
    with st.sidebar:
        # Logo
        try:
            st.image("logo.png", width=80)
            st.markdown("<h3 style='text-align: center; margin-top: 0.5rem;'>Nexus SEO</h3>", unsafe_allow_html=True)
        except:
            st.markdown("<h2 style='text-align: center; color: #6366f1;'>🎯</h2>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'>Nexus SEO</h3>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        plan_name = PLANS[st.session_state.user_plan]['name']
        badge_class = f"badge-{st.session_state.user_plan}"
        st.markdown(f'<span class="plan-badge {badge_class}">{plan_name} Plan</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"**{st.session_state.user.email}**")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    st.title(f"Welcome back! 👋")
    st.markdown("### Your SEO Command Center")
    
    st.markdown("---")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">Plan</div>
            <div class="stat-number">{PLANS[st.session_state.user_plan]['name']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        credits = PLANS[st.session_state.user_plan].get('credits', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">Credits</div>
            <div class="stat-number">{credits:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        limit = get_scans_limit()
        limit_text = "∞" if limit == float('inf') else str(int(limit))
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">Scans</div>
            <div class="stat-number">{st.session_state.scans_used}/{limit_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        try:
            scans = supabase.table('scans').select('id').eq('user_id', st.session_state.user.id).execute()
            total = len(scans.data) if scans.data else 0
        except:
            total = 0
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">Total</div>
            <div class="stat-number">{total}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Features
    st.markdown("## 🚀 Main Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2.5rem 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); text-align: center; min-height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="font-size: 4rem; margin-bottom: 1rem;">🧠</div>
                <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.5rem;">Advanced AI Scanner</h2>
                <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Multi-agent AI system analyzing technical SEO, content strategy, and competitive intelligence</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if can_scan():
            if st.button("🚀 Start Advanced Scan", use_container_width=True, type="primary", key="scan_main"):
                st.switch_page("pages/3_Advanced_Scanner.py")
        else:
            st.error(f"❌ Limit reached ({int(get_scans_limit())} scans/month)")
            if st.button("⚡ Upgrade Plan", use_container_width=True, key="upgrade_scan"):
                st.switch_page("pages/4_Billing.py")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2.5rem 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3); text-align: center; min-height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.5rem;">Scan History</h2>
                <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Access all your previous SEO reports, track progress over time, and download detailed insights</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("📂 View History", use_container_width=True, key="history_main"):
            st.switch_page("pages/3_Scan_Results.py")
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 2.5rem 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(250, 112, 154, 0.3); text-align: center; min-height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="font-size: 4rem; margin-bottom: 1rem;">💎</div>
                <h2 style="color: white; margin: 0 0 1rem 0; font-size: 1.5rem;">Upgrade Plan</h2>
                <p style="color: rgba(255,255,255,0.9); font-size: 1rem; line-height: 1.6;">Unlock unlimited scans, advanced AI agents, PDF reports, and premium features</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("⚡ Upgrade Now", use_container_width=True, type="primary", key="upgrade_main"):
            st.switch_page("pages/4_Billing.py")

if __name__ == "__main__":
    main()