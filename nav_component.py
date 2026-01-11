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
            st.switch_page("app.py")
    
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
            st.switch_page("app.py")
    
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
            st.switch_page("app.py")
        
        st.markdown("---")
        st.markdown("**📍 Main Pages**")
        
        if st.button("🔍 Scanner", use_container_width=True, key="sidebar_scanner"):
            st.switch_page("pages/Advanced_Scanner.py")
        
        if st.button("📊 Results", use_container_width=True, key="sidebar_results"):
            st.switch_page("pages/3_Scan_Results.py")
        
        if st.button("💳 Billing", use_container_width=True, key="sidebar_billing"):
            st.switch_page("pages/4_Billing.py")
        
        if st.button("💰 Prices", use_container_width=True, key="sidebar_prices"):
            st.switch_page("pages/5_Check_Prices.py")
        
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
            st.switch_page("pages/Advanced_Scanner.py")
    
    with col2:
        if st.button("📊 View Results", use_container_width=True, key="footer_results"):
            st.switch_page("pages/3_Scan_Results.py")
    
    with col3:
        if st.button("🏠 Dashboard", use_container_width=True, key="footer_home"):
            st.switch_page("app.py")