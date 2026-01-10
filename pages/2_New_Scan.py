"""
New Scan Page - Minimal Working Version
"""

import streamlit as st
import os
import sys

st.set_page_config(page_title="New Scan", page_icon="🔍", layout="wide")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from supabase import create_client

# Import services with error handling
try:
    from services.seo_scanner import SEOScanner
except:
    st.error("SEO Scanner not available")
    st.stop()

try:
    from services.ai_service import analyze_seo_with_ai
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False
    print("AI service not available")

@st.cache_resource
def get_supabase():
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
    return create_client(url, key)

@st.cache_resource
def get_service_supabase():
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

# Check login
if 'user' not in st.session_state or not st.session_state.user:
    st.error("🔒 Please log in first")
    if st.button("← Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_id = st.session_state.user.id

# Header
st.title("🔍 New SEO Scan")
st.markdown("Analyze any website for SEO performance")
st.markdown("---")

# Get user profile
try:
    profile = service_supabase.table("profiles").select("*").eq("id", user_id).execute()
    user_data = profile.data[0] if profile.data else {
        'tier': 'demo',
        'monthly_scans_used': 0,
        'monthly_scan_limit': 50,
        'credits_balance': 1000
    }
except:
    user_data = {
        'tier': 'demo',
        'monthly_scans_used': 0,
        'monthly_scan_limit': 50,
        'credits_balance': 1000
    }

# Stats
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Scans", f"{user_data.get('monthly_scans_used', 0)}/{user_data.get('monthly_scan_limit', 50)}")
with col2:
    st.metric("Plan", user_data.get('tier', 'demo').upper())
with col3:
    st.metric("Credits", f"{user_data.get('credits_balance', 0):,}")

st.markdown("---")

# Input
st.markdown("### 🎯 Enter Website URL")
url_input = st.text_input("Website URL", placeholder="https://example.com")

with st.expander("⚙️ Advanced Options"):
    st.info("Advanced options coming soon!")

# Scan button
if st.button("🚀 Start Scan", type="primary", use_container_width=True):
    if not url_input:
        st.error("❌ Please enter a URL")
    elif user_data['monthly_scans_used'] >= user_data['monthly_scan_limit']:
        st.error("❌ Monthly limit reached!")
    else:
        with st.spinner(f"🔍 Scanning {url_input}..."):
            try:
                scanner = SEOScanner(supabase)
                scan_id, error = scanner.scan_url(user_id, url_input)
                
                if error:
                    st.error(f"❌ Scan failed: {error}")
                else:
                    st.success("✅ Scan complete!")
                    
                    # Get scan data
                    scan_result = service_supabase.table("scans").select("*").eq("id", scan_id).execute()
                    
                    if scan_result.data:
                        scan_data = scan_result.data[0]
                        
                        # Try AI analysis
                        if AI_AVAILABLE:
                            try:
                                with st.spinner("🤖 Generating AI recommendations..."):
                                    ai_recommendations = analyze_seo_with_ai(scan_data)
                                    
                                if ai_recommendations:
                                    scan_data['ai_recommendations'] = ai_recommendations
                                    service_supabase.table('scans').update({
                                        'ai_recommendations': ai_recommendations
                                    }).eq('id', scan_id).execute()
                                    st.success("✅ AI analysis complete!")
                                else:
                                    st.warning("⚠️ AI analysis unavailable")
                                    scan_data['ai_recommendations'] = None
                            except Exception as e:
                                st.warning(f"⚠️ AI error: {str(e)}")
                                scan_data['ai_recommendations'] = None
                        else:
                            scan_data['ai_recommendations'] = None
                        
                        st.session_state.current_scan = scan_data
                        st.balloons()
                        st.rerun()
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results
if 'current_scan' in st.session_state and st.session_state.current_scan:
    scan_data = st.session_state.current_scan
    
    st.markdown("---")
    st.markdown("## 📊 Scan Results")
    
    # Scores
    col1, col2, col3, col4 = st.columns(4)
    
    score = scan_data.get("overall_score", 0)
    icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    
    with col1:
        st.metric("SEO Score", f"{icon} {score}/100")
    with col2:
        st.metric("Critical Issues", len(scan_data.get('issues_detail', {}).get('critical', [])))
    with col3:
        st.metric("Warnings", len(scan_data.get('issues_detail', {}).get('high', [])))
    with col4:
        st.metric("Opportunities", len(scan_data.get('issues_detail', {}).get('medium', [])))
    
    st.markdown("---")
    
    # Details
    st.markdown("### 🔍 Key Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Meta Tags")
        st.markdown(f"**Title:** {scan_data.get('title', 'N/A')[:100]}")
        st.caption(f"Length: {len(scan_data.get('title', ''))} chars")
    
    with col2:
        st.markdown("#### 🔧 Technical")
        st.markdown(f"**Load Time:** {scan_data.get('load_time_ms', 0)} ms")
        st.markdown(f"**HTTPS:** {'✅' if scan_data.get('has_ssl') else '❌'}")
    
    # AI Recommendations
    if scan_data.get('ai_recommendations'):
        st.markdown("---")
        st.markdown("### 🤖 AI Recommendations")
        with st.expander("View Analysis", expanded=True):
            st.markdown(scan_data['ai_recommendations'])
    
    # Actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📥 PDF export coming soon")
    with col2:
        st.info("📧 Email coming soon")
    with col3:
        if st.button("🔄 New Scan", use_container_width=True):
            st.session_state.current_scan = None
            st.rerun()

# Recent scans
st.markdown("---")
st.markdown("### 📚 Recent Scans")

try:
    recent = service_supabase.table("scans").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(5).execute()
    
    if recent.data:
        for scan in recent.data:
            score = scan.get("overall_score", 0)
            icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            st.markdown(f"{icon} **{scan.get('url', 'Unknown')}** - Score: {score}/100")
    else:
        st.info("📭 No scans yet!")
except:
    st.info("💡 Run your first scan above!")