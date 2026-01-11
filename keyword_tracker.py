"""
Keyword Tracker - Track Your Rankings
Monitor keyword positions across search engines
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(page_title="Keyword Tracker", page_icon="🔑", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .keyword-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .rank-up {
        color: #10b981;
        font-weight: 600;
    }
    .rank-down {
        color: #ef4444;
        font-weight: 600;
    }
    .rank-stable {
        color: #6b7280;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'keywords' not in st.session_state:
    st.session_state.keywords = []
if 'tracking_history' not in st.session_state:
    st.session_state.tracking_history = {}

# Header
st.markdown('<div class="main-header">🔑 Keyword Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Monitor your keyword rankings and track progress over time</div>', unsafe_allow_html=True)

# Sidebar - Add Keywords
with st.sidebar:
    st.markdown("### ➕ Add Keywords")
    
    with st.form("add_keyword_form"):
        keyword = st.text_input("Keyword", placeholder="e.g., best SEO tools")
        target_url = st.text_input("Target URL", placeholder="https://example.com/page")
        search_engine = st.selectbox("Search Engine", ["Google", "Bing", "Yahoo"])
        location = st.text_input("Location", placeholder="United States")
        
        if st.form_submit_button("Add Keyword", use_container_width=True):
            if keyword and target_url:
                # Simulate initial ranking
                initial_rank = random.randint(5, 50)
                
                keyword_data = {
                    'keyword': keyword,
                    'url': target_url,
                    'search_engine': search_engine,
                    'location': location,
                    'current_rank': initial_rank,
                    'previous_rank': initial_rank,
                    'best_rank': initial_rank,
                    'added_date': datetime.now(),
                    'search_volume': random.randint(100, 10000),
                    'difficulty': random.randint(1, 100)
                }
                
                st.session_state.keywords.append(keyword_data)
                
                # Initialize tracking history
                if keyword not in st.session_state.tracking_history:
                    st.session_state.tracking_history[keyword] = []
                
                st.success(f"✅ Added: {keyword}")
                st.rerun()
    
    # Bulk Import
    st.markdown("---")
    st.markdown("### 📥 Bulk Import")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'], help="CSV with columns: keyword, url, location")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            for _, row in df.iterrows():
                keyword_data = {
                    'keyword': row['keyword'],
                    'url': row.get('url', ''),
                    'search_engine': row.get('search_engine', 'Google'),
                    'location': row.get('location', 'United States'),
                    'current_rank': random.randint(5, 50),
                    'previous_rank': random.randint(5, 50),
                    'best_rank': random.randint(1, 20),
                    'added_date': datetime.now(),
                    'search_volume': random.randint(100, 10000),
                    'difficulty': random.randint(1, 100)
                }
                st.session_state.keywords.append(keyword_data)
            st.success(f"✅ Imported {len(df)} keywords")
            st.rerun()
        except Exception as e:
            st.error(f"Error importing: {str(e)}")

# Main content
if len(st.session_state.keywords) == 0:
    st.info("👆 Add your first keyword using the sidebar form")
else:
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_keywords = len(st.session_state.keywords)
    top_10_count = sum(1 for k in st.session_state.keywords if k['current_rank'] <= 10)
    avg_rank = sum(k['current_rank'] for k in st.session_state.keywords) / total_keywords
    improved_count = sum(1 for k in st.session_state.keywords if k['current_rank'] < k['previous_rank'])
    
    with col1:
        st.metric("Total Keywords", total_keywords)
    with col2:
        st.metric("Top 10 Rankings", top_10_count)
    with col3:
        st.metric("Average Position", f"{avg_rank:.1f}")
    with col4:
        st.metric("Improved This Week", improved_count)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Rankings", "🔍 Details", "⚙️ Settings"])
    
    with tab1:
        # Performance chart
        st.markdown("### 📈 Ranking Performance")
        
        # Simulate historical data
        dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -1)]
        
        fig = go.Figure()
        
        for kw_data in st.session_state.keywords[:5]:  # Show top 5 keywords
            ranks = []
            current = kw_data['current_rank']
            for i in range(30):
                variation = random.randint(-5, 3)
                rank = max(1, min(100, current + variation))
                ranks.append(rank)
                current = rank
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=ranks,
                mode='lines+markers',
                name=kw_data['keyword'][:30],
                line=dict(width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Ranking Position",
            yaxis=dict(autorange="reversed"),
            height=400,
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Position Distribution")
            
            positions = {
                '1-3': sum(1 for k in st.session_state.keywords if 1 <= k['current_rank'] <= 3),
                '4-10': sum(1 for k in st.session_state.keywords if 4 <= k['current_rank'] <= 10),
                '11-20': sum(1 for k in st.session_state.keywords if 11 <= k['current_rank'] <= 20),
                '21-50': sum(1 for k in st.session_state.keywords if 21 <= k['current_rank'] <= 50),
                '51+': sum(1 for k in st.session_state.keywords if k['current_rank'] > 50)
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(positions.keys()),
                values=list(positions.values()),
                hole=0.4
            )])
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Search Volume vs Difficulty")
            
            df_scatter = pd.DataFrame(st.session_state.keywords)
            fig_scatter = px.scatter(
                df_scatter,
                x='difficulty',
                y='search_volume',
                size='current_rank',
                color='current_rank',
                hover_data=['keyword'],
                labels={'difficulty': 'Keyword Difficulty', 'search_volume': 'Search Volume'},
                height=300
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 All Rankings")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_filter = st.text_input("🔍 Search keywords", placeholder="Filter by keyword")
        with col2:
            engine_filter = st.multiselect("Search Engine", 
                                          options=list(set(k['search_engine'] for k in st.session_state.keywords)),
                                          default=list(set(k['search_engine'] for k in st.session_state.keywords)))
        with col3:
            rank_filter = st.select_slider("Position Range", 
                                          options=['All', '1-10', '11-20', '21-50', '51+'],
                                          value='All')
        
        # Filter keywords
        filtered_keywords = st.session_state.keywords
        
        if search_filter:
            filtered_keywords = [k for k in filtered_keywords if search_filter.lower() in k['keyword'].lower()]
        
        if engine_filter:
            filtered_keywords = [k for k in filtered_keywords if k['search_engine'] in engine_filter]
        
        if rank_filter != 'All':
            if rank_filter == '1-10':
                filtered_keywords = [k for k in filtered_keywords if 1 <= k['current_rank'] <= 10]
            elif rank_filter == '11-20':
                filtered_keywords = [k for k in filtered_keywords if 11 <= k['current_rank'] <= 20]
            elif rank_filter == '21-50':
                filtered_keywords = [k for k in filtered_keywords if 21 <= k['current_rank'] <= 50]
            elif rank_filter == '51+':
                filtered_keywords = [k for k in filtered_keywords if k['current_rank'] > 50]
        
        # Display keywords
        for kw_data in sorted(filtered_keywords, key=lambda x: x['current_rank']):
            rank_change = kw_data['previous_rank'] - kw_data['current_rank']
            
            if rank_change > 0:
                change_class = "rank-up"
                change_icon = "📈"
                change_text = f"+{rank_change}"
            elif rank_change < 0:
                change_class = "rank-down"
                change_icon = "📉"
                change_text = f"{rank_change}"
            else:
                change_class = "rank-stable"
                change_icon = "➖"
                change_text = "0"
            
            with st.expander(f"**#{kw_data['current_rank']}** - {kw_data['keyword']}", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Position", kw_data['current_rank'], 
                             f"{change_text} from last week")
                with col2:
                    st.metric("Best Position", kw_data['best_rank'])
                with col3:
                    st.metric("Search Volume", f"{kw_data['search_volume']:,}")
                with col4:
                    st.metric("Difficulty", f"{kw_data['difficulty']}/100")
                
                st.markdown(f"**URL:** {kw_data['url']}")
                st.markdown(f"**Engine:** {kw_data['search_engine']} | **Location:** {kw_data['location']}")
                st.markdown(f"**Tracking since:** {kw_data['added_date'].strftime('%Y-%m-%d')}")
    
    with tab3:
        st.markdown("### 🔍 Keyword Details")
        
        if st.session_state.keywords:
            selected_kw = st.selectbox(
                "Select keyword to analyze",
                options=[k['keyword'] for k in st.session_state.keywords]
            )
            
            kw_data = next(k for k in st.session_state.keywords if k['keyword'] == selected_kw)
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Rank", kw_data['current_rank'])
            with col2:
                st.metric("Best Rank", kw_data['best_rank'])
            with col3:
                st.metric("Search Volume", f"{kw_data['search_volume']:,}")
            with col4:
                st.metric("Difficulty", f"{kw_data['difficulty']}/100")
            
            # Historical chart
            st.markdown("#### 📈 Position History")
            
            dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(90, 0, -1)]
            ranks = []
            current = kw_data['current_rank']
            
            for i in range(90):
                variation = random.randint(-3, 2)
                rank = max(1, min(100, current + variation))
                ranks.append(rank)
                current = rank
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=ranks,
                mode='lines+markers',
                name='Position',
                fill='tozeroy',
                line=dict(color='#667eea', width=3),
                marker=dict(size=4)
            ))
            
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Position",
                yaxis=dict(autorange="reversed"),
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # SERP Features
            st.markdown("#### 🎯 SERP Features")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Appearing in:**")
                features = ['Featured Snippet', 'People Also Ask', 'Image Pack', 'Video Pack']
                for feature in features:
                    st.checkbox(feature, value=random.choice([True, False]), disabled=True)
            
            with col2:
                st.markdown("**Competitors in SERP:**")
                competitors = ['competitor1.com', 'competitor2.com', 'competitor3.com']
                for comp in competitors:
                    st.write(f"• {comp}")
    
    with tab4:
        st.markdown("### ⚙️ Tracking Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔄 Update Frequency")
            update_freq = st.radio(
                "How often to check rankings",
                options=['Daily', 'Weekly', 'Monthly'],
                index=1
            )
            
            st.markdown("#### 📧 Notifications")
            st.checkbox("Email alerts for rank changes", value=True)
            st.checkbox("Alert on entering top 10", value=True)
            st.checkbox("Alert on leaving top 10", value=True)
            
            alert_threshold = st.slider("Alert on position change", 1, 20, 5)
            st.caption(f"Get notified when position changes by {alert_threshold}+ positions")
        
        with col2:
            st.markdown("#### 📊 Export Data")
            
            if st.button("📥 Export to CSV", use_container_width=True):
                df = pd.DataFrame(st.session_state.keywords)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"keyword_rankings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("#### 🗑️ Manage Keywords")
            
            if st.button("🔄 Refresh All Rankings", use_container_width=True):
                with st.spinner("Updating rankings..."):
                    for kw in st.session_state.keywords:
                        kw['previous_rank'] = kw['current_rank']
                        kw['current_rank'] = max(1, kw['current_rank'] + random.randint(-5, 3))
                    st.success("✅ Rankings updated!")
                    st.rerun()
            
            if st.button("🗑️ Clear All Keywords", type="secondary", use_container_width=True):
                if st.session_state.get('confirm_clear', False):
                    st.session_state.keywords = []
                    st.session_state.tracking_history = {}
                    st.session_state.confirm_clear = False
                    st.success("All keywords cleared")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm deletion")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Set up automated tracking to monitor your rankings without manual checks!")