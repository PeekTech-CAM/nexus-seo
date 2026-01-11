"""
NEXUS SEO INTELLIGENCE - Complete SaaS System
Plans: Demo, Pro, Agency, Elite + Admin Panel
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
    "kamal@nexusseo.com",  # Replace with your actual email
    "admin@nexusseo.com"
]

# CSS
st.markdown("""
<style>
    .main { background: #f8fafc; padding: 2rem; }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white; border: none; padding: 0.75rem 2rem;
        border-radius: 10px; font-weight: 600;
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
    .feature-locked {
        opacity: 0.5;
        pointer-events: none;
        position: relative;
    }
    .locked-overlay {
        background: rgba(0,0,0,0.1);
        padding: 1rem;
        border-radius: 10px;
        border: 2px dashed #6b7280;
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

def has_feature(feature):
    """Check if user's plan has a specific feature"""
    user_plan = st.session_state.user_plan
    return feature in PLANS.get(user_plan, {}).get('features', [])

def get_scans_limit():
    """Get scan limit for current plan"""
    limit = PLANS.get(st.session_state.user_plan, {}).get('scans_per_month', 2)
    return limit if limit > 0 else float('inf')

def can_scan():
    """Check if user can perform a scan"""
    if st.session_state.user_plan == 'elite':
        return True
    return st.session_state.scans_used < get_scans_limit()

def feature_gate(feature_name, required_plan='pro'):
    """Decorator/gate to check if feature is available"""
    if not has_feature(feature_name):
        plan_badge = PLANS.get(required_plan, {}).get('name', 'Pro')
        st.warning(f"🔒 This feature requires **{plan_badge}** plan or higher")
        if st.button(f"⚡ Upgrade to {plan_badge}", key=f"upgrade_{feature_name}"):
            st.switch_page("pages/4_Billing.py")
        return False
    return True

# Main app
def main():
    if st.session_state.user is None:
        render_login()
    else:
        # Load user data
        load_user_data()
        
        # Check if admin
        if is_admin():
            render_admin_dashboard()
        else:
            render_user_dashboard()

def render_login():
    """Login page with Demo option"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #6366f1; font-size: 3rem;">🎯</h1>
            <h1>Nexus SEO Intelligence</h1>
            <p style="color: #6b7280;">AI-Powered SEO Analysis Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Demo Access Button
        if st.button("🎮 Try Demo (No Signup Required)", use_container_width=True, type="primary"):
            # Create anonymous demo session
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

def load_user_data():
    """Load user's plan and usage data"""
    try:
        # In demo mode
        if st.session_state.user.id == 'demo_user':
            st.session_state.user_plan = 'demo'
            st.session_state.scans_used = 0
            return
        
        # Load from database
        profile = supabase.table('profiles').select('*').eq('id', st.session_state.user.id).execute()
        
        if profile.data:
            user_data = profile.data[0]
            st.session_state.user_plan = user_data.get('tier', 'demo')
            st.session_state.scans_used = user_data.get('monthly_scans_used', 0)
    except:
        st.session_state.user_plan = 'demo'
        st.session_state.scans_used = 0

def render_admin_dashboard():
    """Admin-only dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔐 ADMIN PANEL")
        st.markdown("---")
        st.markdown(f"**{st.session_state.user.email}**")
        st.markdown("---")
        
        page = st.radio("Admin Menu", [
            "👥 User Management",
            "📊 Analytics",
            "⚙️ Settings",
            "💳 Billing Management"
        ])
        
        st.markdown("---")
        
        if st.button("👤 Switch to User View"):
            render_user_dashboard()
            st.stop()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Admin content
    st.title("🔐 Admin Dashboard")
    
    if page == "👥 User Management":
        render_user_management()
    elif page == "📊 Analytics":
        render_analytics()
    elif page == "⚙️ Settings":
        render_settings()
    elif page == "💳 Billing Management":
        render_billing_management()

def render_user_management():
    """Admin: Manage users"""
    st.markdown("## 👥 User Management")
    
    try:
        # Get all users
        users = supabase.table('profiles').select('*').execute()
        
        if users.data:
            st.metric("Total Users", len(users.data))
            
            # Plan distribution
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
            
            # User list
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
                        st.write(f"**Created:** {user.get('created_at', 'Unknown')[:10]}")
                    
                    # Admin actions
                    new_plan = st.selectbox("Change Plan", ['demo', 'pro', 'agency', 'elite'], key=f"plan_{user.get('id')}")
                    if st.button("Update Plan", key=f"update_{user.get('id')}"):
                        supabase.table('profiles').update({'tier': new_plan}).eq('id', user.get('id')).execute()
                        st.success(f"Plan updated to {new_plan}!")
                        st.rerun()
        else:
            st.info("No users yet")
    except Exception as e:
        st.error(f"Error loading users: {e}")

def render_analytics():
    """Admin: View analytics"""
    st.markdown("## 📊 Platform Analytics")
    
    try:
        # Get scan stats
        scans = supabase.table('scans').select('*').execute()
        
        if scans.data:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Scans", len(scans.data))
            
            with col2:
                # Scans today
                today = datetime.now().date().isoformat()
                today_scans = len([s for s in scans.data if s.get('created_at', '')[:10] == today])
                st.metric("Scans Today", today_scans)
            
            with col3:
                # Active users
                unique_users = len(set([s.get('user_id') for s in scans.data]))
                st.metric("Active Users", unique_users)
        else:
            st.info("No scan data yet")
    except Exception as e:
        st.error(f"Error loading analytics: {e}")

def render_settings():
    """Admin: Platform settings"""
    st.markdown("## ⚙️ Platform Settings")
    
    st.warning("🚧 Settings panel coming soon!")
    
    st.markdown("""
    **Available Settings:**
    - API keys management
    - Feature flags
    - Rate limiting
    - Email templates
    - Branding customization
    """)

def render_billing_management():
    """Admin: Billing management"""
    st.markdown("## 💳 Billing Management")
    
    st.warning("🚧 Billing management coming soon!")
    
    st.markdown("""
    **Features:**
    - View all transactions
    - Manage subscriptions
    - Issue refunds
    - Generate invoices
    """)

def render_user_dashboard():
    """Regular user dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Nexus SEO")
        st.markdown("---")
        
        # Show plan badge
        plan_name = PLANS[st.session_state.user_plan]['name']
        badge_class = f"badge-{st.session_state.user_plan}"
        st.markdown(f'<span class="plan-badge {badge_class}">{plan_name} Plan</span>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"**{st.session_state.user.email}**")
        
        # Show admin notice if applicable
        if is_admin():
            if st.button("🔐 Open Admin Panel", use_container_width=True):
                st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Main dashboard
    st.title(f"Welcome back! 👋")
    st.markdown("### Your SEO Command Center")
    
    # Plan limitations notice
    if st.session_state.user_plan == 'demo':
        st.info(f"🎮 **Demo Mode** - You have **{2 - st.session_state.scans_used}** free scans remaining. Upgrade for unlimited access!")
    
    st.markdown("---")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Plan", PLANS[st.session_state.user_plan]['name'])
    
    with col2:
        credits = PLANS[st.session_state.user_plan].get('credits', 0)
        st.metric("Credits", f"{credits:,}")
    
    with col3:
        limit = get_scans_limit()
        limit_text = "Unlimited" if limit == float('inf') else str(int(limit))
        st.metric("Scans", f"{st.session_state.scans_used}/{limit_text}")
    
    with col4:
        try:
            scans = supabase.table('scans').select('id').eq('user_id', st.session_state.user.id).execute()
            total = len(scans.data) if scans.data else 0
        except:
            total = 0
        st.metric("Total Scans", total)
    
    st.markdown("---")
    
    # Main Features
    st.markdown("## 🚀 Main Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🧠 Advanced AI Scanner")
        st.markdown("Multi-agent AI analysis with comprehensive insights")
        
        if can_scan():
            if st.button("🚀 Start Advanced Scan", use_container_width=True, type="primary"):
                st.switch_page("pages/3_Advanced_Scanner.py")
        else:
            st.error(f"❌ Scan limit reached ({int(get_scans_limit())} scans/month)")
            if st.button("⚡ Upgrade Plan", use_container_width=True):
                st.switch_page("pages/4_Billing.py")
    
    with col2:
        st.markdown("### 📊 Scan History")
        st.markdown("View your previous reports")
        
        if has_feature('basic_scan'):
            if st.button("📂 View History", use_container_width=True):
                st.info("History page coming soon!")
        else:
            st.markdown('<div class="locked-overlay">🔒 Requires Pro Plan</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 💳 Billing")
        st.markdown("Manage your subscription")
        
        if st.button("💎 View Plans", use_container_width=True):
            st.switch_page("pages/4_Billing.py")
    
    st.markdown("---")
    
    # Feature comparison
    st.markdown("## 📋 Your Plan Features")
    
    current_features = PLANS[st.session_state.user_plan]['features']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Available Features")
        feature_names = {
            'basic_scan': 'Basic SEO Scan',
            'ai_analysis': 'AI-Powered Analysis',
            'export_json': 'Export JSON Reports',
            'export_pdf': 'Export PDF Reports',
            'white_label': 'White Label Reports',
            'api_access': 'API Access',
            'priority_support': 'Priority Support',
            'team_collaboration': 'Team Collaboration',
            'custom_ai_training': 'Custom AI Training',
            'dedicated_manager': 'Dedicated Account Manager',
            'custom_integrations': 'Custom Integrations'
        }
        
        for feature in current_features:
            st.success(f"✓ {feature_names.get(feature, feature)}")
    
    with col2:
        if st.session_state.user_plan != 'elite':
            st.markdown("### 🔒 Locked Features")
            all_features = set()
            for plan in PLANS.values():
                all_features.update(plan['features'])
            
            locked = all_features - set(current_features)
            for feature in list(locked)[:5]:
                st.warning(f"🔒 {feature_names.get(feature, feature)}")
            
            if st.button("⚡ Upgrade to Unlock All", use_container_width=True):
                st.switch_page("pages/4_Billing.py")

if __name__ == "__main__":
    main()