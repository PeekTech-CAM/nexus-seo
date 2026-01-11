"""
Backlink Monitor - Track Your Backlinks
Monitor new and lost backlinks
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Backlink Monitor - Nexus SEO",
    page_icon="🔗",
    layout="wide"
)

# ============================================================================
# HIDE DEFAULT NAV
# ============================================================================
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebarNav"] {display: none !important;}
    nav[aria-label="Pages"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION
# ============================================================================
from nav_component import add_page_navigation
add_page_navigation("Backlink Monitor", "🔗")

# ============================================================================
# AUTH CHECK
# ============================================================================
from rbac_system import require_access, get_user_tier

if 'user' not in st.session_state or not st.session_state.user:
    st.warning("⚠️ Please log in to access this feature")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_email = st.session_state.user.email
user_tier = get_user_tier(st.session_state.get('user_data', {}))

require_access("backlink_monitor", user_email, user_tier)

# ============================================================================
# HEADER
# ============================================================================
st.title("🔗 Backlink Monitor")
st.markdown("Track and analyze your website's backlinks")
st.markdown("---")

# ============================================================================
# SESSION STATE
# ============================================================================
if 'monitored_domain' not in st.session_state:
    st.session_state.monitored_domain = None
if 'backlinks_data' not in st.session_state:
    st.session_state.backlinks_data = None

# ============================================================================
# MOCK BACKLINK GENERATOR (For Demo)
# ============================================================================
def generate_mock_backlinks(domain):
    """Generate realistic mock backlink data"""
    
    referring_domains = [
        "techcrunch.com", "medium.com", "dev.to", "reddit.com",
        "linkedin.com", "twitter.com", "facebook.com", "instagram.com",
        "youtube.com", "github.com", "stackoverflow.com", "quora.com",
        "wordpress.com", "blogger.com", "tumblr.com", "pinterest.com"
    ]
    
    backlinks = []
    
    for i in range(random.randint(15, 30)):
        ref_domain = random.choice(referring_domains)
        
        # Generate dates
        days_ago = random.randint(1, 90)
        discovered_date = datetime.now() - timedelta(days=days_ago)
        
        # Status
        status = random.choices(
            ['active', 'active', 'active', 'lost'],
            weights=[7, 7, 7, 1]
        )[0]
        
        # Domain authority (mock)
        da = random.randint(20, 95)
        
        # Link type
        link_type = random.choice(['dofollow', 'nofollow'])
        
        backlink = {
            'id': i + 1,
            'source_url': f"https://{ref_domain}/article-{i+1}",
            'source_domain': ref_domain,
            'target_url': f"https://{domain}/page-{random.randint(1,10)}",
            'anchor_text': random.choice([
                domain,
                'click here',
                'read more',
                'learn more',
                'check this out',
                'SEO tips',
                'web development'
            ]),
            'discovered_date': discovered_date.strftime("%Y-%m-%d"),
            'status': status,
            'domain_authority': da,
            'link_type': link_type,
            'page_authority': random.randint(15, 85)
        }
        
        backlinks.append(backlink)
    
    return backlinks

# ============================================================================
# INPUT SECTION
# ============================================================================
if st.session_state.monitored_domain is None:
    
    st.markdown("### 🌐 Enter Your Domain to Monitor")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        domain = st.text_input(
            "Domain Name",
            placeholder="example.com",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🔍 Start Monitoring", type="primary", use_container_width=True):
            if domain:
                with st.spinner("🔍 Discovering backlinks..."):
                    import time
                    time.sleep(2)
                    
                    st.session_state.monitored_domain = domain
                    st.session_state.backlinks_data = generate_mock_backlinks(domain)
                    st.success("✅ Backlinks discovered!")
                    st.rerun()
            else:
                st.error("❌ Please enter a domain")
    
    st.markdown("---")
    
    # Info section
    st.markdown("### ℹ️ What We Monitor")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔍 Discovery**
        - New backlinks
        - Lost backlinks
        - Changed anchors
        """)
    
    with col2:
        st.info("""
        **📊 Metrics**
        - Domain Authority
        - Page Authority
        - Link type (do/nofollow)
        """)
    
    with col3:
        st.info("""
        **🔔 Alerts**
        - New link notifications
        - Lost link alerts
        - Authority changes
        """)

# ============================================================================
# RESULTS SECTION
# ============================================================================
else:
    domain = st.session_state.monitored_domain
    backlinks = st.session_state.backlinks_data
    
    # Top bar
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### 🌐 Monitoring: **{domain}**")
    
    with col2:
        if st.button("🔄 Change Domain"):
            st.session_state.monitored_domain = None
            st.session_state.backlinks_data = None
            st.rerun()
    
    st.markdown("---")
    
    # ========================================================================
    # OVERVIEW METRICS
    # ========================================================================
    active_links = [b for b in backlinks if b['status'] == 'active']
    lost_links = [b for b in backlinks if b['status'] == 'lost']
    
    # Calculate new links (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_links = [
        b for b in active_links 
        if datetime.strptime(b['discovered_date'], "%Y-%m-%d") >= thirty_days_ago
    ]
    
    # Unique domains
    unique_domains = len(set(b['source_domain'] for b in backlinks))
    
    # Average DA
    avg_da = sum(b['domain_authority'] for b in backlinks) / len(backlinks) if backlinks else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Backlinks", len(backlinks))
    
    with col2:
        st.metric("🟢 Active Links", len(active_links))
    
    with col3:
        st.metric("🆕 New (30d)", len(new_links), delta=f"+{len(new_links)}")
    
    with col4:
        st.metric("📉 Lost", len(lost_links), delta=f"-{len(lost_links)}")
    
    st.markdown("---")
    
    # ========================================================================
    # FILTERS
    # ========================================================================
    st.markdown("### 🔍 Filter Backlinks")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Status", ["All", "Active", "Lost"])
    
    with col2:
        link_type_filter = st.selectbox("Link Type", ["All", "Dofollow", "Nofollow"])
    
    with col3:
        da_min = st.slider("Min Domain Authority", 0, 100, 0)
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Date (Newest)", "Date (Oldest)", "DA (High)", "DA (Low)"])
    
    # Apply filters
    filtered_links = backlinks.copy()
    
    if status_filter != "All":
        filtered_links = [b for b in filtered_links if b['status'] == status_filter.lower()]
    
    if link_type_filter != "All":
        filtered_links = [b for b in filtered_links if b['link_type'] == link_type_filter.lower()]
    
    filtered_links = [b for b in filtered_links if b['domain_authority'] >= da_min]
    
    # Sort
    if sort_by == "Date (Newest)":
        filtered_links.sort(key=lambda x: x['discovered_date'], reverse=True)
    elif sort_by == "Date (Oldest)":
        filtered_links.sort(key=lambda x: x['discovered_date'])
    elif sort_by == "DA (High)":
        filtered_links.sort(key=lambda x: x['domain_authority'], reverse=True)
    elif sort_by == "DA (Low)":
        filtered_links.sort(key=lambda x: x['domain_authority'])
    
    st.markdown(f"**Showing {len(filtered_links)} of {len(backlinks)} backlinks**")
    st.markdown("---")
    
    # ========================================================================
    # BACKLINKS TABLE
    # ========================================================================
    st.markdown("### 🔗 Backlinks")
    
    for link in filtered_links[:20]:  # Show first 20
        with st.expander(f"🌐 {link['source_domain']} → DA: {link['domain_authority']} | {link['status'].upper()}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Source:** [{link['source_url']}]({link['source_url']})")
                st.markdown(f"**Target:** {link['target_url']}")
                st.markdown(f"**Anchor Text:** `{link['anchor_text']}`")
            
            with col2:
                st.metric("Domain Authority", link['domain_authority'])
                st.metric("Page Authority", link['page_authority'])
                
                status_badge = "🟢" if link['status'] == 'active' else "🔴"
                st.markdown(f"**Status:** {status_badge} {link['status'].upper()}")
                
                type_badge = "✅" if link['link_type'] == 'dofollow' else "⚠️"
                st.markdown(f"**Type:** {type_badge} {link['link_type'].upper()}")
            
            st.caption(f"Discovered: {link['discovered_date']}")
    
    if len(filtered_links) > 20:
        st.info(f"ℹ️ Showing first 20 of {len(filtered_links)} results. Refine filters to see more.")
    
    st.markdown("---")
    
    # ========================================================================
    # INSIGHTS
    # ========================================================================
    st.markdown("### 💡 Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏆 Top Referring Domains**")
        domain_counts = {}
        for link in active_links:
            domain_counts[link['source_domain']] = domain_counts.get(link['source_domain'], 0) + 1
        
        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for domain, count in top_domains:
            st.markdown(f"- {domain}: **{count}** links")
    
    with col2:
        st.markdown("**📊 Average Metrics**")
        st.metric("Avg Domain Authority", f"{avg_da:.1f}")
        dofollow_count = len([b for b in active_links if b['link_type'] == 'dofollow'])
        st.metric("Dofollow Links", f"{dofollow_count} ({dofollow_count/len(active_links)*100:.0f}%)")
    
    with col3:
        st.markdown("**📈 Growth**")
        st.metric("New Links (7d)", len([b for b in new_links if (datetime.now() - datetime.strptime(b['discovered_date'], "%Y-%m-%d")).days <= 7]))
        st.metric("Lost Links (30d)", len(lost_links))
    
    st.markdown("---")
    
    # Export
    if st.button("📥 Export Backlinks (CSV)", use_container_width=True):
        st.info("CSV export feature coming soon!")