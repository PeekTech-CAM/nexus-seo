"""
RBAC System - Role-Based Access Control
Manages user tiers and admin privileges
"""

import streamlit as st

# ============================================================================
# TIER DEFINITIONS & FEATURES
# ============================================================================

TIER_FEATURES = {
    'demo': {
        'name': '🆓 Demo',
        'price': 'Free',
        'credits': 1000,
        'scans_per_month': 5,
        'features': [
            '5 scans per month',
            'Basic SEO analysis',
            'Overall score & issues',
            'Limited AI insights',
            'Community support'
        ],
        'hidden_features': [],
        'pages_access': [
            '3_advanced_scanner',
            '2_scan_results',
            '4_billing',
            'check_prices'
        ]
    },
    
    'pro': {
        'name': '⭐ Pro',
        'price': '€49/month',
        'credits': 10000,
        'scans_per_month': 100,
        'features': [
            '100 scans per month',
            'Advanced SEO analysis',
            'Detailed AI recommendations',
            'Competitor analysis',
            'Backlink monitoring',
            'Keyword tracking',
            'PDF report exports',
            'Priority email support',
            'API access (5000 calls/month)'
        ],
        'hidden_features': [],
        'pages_access': [
            '3_advanced_scanner',
            '2_scan_results',
            '4_billing',
            'check_prices',
            'competitor_analysis',
            'backlink_monitor',
            'keyword_tracker'
        ]
    },
    
    'agency': {
        'name': '🚀 Agency',
        'price': '€149/month',
        'credits': 50000,
        'scans_per_month': 500,
        'features': [
            '500 scans per month',
            'Everything in Pro, plus:',
            'White-label reports',
            'Client management dashboard',
            'Team collaboration (5 users)',
            'Custom branding',
            'Automated reporting',
            'Scheduled scans',
            'Advanced analytics',
            'Dedicated account manager',
            'API access (50000 calls/month)',
            'Webhook integrations'
        ],
        'hidden_features': [],
        'pages_access': [
            '3_advanced_scanner',
            '2_scan_results',
            '4_billing',
            'check_prices',
            'competitor_analysis',
            'backlink_monitor',
            'keyword_tracker',
            'client_management',
            'team_dashboard',
            'white_label_reports',
            'scheduled_scans'
        ]
    },
    
    'elite': {
        'name': '💎 Elite',
        'price': '€399/month',
        'credits': 'unlimited',
        'scans_per_month': 'unlimited',
        'features': [
            'Unlimited scans',
            'Everything in Agency, plus:',
            'Unlimited team members',
            'Custom AI model training',
            'Advanced API (unlimited calls)',
            'Custom integrations',
            'Dedicated infrastructure',
            'SLA guarantee (99.9% uptime)',
            '24/7 priority support',
            'Custom feature development',
            'Monthly strategy calls',
            'Direct Slack/Discord channel',
            'Data export & migration tools',
            'Custom reporting templates'
        ],
        'hidden_features': [],
        'pages_access': [
            '3_advanced_scanner',
            '2_scan_results',
            '4_billing',
            'check_prices',
            'competitor_analysis',
            'backlink_monitor',
            'keyword_tracker',
            'client_management',
            'team_dashboard',
            'white_label_reports',
            'scheduled_scans',
            'custom_ai_training',
            'advanced_analytics',
            'api_management',
            'custom_integrations'
        ]
    }
}

# ============================================================================
# ADMIN CONFIGURATION
# ============================================================================

ADMIN_EMAILS = [
    'moroccoboy1990@gmail.com',
    'admin@nexusseo.com',
    # Add more admin emails here
]

ADMIN_ONLY_PAGES = [
    'quick_test',
    'debug_secrets',
    'debug_stripe',
    'diagnostic_tool',
    'secrets_test'
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_admin(user_email):
    """Check if user is an administrator"""
    if not user_email:
        return False
    return user_email.lower() in [email.lower() for email in ADMIN_EMAILS]


def get_user_tier(user_data):
    """Get user's subscription tier"""
    if not user_data:
        return 'demo'
    return user_data.get('tier', 'demo').lower()


def can_access_page(user_email, user_tier, page_name):
    """Check if user can access a specific page"""
    
    # Admins can access everything
    if is_admin(user_email):
        return True
    
    # Regular users cannot access admin-only pages
    if page_name in ADMIN_ONLY_PAGES:
        return False
    
    # Check if page is in user's tier access list
    tier_config = TIER_FEATURES.get(user_tier, TIER_FEATURES['demo'])
    return page_name in tier_config['pages_access']


def get_tier_features(tier):
    """Get features for a specific tier"""
    return TIER_FEATURES.get(tier, TIER_FEATURES['demo'])


def check_feature_access(user_tier, feature_name):
    """Check if user's tier has access to a specific feature"""
    
    # Define feature mappings
    feature_mapping = {
        'competitor_analysis': ['pro', 'agency', 'elite'],
        'backlink_monitor': ['pro', 'agency', 'elite'],
        'keyword_tracking': ['pro', 'agency', 'elite'],
        'white_label': ['agency', 'elite'],
        'team_collaboration': ['agency', 'elite'],
        'custom_ai': ['elite'],
        'unlimited_scans': ['elite'],
        'api_access': ['pro', 'agency', 'elite'],
        'pdf_export': ['pro', 'agency', 'elite'],
        'scheduled_scans': ['agency', 'elite'],
        'custom_integrations': ['elite']
    }
    
    allowed_tiers = feature_mapping.get(feature_name, [])
    return user_tier in allowed_tiers


def show_upgrade_prompt(required_tier, feature_name):
    """Show upgrade prompt when user tries to access premium feature"""
    tier_config = TIER_FEATURES[required_tier]
    
    st.warning(f"""
    ### 🔒 {feature_name} - {tier_config['name']} Feature
    
    This feature requires {tier_config['name']} plan or higher.
    
    **Upgrade to unlock:**
    """)
    
    for feature in tier_config['features'][:5]:
        st.markdown(f"✅ {feature}")
    
    if st.button(f"⭐ Upgrade to {tier_config['name']}", type="primary"):
        try:
            st.switch_page("pages/4_billing.py")
        except Exception as e:
            st.error("Billing page not found")


# ============================================================================
# SIDEBAR NAVIGATION WITH RBAC
# ============================================================================

def render_rbac_sidebar(user_email, user_data):
    """Render sidebar with role-based access control"""
    
    user_tier = get_user_tier(user_data)
    is_user_admin = is_admin(user_email)
    
    with st.sidebar:
        # User info
        st.markdown(f"### 👤 {user_email.split('@')[0]}")
        st.caption(user_email)
        
        tier_config = TIER_FEATURES[user_tier]
        tier_icon = "👑" if is_user_admin else tier_config['name'].split()[0]
        tier_name = "Admin" if is_user_admin else tier_config['name']
        
        st.markdown(f"**{tier_icon} {tier_name}**")
        st.markdown("---")
        
        # Credits and usage
        credits = user_data.get('credits_balance', 0)
        scans_used = user_data.get('monthly_scans_used', 0)
        scan_limit = user_data.get('monthly_scan_limit', 5)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💎 Credits", f"{credits:,}")
        with col2:
            st.metric("📊 Scans", f"{scans_used}/{scan_limit}")
        
        progress = min(scans_used / scan_limit, 1.0) if scan_limit > 0 else 0
        st.progress(progress)
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 🧭 Navigation")
        
        # Home (always visible)
        if st.button("🏠 Home Dashboard", use_container_width=True, key="nav_home", type="primary"):
            try:
                st.switch_page("app.py")
            except:
                st.rerun()
        
        st.markdown("**📍 Main Features**")
        
        # Scanner (all users)
        if st.button("🔍 SEO Scanner", use_container_width=True, key="nav_scanner"):
            try:
                st.switch_page("pages/3_advanced_scanner.py")
            except Exception as e:
                st.error(f"Scanner page not found: {e}")
        
        # Results (all users)
        if st.button("📊 Scan Results", use_container_width=True, key="nav_results"):
            try:
                st.switch_page("pages/2_scan_results.py")
            except Exception as e:
                st.error(f"Results page not found: {e}")
        
        # Billing (all users)
        if st.button("💳 Billing", use_container_width=True, key="nav_billing"):
            try:
                st.switch_page("pages/4_billing.py")
            except Exception as e:
                st.error(f"Billing page not found: {e}")
        
        # Pro Features
        if user_tier in ['pro', 'agency', 'elite'] or is_user_admin:
            st.markdown("---")
            st.markdown("**⭐ Pro Features**")
            
            if st.button("🎯 Competitor Analysis", use_container_width=True, key="nav_competitor"):
                st.info("🚧 Coming soon!")
            
            if st.button("🔗 Backlink Monitor", use_container_width=True, key="nav_backlinks"):
                st.info("🚧 Coming soon!")
            
            if st.button("🔑 Keyword Tracker", use_container_width=True, key="nav_keywords"):
                st.info("🚧 Coming soon!")
        
        # Agency Features
        if user_tier in ['agency', 'elite'] or is_user_admin:
            st.markdown("---")
            st.markdown("**🚀 Agency Features**")
            
            if st.button("👥 Client Management", use_container_width=True, key="nav_clients"):
                st.info("🚧 Coming soon!")
            
            if st.button("📄 White Label Reports", use_container_width=True, key="nav_whitelabel"):
                st.info("🚧 Coming soon!")
            
            if st.button("⏰ Scheduled Scans", use_container_width=True, key="nav_scheduled"):
                st.info("🚧 Coming soon!")
        
        # Elite Features
        if user_tier == 'elite' or is_user_admin:
            st.markdown("---")
            st.markdown("**💎 Elite Features**")
            
            if st.button("🤖 Custom AI Training", use_container_width=True, key="nav_ai"):
                st.info("🚧 Coming soon!")
            
            if st.button("🔌 API Management", use_container_width=True, key="nav_api"):
                st.info("🚧 Coming soon!")
        
        # Admin Section (only for admins)
        if is_user_admin:
            st.markdown("---")
            st.markdown("**👑 Admin Panel**")
            
            admin_pages = [
                ("🧪 Quick Test", "pages/secrets_test.py"),
                ("🔐 Debug Secrets", "pages/diagnostic_tool.py"),
                ("💳 Debug Stripe", "pages/debug_stripe.py"),
                ("💰 Check Prices", "pages/check_prices.py"),
            ]
            
            for label, page_path in admin_pages:
                key = f"nav_{label.lower().replace(' ', '_')}"
                if st.button(label, use_container_width=True, key=key):
                    try:
                        st.switch_page(page_path)
                    except Exception as e:
                        st.warning(f"Page not found: {page_path}")
        
        st.markdown("---")
        
        # Upgrade prompt (if not Elite and not admin)
        if user_tier != 'elite' and not is_user_admin:
            next_tier = {
                'demo': 'pro',
                'pro': 'agency',
                'agency': 'elite'
            }.get(user_tier, 'pro')
            
            next_tier_config = TIER_FEATURES[next_tier]
            
            st.info(f"""
            **🚀 Upgrade to {next_tier_config['name']}**
            
            {next_tier_config['price']}
            
            Unlock more features!
            """)
            
            if st.button("⭐ Upgrade Now", use_container_width=True, type="primary", key="upgrade_sidebar"):
                try:
                    st.switch_page("pages/4_billing.py")
                except:
                    st.error("Billing page not found")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
            st.session_state.user = None
            st.session_state.clear()
            st.rerun()
        
        # Footer
        st.caption("🎯 Nexus SEO Intelligence")
        if is_user_admin:
            st.caption("👑 Admin Access")


# ============================================================================
# PAGE ACCESS GUARD
# ============================================================================

def require_access(page_name, user_email=None, user_tier=None):
    """
    Guard function to check if user can access a page.
    Call this at the top of every page after imports.
    
    Usage:
        from rbac_system import require_access
        require_access("3_advanced_scanner", user_email, user_tier)
    """
    
    if not user_email:
        st.error("🔒 Please sign in to access this page")
        if st.button("Go to Login"):
            try:
                st.switch_page("app.py")
            except:
                st.rerun()
        st.stop()
    
    if not can_access_page(user_email, user_tier, page_name):
        st.error(f"""
        ### 🔒 Access Denied
        
        This page requires a higher subscription tier or admin privileges.
        """)
        
        if st.button("View Plans", type="primary"):
            try:
                st.switch_page("pages/4_billing.py")
            except:
                st.error("Billing page not found")
        
        if st.button("← Back to Home"):
            try:
                st.switch_page("app.py")
            except:
                st.rerun()
        
        st.stop()


# ============================================================================
# FEATURE GATES
# ============================================================================

def feature_gate(feature_name, user_tier, show_upgrade=True):
    """
    Check if user has access to a feature. Show upgrade prompt if not.
    
    Usage:
        if feature_gate('competitor_analysis', user_tier):
            # Show feature
        else:
            # Feature is blocked and upgrade prompt is shown
    """
    
    has_access = check_feature_access(user_tier, feature_name)
    
    if not has_access and show_upgrade:
        # Determine required tier
        required_tiers = {
            'competitor_analysis': 'pro',
            'backlink_monitor': 'pro',
            'keyword_tracking': 'pro',
            'white_label': 'agency',
            'team_collaboration': 'agency',
            'custom_ai': 'elite',
            'unlimited_scans': 'elite'
        }
        
        required_tier = required_tiers.get(feature_name, 'pro')
        show_upgrade_prompt(required_tier, feature_name.replace('_', ' ').title())
    
    return has_access


# ============================================================================
# USAGE TRACKING
# ============================================================================

def track_feature_usage(user_id, feature_name):
    """Track when users try to use premium features"""
    # Log to database for analytics
    # This helps you understand which features drive upgrades
    pass


def check_scan_limit(user_data):
    """Check if user has reached their scan limit"""
    scans_used = user_data.get('monthly_scans_used', 0)
    scan_limit = user_data.get('monthly_scan_limit', 5)
    
    if scans_used >= scan_limit:
        st.error(f"""
        ### 🚫 Scan Limit Reached
        
        You've used all {scan_limit} scans for this month.
        
        **Upgrade to get more scans:**
        - ⭐ Pro: 100 scans/month
        - 🚀 Agency: 500 scans/month  
        - 💎 Elite: Unlimited scans
        """)
        
        if st.button("⭐ Upgrade Now", type="primary"):
            try:
                st.switch_page("pages/4_billing.py")
            except:
                st.error("Billing page not found")
        
        return False
    
    return True