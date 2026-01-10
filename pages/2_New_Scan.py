"""
New Scan Page - Enhanced Version
Professional SEO scanning interface with AI analysis
"""

import streamlit as st
import os
import sys
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="New Scan - Nexus SEO", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supabase import create_client

# Import services with error handling
try:
    from services.seo_scanner import SEOScanner
    SCANNER_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ SEO Scanner not available: {e}")
    SCANNER_AVAILABLE = False

try:
    from services.ai_service import analyze_seo_with_ai, is_ai_available, get_quick_tip
    AI_AVAILABLE = is_ai_available()
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ AI service not available")

# ═══════════════════════════════════════════════════════════════════
# Supabase Setup
# ═══════════════════════════════════════════════════════════════════

@st.cache_resource
def get_supabase():
    """Initialize Supabase client"""
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
        if not url or not key:
            st.error("❌ Supabase credentials not found")
            st.stop()
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Supabase connection error: {e}")
        st.stop()

@st.cache_resource
def get_service_supabase():
    """Initialize Supabase client with service role key"""
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if key:
            return create_client(url, key)
    except:
        pass
    return None

supabase = get_supabase()
service_supabase = get_service_supabase() or supabase

# ═══════════════════════════════════════════════════════════════════
# Authentication Check
# ═══════════════════════════════════════════════════════════════════

if 'user' not in st.session_state or not st.session_state.user:
    st.error("🔒 Please log in to access this page")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("← Go to Login", use_container_width=True, type="primary"):
            st.switch_page("app.py")
    st.stop()

user_id = st.session_state.user.id

# ═══════════════════════════════════════════════════════════════════
# Header
# ═══════════════════════════════════════════════════════════════════

st.title("🔍 New SEO Scan")
st.markdown("**Comprehensive website analysis powered by AI**")
st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# Get User Profile
# ═══════════════════════════════════════════════════════════════════

@st.cache_data(ttl=60)
def get_user_profile(user_id):
    """Fetch user profile with caching"""
    try:
        profile = service_supabase.table("profiles").select("*").eq("id", user_id).execute()
        if profile.data and len(profile.data) > 0:
            return profile.data[0]
    except Exception as e:
        print(f"Profile fetch error: {e}")
    
    # Default values
    return {
        'tier': 'demo',
        'monthly_scans_used': 0,
        'monthly_scan_limit': 50,
        'credits_balance': 1000
    }

user_data = get_user_profile(user_id)

# ═══════════════════════════════════════════════════════════════════
# Stats Display
# ═══════════════════════════════════════════════════════════════════

col1, col2, col3, col4 = st.columns(4)

scans_used = user_data.get('monthly_scans_used', 0)
scans_limit = user_data.get('monthly_scan_limit', 50)
scans_remaining = scans_limit - scans_used

with col1:
    st.metric(
        "Scans Used", 
        f"{scans_used}/{scans_limit}",
        delta=f"{scans_remaining} remaining",
        delta_color="normal"
    )

with col2:
    tier = user_data.get('tier', 'demo').upper()
    st.metric("Plan", tier)

with col3:
    credits = user_data.get('credits_balance', 0)
    st.metric("Credits", f"{credits:,}")

with col4:
    ai_status = "✅ Active" if AI_AVAILABLE else "❌ Offline"
    st.metric("AI Analysis", ai_status)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# URL Input Section
# ═══════════════════════════════════════════════════════════════════

st.markdown("### 🎯 Enter Website URL")

col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com or example.com",
        label_visibility="collapsed",
        key="url_input"
    )

with col2:
    scan_button = st.button(
        "🚀 Start Scan",
        type="primary",
        use_container_width=True,
        disabled=not SCANNER_AVAILABLE
    )

# Advanced options
with st.expander("⚙️ Advanced Options"):
    st.info("🚧 Advanced scanning options coming soon!")
    st.markdown("""
    Future features:
    - 📱 Mobile vs Desktop analysis
    - 🌍 Multi-region scanning
    - 🔍 Deep crawl (multiple pages)
    - 📊 Competitor comparison
    """)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# Scan Processing
# ═══════════════════════════════════════════════════════════════════

if scan_button:
    # Validation
    if not url_input or url_input.strip() == "":
        st.error("❌ Please enter a valid URL")
    elif scans_used >= scans_limit:
        st.error(f"❌ Monthly scan limit reached ({scans_limit}/{scans_limit})")
        st.info("💡 Upgrade your plan to get more scans!")
    else:
        # Clear previous scan
        if 'current_scan' in st.session_state:
            del st.session_state.current_scan
        
        url_input = url_input.strip()
        
        # Progress container
        progress_container = st.container()
        
        with progress_container:
            st.markdown(f"### 🔄 Scanning: `{url_input}`")
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize scanner
                status_text.text("🔧 Initializing scanner...")
                progress_bar.progress(10)
                
                scanner = SEOScanner(supabase)
                
                # Perform scan
                status_text.text("🌐 Fetching website data...")
                progress_bar.progress(30)
                
                scan_id, error = scanner.scan_url(user_id, url_input)
                
                if error:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Scan failed: {error}")
                    st.info("💡 Tip: Make sure the URL is correct and the website is accessible")
                else:
                    progress_bar.progress(60)
                    status_text.text("✅ Scan complete! Fetching results...")
                    
                    # Fetch scan results
                    scan_result = service_supabase.table("seo_scans").select("*").eq("id", scan_id).execute()
                    
                    if scan_result.data and len(scan_result.data) > 0:
                        scan_data = scan_result.data[0]
                        progress_bar.progress(70)
                        
                        # Try AI analysis
                        if AI_AVAILABLE:
                            status_text.text("🤖 Generating AI recommendations...")
                            progress_bar.progress(80)
                            
                            try:
                                ai_recommendations = analyze_seo_with_ai(scan_data)
                                
                                if ai_recommendations:
                                    # Update scan with AI recommendations
                                    service_supabase.table('seo_scans').update({
                                        'ai_recommendations': ai_recommendations
                                    }).eq('id', scan_id).execute()
                                    
                                    scan_data['ai_recommendations'] = ai_recommendations
                                    status_text.text("✅ AI analysis complete!")
                                else:
                                    scan_data['ai_recommendations'] = None
                                    status_text.text("⚠️ AI analysis unavailable")
                                    
                            except Exception as e:
                                print(f"AI error: {e}")
                                scan_data['ai_recommendations'] = None
                                status_text.text("⚠️ AI analysis failed")
                        else:
                            scan_data['ai_recommendations'] = None
                        
                        progress_bar.progress(100)
                        status_text.text("🎉 All done!")
                        
                        # Store in session state
                        st.session_state.current_scan = scan_data
                        
                        # Clear cache to update stats
                        get_user_profile.clear()
                        
                        # Success effects
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        progress_bar.empty()
                        status_text.empty()
                        st.error("❌ Failed to retrieve scan results")
                        
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ Unexpected error: {str(e)}")
                print(f"Scan error: {e}")

# ═══════════════════════════════════════════════════════════════════
# Display Scan Results
# ═══════════════════════════════════════════════════════════════════

if 'current_scan' in st.session_state and st.session_state.current_scan:
    scan_data = st.session_state.current_scan
    
    st.markdown("---")
    st.markdown("## 📊 Scan Results")
    st.markdown(f"**URL:** `{scan_data.get('url', 'Unknown')}`")
    st.caption(f"Scanned on {scan_data.get('created_at', 'Unknown')}")
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # Score Overview
    # ═══════════════════════════════════════════════════════════════
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    overall_score = scan_data.get("overall_score", 0)
    
    # Score color and emoji
    if overall_score >= 80:
        score_color = "🟢"
        score_status = "Excellent"
    elif overall_score >= 60:
        score_color = "🟡"
        score_status = "Good"
    elif overall_score >= 40:
        score_color = "🟠"
        score_status = "Needs Work"
    else:
        score_color = "🔴"
        score_status = "Critical"
    
    with col1:
        st.metric(
            "Overall Score",
            f"{score_color} {overall_score}/100",
            delta=score_status,
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Technical",
            f"{scan_data.get('technical_score', 0)}/100"
        )
    
    with col3:
        st.metric(
            "Content",
            f"{scan_data.get('content_score', 0)}/100"
        )
    
    with col4:
        st.metric(
            "Performance",
            f"{scan_data.get('performance_score', 0)}/100"
        )
    
    with col5:
        issues = scan_data.get('issues_detail', {})
        total_issues = (
            len(issues.get('critical', [])) +
            len(issues.get('high', [])) +
            len(issues.get('medium', []))
        )
        st.metric(
            "Issues Found",
            total_issues,
            delta="Fix to improve" if total_issues > 0 else "All clear!",
            delta_color="inverse" if total_issues > 0 else "normal"
        )
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # Issues Breakdown
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown("### 🚨 Issues Detected")
    
    issues = scan_data.get('issues_detail', {})
    
    tab1, tab2, tab3, tab4 = st.tabs([
        f"🔴 Critical ({len(issues.get('critical', []))})",
        f"🟠 High ({len(issues.get('high', []))})",
        f"🟡 Medium ({len(issues.get('medium', []))})",
        f"🟢 Low ({len(issues.get('low', []))})"
    ])
    
    with tab1:
        critical = issues.get('critical', [])
        if critical:
            for issue in critical:
                st.error(issue)
        else:
            st.success("✅ No critical issues found!")
    
    with tab2:
        high = issues.get('high', [])
        if high:
            for issue in high:
                st.warning(issue)
        else:
            st.success("✅ No high priority issues found!")
    
    with tab3:
        medium = issues.get('medium', [])
        if medium:
            for issue in medium:
                st.info(issue)
        else:
            st.success("✅ No medium priority issues found!")
    
    with tab4:
        low = issues.get('low', [])
        if low:
            for issue in low:
                st.info(issue)
        else:
            st.success("✅ No low priority issues found!")
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # Technical Details
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown("### 🔍 Technical Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📝 Meta Information")
        st.markdown(f"**Title:** {scan_data.get('title', 'N/A')[:80]}...")
        st.caption(f"Length: {len(scan_data.get('title', ''))} characters")
        st.markdown(f"**Description:** {scan_data.get('meta_description', 'N/A')[:80]}...")
        st.caption(f"Length: {len(scan_data.get('meta_description', ''))} characters")
    
    with col2:
        st.markdown("#### 📊 Content Stats")
        st.markdown(f"**Word Count:** {scan_data.get('word_count', 0):,}")
        st.markdown(f"**H1 Tags:** {scan_data.get('h1_count', 0)}")
        st.markdown(f"**H2 Tags:** {scan_data.get('h2_count', 0)}")
        st.markdown(f"**Images:** {scan_data.get('image_count', 0)}")
        st.markdown(f"**Links:** {scan_data.get('link_count', 0)}")
    
    with col3:
        st.markdown("#### ⚡ Performance")
        st.markdown(f"**Load Time:** {scan_data.get('load_time_ms', 0)}ms")
        st.markdown(f"**Page Size:** {scan_data.get('page_size_kb', 0)}KB")
        st.markdown(f"**HTTPS:** {'✅ Enabled' if scan_data.get('has_ssl') else '❌ Disabled'}")
        st.markdown(f"**Mobile Friendly:** {'✅ Yes' if scan_data.get('is_mobile_friendly') else '❌ No'}")
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # AI Recommendations
    # ═══════════════════════════════════════════════════════════════
    
    if scan_data.get('ai_recommendations'):
        st.markdown("### 🤖 AI-Powered Recommendations")
        with st.expander("📋 View Full Analysis", expanded=True):
            st.markdown(scan_data['ai_recommendations'])
    elif AI_AVAILABLE:
        st.info("⚠️ AI analysis is available but wasn't generated for this scan. Try scanning again!")
    else:
        st.info("💡 AI analysis is currently unavailable. Enable it in your settings for smarter recommendations!")
    
    st.markdown("---")
    
    # ═══════════════════════════════════════════════════════════════
    # Actions
    # ═══════════════════════════════════════════════════════════════
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📥 Export PDF", use_container_width=True):
            st.info("🚧 PDF export coming soon!")
    
    with col2:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("🚧 Email feature coming soon!")
    
    with col3:
        if st.button("📊 View History", use_container_width=True):
            st.switch_page("pages/Scan_Results.py")
    
    with col4:
        if st.button("🔄 New Scan", use_container_width=True, type="primary"):
            del st.session_state.current_scan
            st.rerun()

# ═══════════════════════════════════════════════════════════════════
# Recent Scans Section
# ═══════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("### 📚 Recent Scans")

try:
    recent = service_supabase.table("seo_scans")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .limit(5)\
        .execute()
    
    if recent.data and len(recent.data) > 0:
        for scan in recent.data:
            score = scan.get("overall_score", 0)
            
            if score >= 80:
                icon = "🟢"
            elif score >= 60:
                icon = "🟡"
            else:
                icon = "🔴"
            
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"{icon} **{scan.get('url', 'Unknown')}**")
            with col2:
                st.markdown(f"Score: **{score}/100**")
            with col3:
                created = scan.get('created_at', '')
                if created:
                    try:
                        date = datetime.fromisoformat(created.replace('Z', '+00:00'))
                        st.caption(date.strftime("%Y-%m-%d"))
                    except:
                        st.caption(created[:10])
            
            st.markdown("---")
    else:
        st.info("📭 No previous scans. Start your first scan above!")
        
except Exception as e:
    st.warning("⚠️ Unable to load recent scans")
    print(f"Recent scans error: {e}")