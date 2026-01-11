"""
nav_component.py
Universal Navigation Component for all pages
Place this file in the root of your project
"""

import streamlit as st

def add_page_navigation(page_title, page_icon="📄"):
    """
    Universal navigation component for all pages.
    Shows: Back button | Breadcrumb | Home button
    
    Args:
        page_title: Name of current page (e.g., "Check Prices")
        page_icon: Emoji icon for the page (e.g., "💰")
    
    Usage:
        from nav_component import add_page_navigation
        add_page_navigation("Check Prices", "💰")
    """
    
    # Update current page in session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = page_title.lower().replace(" ", "_")
    
    # Navigation bar with breadcrumb and buttons
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col1:
        if st.button("⬅️ Back", key="back_to_home", use_container_width=True, type="secondary"):
            st.session_state.current_page = 'home'
            try:
                st.switch_page("app.py")
            except Exception:
                st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 0.5rem;">
            <span style="color: #666;">🏠 Home</span>
            <span style="color: #999;"> / </span>
            <span style="color: #333; font-weight: 600;">{page_icon} {page_title}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🏠 Home", key="go_home", use_container_width=True, type="primary"):
            st.session_state.current_page = 'home'
            try:
                st.switch_page("app.py")
            except Exception:
                st.rerun()
    
    st.markdown("---")


def add_sidebar_navigation():
    """
    Optional: Add quick navigation in sidebar
    Useful for pages that want additional navigation options
    
    Usage:
        from nav_component import add_sidebar_navigation
        add_sidebar_navigation()
    """
    with st.sidebar:
        st.markdown("### 🧭 Quick Navigation")
        
        if st.button("🏠 Dashboard", use_container_width=True, key="sidebar_home"):
            try:
                st.switch_page("app.py")
            except Exception:
                st.rerun()
        
        st.markdown("---")
        st.markdown("**📍 Main Pages**")
        
        # Updated page paths to match your actual file names
        nav_items = [
            ("🔍 Scanner", "pages/1_dashboard.py"),
            ("🎯 SEO Scanner", "pages/2_seo_scanner.py"),
            ("📊 Scan Results", "pages/2_scan_results.py"),
            ("🔍 Advanced Scanner", "pages/3_advanced_scanner.py"),
            ("💳 Billing", "pages/4_billing.py"),
            ("🔍 Check Prices", "pages/check_prices.py"),
        ]
        
        for label, page_path in nav_items:
            # Create unique key from label
            key = f"sidebar_{label.replace(' ', '_').lower()}"
            if st.button(label, use_container_width=True, key=key):
                try:
                    st.switch_page(page_path)
                except Exception as e:
                    st.error(f"Page not found: {page_path}")
        
        st.markdown("---")
        st.caption("🎯 Nexus SEO Intelligence")


def add_footer_quick_actions():
    """
    Optional: Add quick action buttons at bottom of page
    
    Usage:
        from nav_component import add_footer_quick_actions
        add_footer_quick_actions()
    """
    st.markdown("---")
    st.markdown("### 🎯 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 New Scan", use_container_width=True, key="footer_scan"):
            try:
                st.switch_page("pages/2_seo_scanner.py")
            except Exception:
                st.error("Scanner page not found")
    
    with col2:
        if st.button("📊 View Results", use_container_width=True, key="footer_results"):
            try:
                st.switch_page("pages/2_scan_results.py")
            except Exception:
                st.error("Results page not found")
    
    with col3:
        if st.button("🏠 Dashboard", use_container_width=True, key="footer_home"):
            try:
                st.switch_page("app.py")
            except Exception:
                st.rerun()


def get_user_info():
    """
    Helper function to get current user info from session state
    Returns user object or None
    """
    if 'user' in st.session_state:
        return st.session_state.user
    return None


def require_auth(redirect_to="app.py"):
    """
    Helper function to require authentication
    Redirects to login if user is not authenticated
    
    Usage:
        from nav_component import require_auth
        require_auth()  # At top of protected pages
    """
    if 'user' not in st.session_state or not st.session_state.user:
        st.warning("⚠️ Please log in to access this page")
        if st.button("Go to Login", type="primary"):
            try:
                st.switch_page(redirect_to)
            except Exception:
                st.rerun()
        st.stop()
    
    return st.session_state.user


def add_user_menu():
    """
    Add user menu to sidebar with profile info and logout
    
    Usage:
        from nav_component import add_user_menu
        add_user_menu()
    """
    user = get_user_info()
    
    if user:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 User Menu")
            
            # Show user email
            if isinstance(user, dict):
                email = user.get('email', 'Unknown')
                tier = user.get('tier', 'FREE').upper()
            else:
                email = getattr(user, 'email', 'Unknown')
                tier = 'FREE'
            
            st.markdown(f"**Email:** {email}")
            st.markdown(f"**Plan:** {tier}")
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True, type="secondary", key="sidebar_logout"):
                # Clear session state
                st.session_state.clear()
                st.success("Logged out successfully!")
                try:
                    st.switch_page("app.py")
                except Exception:
                    st.rerun()