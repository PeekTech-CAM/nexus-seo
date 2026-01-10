"""
Add this to your main app.py or each page to customize the sidebar
This replaces the default navigation with useful features
"""

import streamlit as st

# Hide default navigation and add custom sidebar
def setup_sidebar():
    """Setup custom sidebar with useful features instead of navigation"""
    
    # Hide default navigation
    st.markdown("""
        <style>
            /* Hide the default navigation */
            [data-testid="stSidebarNav"] {
                display: none;
            }
            
            /* Optional: Hide "No Active Plan" warning if you want */
            .element-container:has(> div > div > div > [data-testid="stNotification"]) {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Add custom sidebar content
    with st.sidebar:
        # Logo/Brand
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("---")
        
        # User info section
        if 'user' in st.session_state and st.session_state.user:
            user = st.session_state.user
            email = user.get('email') if isinstance(user, dict) else user.email
            
            st.markdown("### 👤 Account")
            st.write(f"**{email}**")
            
            # Get user profile stats
            try:
                from supabase import create_client
                url = st.secrets.get("SUPABASE_URL")
                key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_KEY")
                if url and key:
                    supabase = create_client(url, key)
                    user_id = user.get('id') if isinstance(user, dict) else user.id
                    response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
                    if response.data:
                        profile = response.data
                        
                        # Show stats
                        st.markdown("---")
                        st.markdown("### 📊 Your Stats")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Plan", profile.get('tier', 'FREE').upper())
                            st.metric("Credits", f"{profile.get('credits_balance', 0):,}")
                        with col2:
                            scans_used = profile.get('monthly_scans_used', 0)
                            scan_limit = profile.get('monthly_scan_limit', 10)
                            st.metric("Scans", f"{scans_used}/{scan_limit}")
                            usage_pct = int((scans_used / scan_limit) * 100) if scan_limit > 0 else 0
                            st.progress(usage_pct / 100)
            except:
                pass
            
            st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔍 New Scan", use_container_width=True, type="primary"):
            st.switch_page("pages/2_New_Scan.py")
        
        if st.button("📊 View Results", use_container_width=True):
            st.switch_page("pages/3_Scan_Results.py")
        
        if st.button("💳 Upgrade Plan", use_container_width=True):
            st.switch_page("pages/4_Billing.py")
        
        st.markdown("---")
        
        # Settings/Options
        st.markdown("### ⚙️ Settings")
        
        # Theme toggle (optional)
        # st.checkbox("Dark Mode", value=True)
        
        # Notifications
        enable_notifications = st.checkbox("Email Notifications", value=False)
        
        # Auto-save
        auto_save = st.checkbox("Auto-save Reports", value=True)
        
        st.markdown("---")
        
        # Resources
        st.markdown("### 📚 Resources")
        
        with st.expander("Help & Support"):
            st.markdown("""
            - [Documentation](https://docs.example.com)
            - [Video Tutorials](https://youtube.com)
            - [Contact Support](mailto:support@nexusseo.com)
            - [Community Forum](https://forum.example.com)
            """)
        
        with st.expander("Learn SEO"):
            st.markdown("""
            - [SEO Basics Guide](https://example.com/guide)
            - [Best Practices](https://example.com/best-practices)
            - [Case Studies](https://example.com/cases)
            """)
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            # Clear session
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.switch_page("app.py")
        
        # Footer
        st.markdown("---")
        st.caption("Nexus SEO Intelligence v1.0")
        st.caption("© 2025 All rights reserved")


# Alternative: Minimal sidebar (just essentials)
def setup_minimal_sidebar():
    """Minimal sidebar with just account info and quick actions"""
    
    # Hide default navigation
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        st.markdown("---")
        
        # User section
        if 'user' in st.session_state and st.session_state.user:
            user = st.session_state.user
            email = user.get('email') if isinstance(user, dict) else user.email
            st.write(f"👤 {email}")
            st.markdown("---")
        
        # Quick actions only
        st.button("🔍 New Scan", use_container_width=True, type="primary", on_click=lambda: st.switch_page("pages/2_New_Scan.py"))
        st.button("📊 Results", use_container_width=True, on_click=lambda: st.switch_page("pages/3_Scan_Results.py"))
        st.button("💳 Billing", use_container_width=True, on_click=lambda: st.switch_page("pages/4_Billing.py"))
        
        st.markdown("---")
        st.button("🚪 Logout", use_container_width=True, on_click=lambda: [st.session_state.clear(), st.switch_page("app.py")])


# Alternative: Stats-focused sidebar
def setup_stats_sidebar():
    """Sidebar focused on showing user stats and progress"""
    
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("# 🎯 Nexus SEO")
        
        if 'user' in st.session_state and st.session_state.user:
            try:
                from supabase import create_client
                url = st.secrets.get("SUPABASE_URL")
                key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_KEY")
                supabase = create_client(url, key)
                
                user = st.session_state.user
                user_id = user.get('id') if isinstance(user, dict) else user.id
                
                # Get profile
                profile = supabase.table('profiles').select('*').eq('id', user_id).single().execute().data
                
                if profile:
                    st.markdown("---")
                    
                    # Plan badge
                    tier = profile.get('tier', 'FREE').upper()
                    tier_colors = {'FREE': '🔵', 'PRO': '🟢', 'AGENCY': '🟡', 'ELITE': '🟣'}
                    st.markdown(f"## {tier_colors.get(tier, '⚪')} {tier} Plan")
                    
                    # Usage this month
                    st.markdown("### This Month")
                    scans_used = profile.get('monthly_scans_used', 0)
                    scan_limit = profile.get('monthly_scan_limit', 10)
                    
                    st.metric("Scans Used", f"{scans_used} / {scan_limit}")
                    st.progress(scans_used / scan_limit if scan_limit > 0 else 0)
                    
                    st.metric("Credits", f"{profile.get('credits_balance', 0):,}")
                    
                    # Get scan stats
                    scans = supabase.table('seo_scans').select('seo_score').eq('user_id', user_id).eq('status', 'completed').execute().data
                    
                    if scans and len(scans) > 0:
                        avg_score = sum(s.get('seo_score', 0) for s in scans) / len(scans)
                        st.metric("Avg SEO Score", f"{avg_score:.0f}/100")
                        st.metric("Total Scans", len(scans))
                    
                    st.markdown("---")
                    
                    # Quick actions
                    if scans_used >= scan_limit:
                        st.warning("⚠️ Scan limit reached")
                        st.button("💳 Upgrade", use_container_width=True, type="primary", on_click=lambda: st.switch_page("pages/4_Billing.py"))
                    else:
                        st.button("🔍 New Scan", use_container_width=True, type="primary", on_click=lambda: st.switch_page("pages/2_New_Scan.py"))
                    
                    st.button("📊 View Results", use_container_width=True, on_click=lambda: st.switch_page("pages/3_Scan_Results.py"))
                    
            except Exception as e:
                st.error(f"Error loading stats: {e}")
        
        st.markdown("---")
        st.button("🚪 Logout", use_container_width=True)