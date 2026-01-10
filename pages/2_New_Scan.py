"""
New Scan Page - Complete Version
"""

import streamlit as st

# HIDE NAVIGATION - MUST BE FIRST
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {display: none !important;}
    section[data-testid="stSidebar"] > div:first-child {display: none !important;}
</style>
""", unsafe_allow_html=True)

from supabase import create_client
import sys
from pathlib import Path
import json
from datetime import datetime
import uuid
import os  # Add this import

# Add services to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from services.seo_scanner import scan_website
    from services.gemini_service import analyze_with_ai
except ImportError:
    st.error("⚠️ Scanner services not found. Make sure services/seo_scanner.py and services/gemini_service.py exist.")
    st.stop()

st.set_page_config(
    page_title="New Scan - Nexus SEO",
    page_icon="🔍",
    layout="wide"
)

@st.cache_resource
def get_supabase():
    """Initialize Supabase client"""
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get("SUPABASE_KEY")
        if url and key:
            return create_client(url, key)
        return None
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

# Check authentication
if 'user' not in st.session_state or not st.session_state.user:
    st.warning("⚠️ Please log in to create scans")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Get user info
user = st.session_state.user
if isinstance(user, dict):
    user_id = user.get('id')
    user_email = user.get('email')
else:
    user_id = user.id
    user_email = user.email

supabase = get_supabase()

# Header
st.title("🔍 New SEO Scan")
st.markdown("Analyze any website for SEO performance and get AI-powered recommendations")
st.markdown("---")

# Get user profile
user_profile = None
if supabase:
    try:
        response = supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        user_profile = response.data if response.data else None
    except:
        pass

# Show current usage
if user_profile:
    col1, col2, col3 = st.columns(3)
    with col1:
        scans_used = user_profile.get('monthly_scans_used', 0)
        scan_limit = user_profile.get('monthly_scan_limit', 10)
        st.metric("Scans This Month", f"{scans_used}/{scan_limit}")
    with col2:
        credits = user_profile.get('credits_balance', 0)
        st.metric("Available Credits", f"{credits:,}")
    with col3:
        tier = user_profile.get('tier', 'FREE').upper()
        st.metric("Current Plan", tier)
    
    st.markdown("---")

# Scan form
st.markdown("### 🎯 Enter Website URL")

col1, col2 = st.columns([3, 1])

with col1:
    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        help="Enter the full URL including https://",
        label_visibility="collapsed"
    )

with col2:
    scan_button = st.button("🚀 Start Scan", type="primary", use_container_width=True)

# Advanced options
with st.expander("⚙️ Advanced Options"):
    col1, col2 = st.columns(2)
    
    with col1:
        include_ai = st.checkbox("Include AI Analysis", value=True, help="Get AI-powered recommendations (uses Gemini Pro)")
        check_mobile = st.checkbox("Mobile Analysis", value=True)
    
    with col2:
        check_performance = st.checkbox("Performance Check", value=True)
        deep_scan = st.checkbox("Deep Scan", value=False, help="More detailed analysis (takes longer)")

# Run scan
if scan_button:
    if not url_input:
        st.error("⚠️ Please enter a URL")
    elif not url_input.startswith(('http://', 'https://')):
        st.error("⚠️ URL must start with http:// or https://")
    else:
        # Check if user has scans remaining
        if user_profile:
            scans_used = user_profile.get('monthly_scans_used', 0)
            scan_limit = user_profile.get('monthly_scan_limit', 10)
            
            if scans_used >= scan_limit:
                st.error("❌ You've reached your monthly scan limit")
                st.info("💡 Upgrade your plan to get more scans")
                if st.button("View Plans"):
                    st.switch_page("pages/4_Billing.py")
                st.stop()
        
        # Create scan record
        scan_id = str(uuid.uuid4())
        
        if supabase:
            try:
                scan_data = {
                    'id': scan_id,
                    'user_id': user_id,
                    'url': url_input,
                    'status': 'processing',
                    'created_at': datetime.utcnow().isoformat()
                }
                
                insert_result = supabase.table('seo_scans').insert(scan_data).execute()
                
                if not insert_result.data:
                    st.error("❌ Failed to create scan record")
                    st.stop()
                
            except Exception as e:
                st.error(f"❌ Database error: {str(e)}")
                st.stop()
        
        # Run the scan
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Fetch and analyze
            status_text.text("🌐 Fetching website...")
            progress_bar.progress(20)
            
            scan_results = scan_website(url_input)
            
            if 'error' in scan_results:
                st.error(f"❌ Scan failed: {scan_results['error']}")
                
                if supabase:
                    supabase.table('seo_scans').update({
                        'status': 'failed',
                        'error': scan_results['error']
                    }).eq('id', scan_id).execute()
                
                st.stop()
            
            status_text.text("📊 Analyzing SEO metrics...")
            progress_bar.progress(50)
            
            # Step 2: AI Analysis
            if include_ai:
                status_text.text("🤖 Running AI analysis with Gemini Pro...")
                progress_bar.progress(70)
                
                try:
                    # Try multiple key names
                    gemini_key = (
                        st.secrets.get("GEMINI_API_KEY") or 
                        st.secrets.get("GOOGLE_API_KEY") or
                        os.getenv("GEMINI_API_KEY") or
                        os.getenv("GOOGLE_API_KEY")
                    )
                    
                    if gemini_key:
                        st.write(f"🔑 Found API key: {gemini_key[:10]}...{gemini_key[-5:]}")
                        ai_analysis = analyze_with_ai(scan_results, gemini_key)
                        
                        if ai_analysis.get('success'):
                            scan_results['ai_analysis'] = ai_analysis
                            scan_results['ai_recommendations'] = ai_analysis.get('ai_recommendations', [])
                            scan_results['ai_summary'] = ai_analysis.get('ai_summary', '')
                            st.success("✅ AI analysis completed!")
                        else:
                            error_msg = ai_analysis.get('error', 'Unknown error')
                            st.warning(f"⚠️ AI analysis failed: {error_msg}")
                    else:
                        st.warning("⚠️ Gemini API key not found. Checked: GEMINI_API_KEY, GOOGLE_API_KEY")
                        st.info("Add GEMINI_API_KEY to .streamlit/secrets.toml")
                
                except Exception as e:
                    st.warning(f"⚠️ AI analysis error: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
            
            progress_bar.progress(90)
            status_text.text("💾 Saving results...")
            
            # Step 3: Save to database
            if supabase:
                try:
                    update_data = {
                        'status': 'completed',
                        'results': json.dumps(scan_results),
                        'seo_score': scan_results.get('seo_score', 0),
                        'completed_at': datetime.utcnow().isoformat()
                    }
                    
                    supabase.table('seo_scans').update(update_data).eq('id', scan_id).execute()
                    
                    # Update user stats
                    current_scans = user_profile.get('monthly_scans_used', 0) if user_profile else 0
                    supabase.table('profiles').update({
                        'monthly_scans_used': current_scans + 1
                    }).eq('id', user_id).execute()
                    
                except Exception as e:
                    st.error(f"Error saving results: {e}")
            
            progress_bar.progress(100)
            status_text.text("✅ Scan complete!")
            
            # Show success
            st.success("🎉 Scan completed successfully!")
            
            # Quick summary
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score = scan_results.get('seo_score', 0)
                score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.metric("SEO Score", f"{score_color} {score}/100")
            
            with col2:
                issues = scan_results.get('issues_count', 0)
                st.metric("Critical Issues", issues)
            
            with col3:
                warnings = scan_results.get('warnings_count', 0)
                st.metric("Warnings", warnings)
            
            with col4:
                opportunities = scan_results.get('opportunities_count', 0)
                st.metric("Opportunities", opportunities)
            
            st.markdown("---")
            
            # Key findings
            st.markdown("### 🔍 Key Findings")
            
            meta = scan_results.get('meta_tags', {})
            with st.expander("📝 Meta Tags", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Title:** {meta.get('title', 'Missing')}")
                    st.write(f"**Length:** {meta.get('title_length', 0)} chars")
                with col2:
                    desc = meta.get('description', 'Missing')
                    st.write(f"**Description:** {desc[:100]}...")
                    st.write(f"**Length:** {meta.get('description_length', 0)} chars")
            
            # AI Summary
            if 'ai_summary' in scan_results and scan_results['ai_summary']:
                with st.expander("🤖 AI Analysis Summary", expanded=True):
                    st.info(scan_results['ai_summary'])
            
            # Action buttons
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 View Full Report", type="primary", use_container_width=True):
                    st.session_state['selected_scan_id'] = scan_id
                    st.switch_page("pages/3_Scan_Results.py")
            
            with col2:
                if st.button("📥 Download PDF", use_container_width=True):
                    st.info("📄 PDF export feature coming soon!")
            
            with col3:
                if st.button("🔄 Scan Another", use_container_width=True):
                    st.rerun()
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ An error occurred: {str(e)}")
            
            if supabase:
                try:
                    supabase.table('seo_scans').update({
                        'status': 'failed',
                        'error': str(e)
                    }).eq('id', scan_id).execute()
                except:
                    pass

# Recent scans
st.markdown("---")
st.markdown("### 📚 Recent Scans")

if supabase:
    try:
        response = supabase.table('seo_scans')\
            .select('id, url, seo_score, status, created_at')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(5)\
            .execute()
        
        recent_scans = response.data if response.data else []
        
        if recent_scans:
            for scan in recent_scans:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{scan.get('url', 'Unknown')}**")
                
                with col2:
                    score = scan.get('seo_score', 0)
                    if score > 0:
                        st.write(f"Score: {score}/100")
                    else:
                        st.write("-")
                
                with col3:
                    status = scan.get('status', 'unknown')
                    status_emoji = {'completed': '✅', 'processing': '⏳', 'failed': '❌'}.get(status, '❓')
                    st.write(f"{status_emoji} {status}")
                
                with col4:
                    if st.button("View", key=f"view_{scan['id']}", use_container_width=True):
                        st.session_state['selected_scan_id'] = scan['id']
                        st.switch_page("pages/3_Scan_Results.py")
        else:
            st.info("📭 No previous scans. Create your first scan above!")
    
    except Exception as e:
        st.warning(f"Could not load recent scans: {e}")

# Footer tips
st.markdown("---")
st.markdown("### 💡 Tips for Better Results")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Before Scanning:**
    - Make sure the website is publicly accessible
    - Use the full URL (including https://)
    - Check that the page loads correctly
    """)

with col2:
    st.markdown("""
    **After Scanning:**
    - Review all recommendations carefully
    - Prioritize critical issues first
    - Track improvements over time
    """)