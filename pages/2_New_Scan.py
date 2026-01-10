"""
New Scan Page - Complete Fixed Version
With working AI analysis using ai_service
"""

import streamlit as st
from datetime import datetime
import sys
import os

# Page config MUST be first
st.set_page_config(
    page_title="New Scan - Nexus SEO",
    page_icon="🔍",
    layout="wide"
)

# Now we can import other modules
from supabase import create_client

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import services - FIXED: Using ai_service instead of gemini_service
try:
    from services.seo_scanner import SEOScanner
    from services.ai_service import analyze_seo_with_ai
    
    # PDF generation is optional
    try:
        # from services.pdf_generator import generate_seo_report
        PDF_AVAILABLE = True
    except ImportError:
        PDF_AVAILABLE = False
        
except ImportError as e:
    st.error(f"❌ Import error: {str(e)}")
    st.info("Make sure services directory exists with all required files")
    st.stop()

# Supabase Clients
@st.cache_resource
def get_supabase():
    """Get regular Supabase client"""
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            st.error("⚠️ Supabase credentials not configured")
            st.stop()
        
        return create_client(url, key)
    except Exception as e:
        st.error(f"Supabase connection error: {str(e)}")
        st.stop()

@st.cache_resource
def get_service_supabase():
    """Get service role client - OPTIONAL"""
    try:
        url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not key:
            return None
        
        return create_client(url, key)
    except Exception as e:
        return None

supabase = get_supabase()
service_supabase = get_service_supabase()

# If no service client, use regular client
if service_supabase is None:
    service_supabase = supabase

# Check User Login
if 'user' not in st.session_state or st.session_state.user is None:
    st.error("🔒 Please log in first")
    if st.button("← Go to Login"):
        st.switch_page("app.py")
    st.stop()

user_id = st.session_state.user.id

# Page Header
st.title("🔍 New SEO Scan")
st.markdown("Analyze any website for SEO performance and get AI-powered recommendations")
st.markdown("---")

# Fetch User Profile
try:
    profile = service_supabase.table("profiles").select("*").eq("id", user_id).execute()
    
    if not profile.data:
        st.error("❌ User profile not found")
        st.stop()
    
    user_data = profile.data[0]
    
except Exception as e:
    st.warning(f"⚠️ Could not load profile: {str(e)}")
    user_data = {
        'tier': 'demo',
        'monthly_scans_used': 0,
        'monthly_scan_limit': 50,
        'credits_balance': 1000
    }

# Display User Stats
col1, col2, col3 = st.columns(3)

with col1:
    scans_used = user_data.get('monthly_scans_used', 0)
    scan_limit = user_data.get('monthly_scan_limit', 50)
    st.metric("Monthly Scans", f"{scans_used}/{scan_limit}")

with col2:
    tier = user_data.get('tier', 'demo').upper()
    st.metric("Plan", tier)

with col3:
    credits = user_data.get('credits_balance', 0)
    st.metric("Credits", f"{credits:,}")

st.markdown("---")

# Input URL & Start Scan
st.markdown("### 🎯 Enter Website URL")

url_input = st.text_input(
    "Website URL",
    placeholder="https://example.com",
    help="Enter the full URL including https://"
)

# Advanced options
with st.expander("⚙️ Advanced Options"):
    st.info("Advanced scanning options coming soon!")

scan_button = st.button("🚀 Start Scan", type="primary", use_container_width=True)

if scan_button:
    if not url_input:
        st.error("❌ Please enter a URL")
    elif user_data['monthly_scans_used'] >= user_data['monthly_scan_limit']:
        st.error("❌ Monthly scan limit reached! Please upgrade your plan.")
        if st.button("💳 Upgrade Now"):
            st.switch_page("pages/4_Billing.py")
    else:
        # Perform the scan
        with st.spinner(f"🔍 Scanning {url_input}... This may take 30-60 seconds..."):
            try:
                scanner = SEOScanner(supabase)
                scan_id, error = scanner.scan_url(user_id, url_input)
                
                if error:
                    st.error(f"❌ Scan failed: {error}")
                    st.session_state.current_scan = None
                else:
                    st.success("✅ Scan complete!")
                    
                    # Fetch the scan data
                    scan_result = service_supabase.table("scans").select("*").eq("id", scan_id).execute()
                    
                    if scan_result.data:
                        scan_data = scan_result.data[0]
                        
                        # Try AI analysis - FIXED: Using new function name
                        st.info("🤖 Generating AI recommendations...")
                        try:
                            ai_recommendations = analyze_seo_with_ai(scan_data)
                            
                            if ai_recommendations:
                                # Add AI recommendations to scan data
                                scan_data['ai_recommendations'] = ai_recommendations
                                
                                # Update scan in database with AI recommendations
                                service_supabase.table('scans').update({
                                    'ai_recommendations': ai_recommendations
                                }).eq('id', scan_id).execute()
                                
                                st.success("✅ AI analysis complete!")
                            else:
                                st.warning("⚠️ AI analysis unavailable, but scan completed successfully!")
                                scan_data['ai_recommendations'] = None
                                
                        except Exception as ai_error:
                            st.warning(f"⚠️ AI analysis failed: {str(ai_error)}")
                            scan_data['ai_recommendations'] = None
                        
                        # Store in session state
                        st.session_state.current_scan = scan_data
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Could not retrieve scan results")
                        
            except Exception as e:
                st.error(f"❌ Scan error: {str(e)}")
                st.session_state.current_scan = None

# Display Current Scan Results
if 'current_scan' in st.session_state and st.session_state.current_scan:
    scan_data = st.session_state.current_scan
    
    st.markdown("---")
    st.markdown("## 📊 Scan Results")
    
    # Overall score
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score = scan_data.get("overall_score", 0)
        if score >= 80:
            color = "🟢"
            status = "Excellent"
        elif score >= 60:
            color = "🟡"
            status = "Good"
        elif score >= 40:
            color = "🟠"
            status = "Fair"
        else:
            color = "🔴"
            status = "Poor"
        
        st.metric("SEO Score", f"{color} {score}/100")
        st.caption(status)
    
    with col2:
        critical = len(scan_data.get('issues_detail', {}).get('critical', []))
        st.metric("Critical Issues", critical)
    
    with col3:
        warnings = len(scan_data.get('issues_detail', {}).get('high', []))
        st.metric("Warnings", warnings)
    
    with col4:
        opportunities = len(scan_data.get('issues_detail', {}).get('medium', []))
        st.metric("Opportunities", opportunities)
    
    st.markdown("---")
    
    # Key Findings
    st.markdown("### 🔍 Key Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Meta Tags")
        st.markdown(f"**Title:** {scan_data.get('title', 'N/A')[:100]}")
        st.caption(f"Length: {len(scan_data.get('title', ''))} chars")
        
        st.markdown(f"**Description:** {scan_data.get('meta_description', 'N/A')[:100]}...")
        st.caption(f"Length: {len(scan_data.get('meta_description', ''))} chars")
    
    with col2:
        st.markdown("#### 🔧 Technical")
        st.markdown(f"**Load Time:** {scan_data.get('load_time_ms', 0)} ms")
        st.markdown(f"**Page Size:** {scan_data.get('page_size_kb', 0)} KB")
        st.markdown(f"**HTTPS:** {'✅ Yes' if scan_data.get('has_ssl') else '❌ No'}")
        st.markdown(f"**Mobile Friendly:** {'✅ Yes' if scan_data.get('is_mobile_friendly') else '❌ No'}")
    
    # AI Recommendations
    if scan_data.get('ai_recommendations'):
        st.markdown("---")
        st.markdown("### 🤖 AI-Powered Recommendations")
        
        with st.expander("View AI Analysis", expanded=True):
            st.markdown(scan_data['ai_recommendations'])
    
    # Export Actions
    st.markdown("---")
    st.markdown("### 📤 Export & Share")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download PDF Report", use_container_width=True, type="primary"):
            try:
                with st.spinner("🔄 Generating PDF..."):
                    pdf_buffer = generate_seo_report(scan_data, user_data)
                
                st.download_button(
                    label="⬇️ Click to Download",
                    data=pdf_buffer,
                    file_name=f"SEO_Report_{scan_data.get('domain', 'website')}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
    
    with col2:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email functionality coming soon!")
    
    with col3:
        if st.button("🔗 Share Link", use_container_width=True):
            st.info("Sharing functionality coming soon!")
    
    # New Scan Button
    st.markdown("---")
    if st.button("🔄 Run Another Scan", use_container_width=True):
        st.session_state.current_scan = None
        st.rerun()

# Recent Scans History
st.markdown("---")
st.markdown("### 📚 Recent Scans")

try:
    recent_scans = service_supabase.table("scans").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(5).execute()
    
    if recent_scans.data:
        for scan in recent_scans.data:
            score = scan.get("overall_score", 0)
            
            if score >= 80:
                color_icon = "🟢"
            elif score >= 60:
                color_icon = "🟡"
            else:
                color_icon = "🔴"
            
            status = "✅ completed" if score > 0 else "❌ failed"
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{color_icon} {scan.get('url', 'Unknown')}**")
                if score > 0:
                    st.caption(f"Score: {score}/100")
            
            with col2:
                st.caption(status)
    else:
        st.info("📭 No scans yet. Create your first scan above! 👆")
        
except Exception as e:
    st.info("💡 Tips for Better Results")
    
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
