"""
Competitor Analysis - Full Featured
Compare your website with competitors
"""

import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Competitor Analysis - Nexus SEO",
    page_icon="🎯",
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
add_page_navigation("Competitor Analysis", "🎯")

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

# Check access
require_access("competitor_analysis", user_email, user_tier)

# ============================================================================
# HEADER
# ============================================================================
st.title("🎯 Competitor Analysis")
st.markdown("Compare your website with up to 5 competitors")
st.markdown("---")

# ============================================================================
# SESSION STATE
# ============================================================================
if 'comparison_results' not in st.session_state:
    st.session_state.comparison_results = None

# ============================================================================
# ANALYSIS FUNCTION
# ============================================================================
def analyze_competitor(url):
    """Analyze a competitor website"""
    try:
        # Add https if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Fetch website
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract data
        title = soup.find('title')
        title_text = title.get_text() if title else 'No title'
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else 'No description'
        
        # Count elements
        h1_tags = len(soup.find_all('h1'))
        h2_tags = len(soup.find_all('h2'))
        images = soup.find_all('img')
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        
        links = soup.find_all('a')
        internal_links = len([a for a in links if a.get('href', '').startswith('/')])
        external_links = len(links) - internal_links
        
        # Calculate basic score
        score = 0
        if title_text and len(title_text) > 10:
            score += 15
        if description and len(description) > 50:
            score += 15
        if h1_tags == 1:
            score += 10
        if h2_tags > 0:
            score += 10
        if total_images > 0 and images_with_alt == total_images:
            score += 20
        if internal_links > 10:
            score += 10
        score += min(20, external_links)  # Up to 20 points for external links
        
        return {
            'url': url,
            'status': 'success',
            'score': min(100, score),
            'title': title_text[:60] + '...' if len(title_text) > 60 else title_text,
            'title_length': len(title_text),
            'description': description[:100] + '...' if len(description) > 100 else description,
            'description_length': len(description),
            'h1_count': h1_tags,
            'h2_count': h2_tags,
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'internal_links': internal_links,
            'external_links': external_links,
            'load_time': response.elapsed.total_seconds(),
            'page_size': len(response.content) / 1024  # KB
        }
        
    except Exception as e:
        return {
            'url': url,
            'status': 'error',
            'error': str(e)
        }

# ============================================================================
# INPUT SECTION
# ============================================================================
if st.session_state.comparison_results is None:
    
    st.markdown("### 🌐 Enter Websites to Compare")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        your_url = st.text_input("🏠 Your Website", placeholder="example.com")
    
    with col2:
        st.metric("Competitors", "Up to 5")
    
    st.markdown("#### 🎯 Competitors")
    
    comp_cols = st.columns(3)
    competitors = []
    
    with comp_cols[0]:
        comp1 = st.text_input("Competitor 1", placeholder="competitor1.com", key="comp1")
        if comp1:
            competitors.append(comp1)
        comp2 = st.text_input("Competitor 2", placeholder="competitor2.com", key="comp2")
        if comp2:
            competitors.append(comp2)
    
    with comp_cols[1]:
        comp3 = st.text_input("Competitor 3", placeholder="competitor3.com", key="comp3")
        if comp3:
            competitors.append(comp3)
        comp4 = st.text_input("Competitor 4", placeholder="competitor4.com", key="comp4")
        if comp4:
            competitors.append(comp4)
    
    with comp_cols[2]:
        comp5 = st.text_input("Competitor 5", placeholder="competitor5.com", key="comp5")
        if comp5:
            competitors.append(comp5)
    
    st.markdown("---")
    
    if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
        if not your_url:
            st.error("❌ Please enter your website URL")
        elif not competitors:
            st.error("❌ Please enter at least one competitor")
        else:
            with st.spinner("🔍 Analyzing websites..."):
                results = []
                
                # Analyze your website
                progress_bar = st.progress(0)
                status = st.empty()
                
                status.info(f"Analyzing your website: {your_url}")
                your_data = analyze_competitor(your_url)
                your_data['is_yours'] = True
                results.append(your_data)
                progress_bar.progress(1 / (len(competitors) + 1))
                time.sleep(0.5)
                
                # Analyze competitors
                for i, comp_url in enumerate(competitors):
                    status.info(f"Analyzing competitor: {comp_url}")
                    comp_data = analyze_competitor(comp_url)
                    comp_data['is_yours'] = False
                    results.append(comp_data)
                    progress_bar.progress((i + 2) / (len(competitors) + 1))
                    time.sleep(0.5)
                
                st.session_state.comparison_results = results
                status.empty()
                progress_bar.empty()
                st.success("✅ Analysis complete!")
                st.rerun()

# ============================================================================
# RESULTS SECTION
# ============================================================================
else:
    results = st.session_state.comparison_results
    
    # Back button
    if st.button("🔄 New Comparison", type="secondary"):
        st.session_state.comparison_results = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("## 📊 Comparison Results")
    
    # Filter successful results
    successful_results = [r for r in results if r['status'] == 'success']
    
    if not successful_results:
        st.error("❌ All analyses failed. Please try again with valid URLs.")
        if st.button("Try Again"):
            st.session_state.comparison_results = None
            st.rerun()
        st.stop()
    
    # ========================================================================
    # OVERVIEW SCORES
    # ========================================================================
    st.markdown("### 🏆 SEO Score Comparison")
    
    cols = st.columns(len(successful_results))
    for idx, result in enumerate(successful_results):
        with cols[idx]:
            is_yours = result.get('is_yours', False)
            badge = "🏠 YOU" if is_yours else f"🎯 Comp {idx}"
            
            score = result['score']
            color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            
            st.markdown(f"**{badge}**")
            st.metric(
                label=result['url'].replace('https://', '').replace('http://', '')[:20],
                value=f"{score}/100",
                delta=f"{color}"
            )
    
    st.markdown("---")
    
    # ========================================================================
    # DETAILED COMPARISON TABLE
    # ========================================================================
    st.markdown("### 📋 Detailed Comparison")
    
    # Create comparison data
    metrics = {
        "Metric": [
            "📝 Title Length",
            "📄 Description Length",
            "🏷️ H1 Tags",
            "🏷️ H2 Tags",
            "🖼️ Total Images",
            "✅ Images with Alt",
            "🔗 Internal Links",
            "🌐 External Links",
            "⚡ Load Time (s)",
            "📦 Page Size (KB)"
        ]
    }
    
    for result in successful_results:
        is_yours = result.get('is_yours', False)
        label = "🏠 YOU" if is_yours else result['url'][:20]
        
        metrics[label] = [
            result['title_length'],
            result['description_length'],
            result['h1_count'],
            result['h2_count'],
            result['total_images'],
            result['images_with_alt'],
            result['internal_links'],
            result['external_links'],
            f"{result['load_time']:.2f}",
            f"{result['page_size']:.1f}"
        ]
    
    st.dataframe(metrics, use_container_width=True, height=400)
    
    st.markdown("---")
    
    # ========================================================================
    # KEY INSIGHTS
    # ========================================================================
    st.markdown("### 💡 Key Insights")
    
    your_result = next((r for r in successful_results if r.get('is_yours')), None)
    
    if your_result:
        competitors_results = [r for r in successful_results if not r.get('is_yours')]
        
        # Calculate averages
        avg_comp_score = sum(r['score'] for r in competitors_results) / len(competitors_results) if competitors_results else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            diff = your_result['score'] - avg_comp_score
            if diff > 0:
                st.success(f"✅ You're ahead by {diff:.1f} points!")
            else:
                st.warning(f"⚠️ You're behind by {abs(diff):.1f} points")
        
        with col2:
            if your_result['h1_count'] != 1:
                st.warning("⚠️ Optimize H1 tags (should be exactly 1)")
            else:
                st.success("✅ H1 tags optimized")
        
        with col3:
            alt_ratio = (your_result['images_with_alt'] / your_result['total_images'] * 100) if your_result['total_images'] > 0 else 0
            if alt_ratio < 100:
                st.warning(f"⚠️ Add alt text to {your_result['total_images'] - your_result['images_with_alt']} images")
            else:
                st.success("✅ All images have alt text")
    
    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================
    st.markdown("---")
    st.markdown("### 🎯 Recommendations")
    
    if your_result:
        recommendations = []
        
        if your_result['title_length'] < 30:
            recommendations.append("📝 Increase title length (aim for 50-60 characters)")
        elif your_result['title_length'] > 70:
            recommendations.append("📝 Shorten title length (aim for 50-60 characters)")
        
        if your_result['description_length'] < 120:
            recommendations.append("📄 Expand meta description (aim for 150-160 characters)")
        
        if your_result['h1_count'] == 0:
            recommendations.append("🏷️ Add an H1 tag to your page")
        elif your_result['h1_count'] > 1:
            recommendations.append("🏷️ Use only one H1 tag per page")
        
        if your_result['images_with_alt'] < your_result['total_images']:
            recommendations.append(f"🖼️ Add alt text to {your_result['total_images'] - your_result['images_with_alt']} images")
        
        if your_result['internal_links'] < 10:
            recommendations.append("🔗 Add more internal links (aim for 10+)")
        
        if your_result['load_time'] > 3:
            recommendations.append("⚡ Optimize page load time (currently > 3 seconds)")
        
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("🎉 Great job! No critical issues found.")
    
    st.markdown("---")
    
    # Export button
    if st.button("📥 Export Report (PDF)", use_container_width=True):
        st.info("PDF export feature coming soon!")