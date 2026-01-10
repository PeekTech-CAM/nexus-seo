"""
Scan Results Page - Complete Version
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
import json
from datetime import datetime

st.set_page_config(
    page_title="Scan Results - Nexus SEO",
    page_icon="📊",
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
    st.warning("⚠️ Please log in to view scan results")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Get user info
user = st.session_state.user
if isinstance(user, dict):
    user_id = user.get('id')
else:
    user_id = user.id

supabase = get_supabase()

# Header
st.title("📊 SEO Scan Results")
st.markdown("View and analyze your website scans")
st.markdown("---")

# Show detailed report if scan is selected
if 'selected_scan_id' in st.session_state:
    scan_id = st.session_state['selected_scan_id']
    
    # Fetch scan
    if supabase:
        try:
            response = supabase.table('seo_scans').select('*').eq('id', scan_id).single().execute()
            scan = response.data if response.data else None
        except Exception as e:
            st.error(f"Error loading scan: {e}")
            scan = None
    else:
        scan = None
    
    if not scan:
        st.error("Scan not found")
        if st.button("⬅️ Back to List"):
            del st.session_state['selected_scan_id']
            st.rerun()
        st.stop()
    
    st.markdown("## 📊 Detailed Report")
    
    # Back button
    if st.button("⬅️ Back to List"):
        del st.session_state['selected_scan_id']
        st.rerun()
    
    st.markdown("---")
    
    # Display scan details
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**URL:** {scan.get('url')}")
        st.markdown(f"**Scan ID:** `{scan.get('id')[:8]}...`")
    
    with col2:
        status = scan.get('status', 'unknown')
        status_emoji = {'completed': '✅', 'processing': '⏳', 'failed': '❌'}.get(status, '❓')
        st.markdown(f"**Status:** {status_emoji} {status.title()}")
        st.markdown(f"**Created:** {scan.get('created_at', 'Unknown')[:10]}")
    
    with col3:
        score = scan.get('seo_score', 0)
        score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        st.markdown(f"**SEO Score:** {score_color} **{score}/100**")
        
    st.markdown("---")
    
    # Display results
    results = scan.get('results')
    if results:
        if isinstance(results, str):
            try:
                results = json.loads(results)
            except:
                pass
        
        if isinstance(results, dict):
            # Display metrics
            st.markdown("### 📈 Key Metrics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                seo_score = results.get('seo_score', 0)
                st.metric("SEO Score", f"{seo_score}/100")
            
            with col2:
                issues_found = results.get('issues_count', 0)
                st.metric("Issues Found", issues_found)
            
            with col3:
                warnings = results.get('warnings_count', 0)
                st.metric("Warnings", warnings)
            
            with col4:
                opportunities = results.get('opportunities_count', 0)
                st.metric("Opportunities", opportunities)
            
            st.markdown("---")
            
            # Meta tags
            if 'meta_tags' in results:
                st.markdown("### 📝 Meta Tags")
                meta = results['meta_tags']
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Title:** {meta.get('title', 'Missing')}")
                    st.write(f"**Length:** {meta.get('title_length', 0)} chars")
                with col2:
                    st.write(f"**Description:** {meta.get('description', 'Missing')[:100]}...")
                    st.write(f"**Length:** {meta.get('description_length', 0)} chars")
                st.markdown("---")
            
            # Content
            if 'content' in results:
                st.markdown("### 📄 Content Analysis")
                content = results['content']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Word Count", content.get('word_count', 0))
                with col2:
                    st.metric("Paragraphs", content.get('paragraph_count', 0))
                with col3:
                    headings = results.get('headings', {})
                    st.metric("H1 Tags", headings.get('h1_count', 0))
                st.markdown("---")
            
            # Images
            if 'images' in results:
                st.markdown("### 🖼️ Images")
                images = results['images']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Images", images.get('total', 0))
                with col2:
                    st.metric("With Alt Text", images.get('with_alt', 0))
                with col3:
                    st.metric("Missing Alt", images.get('without_alt', 0))
                st.markdown("---")
            
            # Technical
            if 'technical' in results:
                st.markdown("### ⚙️ Technical SEO")
                tech = results['technical']
                col1, col2, col3 = st.columns(3)
                with col1:
                    ssl_status = "✅ Yes" if tech.get('has_ssl') else "❌ No"
                    st.write(f"**HTTPS:** {ssl_status}")
                with col2:
                    st.write(f"**Load Time:** {tech.get('load_time', 0):.2f}s")
                with col3:
                    st.write(f"**Page Size:** {tech.get('page_size', 0) / 1024:.1f} KB")
                st.markdown("---")
            
            # Issues
            if 'issues' in results and results['issues']:
                st.markdown("### ⚠️ Critical Issues")
                for issue in results['issues']:
                    with st.expander(f"🔴 {issue.get('title', 'Issue')}"):
                        st.markdown(issue.get('description', ''))
                st.markdown("---")
            
            # Warnings
            if 'warnings' in results and results['warnings']:
                st.markdown("### ⚡ Warnings")
                for warning in results['warnings']:
                    with st.expander(f"🟡 {warning.get('title', 'Warning')}"):
                        st.markdown(warning.get('description', ''))
                st.markdown("---")
            
            # Recommendations
            if 'recommendations' in results and results['recommendations']:
                st.markdown("### 💡 Recommendations")
                for rec in results['recommendations']:
                    with st.expander(f"💡 {rec.get('title', 'Recommendation')}"):
                        st.markdown(rec.get('description', ''))
                st.markdown("---")
            
            # AI Analysis
            if 'ai_summary' in results and results['ai_summary']:
                st.markdown("### 🤖 AI Analysis")
                st.info(results['ai_summary'])
                
                if 'ai_recommendations' in results and results['ai_recommendations']:
                    for ai_rec in results['ai_recommendations']:
                        with st.expander(f"🤖 {ai_rec.get('title', 'AI Recommendation')}"):
                            st.markdown(ai_rec.get('description', ''))
                st.markdown("---")
            
            # Raw data
            with st.expander("🔍 Raw Data"):
                st.json(results)
        else:
            st.info("Results data is being processed...")
    else:
        st.info("No results available yet. The scan may still be processing.")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Report (PDF)", use_container_width=True):
            st.info("PDF export coming soon!")
    
    with col2:
        if st.button("📧 Email Report", use_container_width=True):
            st.info("Email feature coming soon!")
    
    with col3:
        if st.button("🔄 Re-scan", use_container_width=True):
            st.info("Re-scan feature coming soon!")

else:
    # Fetch user's scans
    scans = []
    if supabase:
        try:
            response = supabase.table('seo_scans')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            
            scans = response.data if response.data else []
        except Exception as e:
            st.error(f"Error loading scans: {e}")

    if not scans:
        st.info("🔍 No scans yet. Create your first scan to get started!")
        if st.button("🎯 New Scan", type="primary"):
            st.switch_page("pages/2_New_Scan.py")
        st.stop()

    # Display scans
    st.markdown(f"### Found {len(scans)} scan(s)")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.selectbox("Status", ["All", "completed", "pending", "failed"])
    with col2:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Score"])
    with col3:
        search = st.text_input("🔍 Search URL")

    # Filter scans
    filtered_scans = scans

    if filter_status != "All":
        filtered_scans = [s for s in filtered_scans if s.get('status') == filter_status]

    if search:
        filtered_scans = [s for s in filtered_scans if search.lower() in s.get('url', '').lower()]

    # Sort scans
    if sort_by == "Date (Oldest)":
        filtered_scans = sorted(filtered_scans, key=lambda x: x.get('created_at', ''))
    elif sort_by == "Score":
        filtered_scans = sorted(filtered_scans, key=lambda x: x.get('seo_score', 0), reverse=True)

    st.markdown("---")

    # Display each scan
    for scan in filtered_scans:
        scan_id = scan.get('id')
        url = scan.get('url', 'N/A')
        status = scan.get('status', 'unknown')
        created_at = scan.get('created_at', '')
        
        # Parse date
        try:
            date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            date_str = date_obj.strftime("%Y-%m-%d %H:%M")
        except:
            date_str = created_at
        
        # Status emoji
        status_emoji = {
            'completed': '✅',
            'pending': '⏳',
            'failed': '❌',
            'processing': '🔄'
        }.get(status, '❓')
        
        # Card layout
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            
            with col1:
                st.markdown(f"### {url}")
                st.caption(f"📅 {date_str}")
            
            with col2:
                score = scan.get('seo_score', 0)
                if score > 0:
                    st.markdown(f"**Score:** {score}/100")
                st.markdown(f"**Status:** {status_emoji} {status.title()}")
            
            with col3:
                if status == 'completed':
                    if st.button("📄 View", key=f"view_{scan_id}"):
                        st.session_state['selected_scan_id'] = scan_id
                        st.rerun()
            
            with col4:
                if st.button("🗑️", key=f"del_{scan_id}"):
                    try:
                        supabase.table('seo_scans').delete().eq('id', scan_id).execute()
                        st.success("Deleted!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.markdown("---")