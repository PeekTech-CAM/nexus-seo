"""
Advanced Analytics - Deep SEO Insights
Comprehensive analytics and data visualization for advanced users
"""

import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="Advanced Analytics", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .correlation-high {
        background: #10b981;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .correlation-medium {
        background: #f59e0b;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    .correlation-low {
        background: #6b7280;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analytics_data' not in st.session_state:
    # Generate sample historical data
    dates = [(datetime.now() - timedelta(days=x)) for x in range(90, 0, -1)]
    
    st.session_state.analytics_data = {
        'dates': [d.strftime('%Y-%m-%d') for d in dates],
        'organic_traffic': [random.randint(1000, 5000) + i*10 for i in range(90)],
        'keyword_rankings': [random.randint(100, 300) + i*2 for i in range(90)],
        'backlinks': [random.randint(500, 1500) + i*5 for i in range(90)],
        'domain_authority': [random.randint(40, 60) + (i//10) for i in range(90)],
        'page_speed': [random.uniform(2.0, 5.0) for _ in range(90)],
        'bounce_rate': [random.uniform(35, 65) for _ in range(90)],
        'conversion_rate': [random.uniform(2, 8) for _ in range(90)],
        'avg_session_duration': [random.randint(120, 300) for _ in range(90)]
    }

# Header
st.markdown('<div class="main-header">📊 Advanced Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Deep insights and comprehensive data analysis for your SEO strategy</div>', unsafe_allow_html=True)

# AI Insights banner
st.markdown("""
<div class="insight-card">
    <h3 style="margin: 0; margin-bottom: 0.5rem;">🤖 AI-Powered Insights</h3>
    <p style="margin: 0; opacity: 0.95;">
        Your organic traffic increased 23% this month. Top contributing factors: 
        improved keyword rankings (+18 positions avg), new backlinks (+145), and 
        enhanced page speed (-0.8s avg load time).
    </p>
</div>
""", unsafe_allow_html=True)

# Summary metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    current_traffic = st.session_state.analytics_data['organic_traffic'][-1]
    prev_traffic = st.session_state.analytics_data['organic_traffic'][-30]
    traffic_change = ((current_traffic - prev_traffic) / prev_traffic) * 100
    st.metric("Organic Traffic", f"{current_traffic:,}", f"{traffic_change:+.1f}%")

with col2:
    current_keywords = st.session_state.analytics_data['keyword_rankings'][-1]
    prev_keywords = st.session_state.analytics_data['keyword_rankings'][-30]
    keywords_change = current_keywords - prev_keywords
    st.metric("Keywords Ranking", current_keywords, f"{keywords_change:+d}")

with col3:
    current_backlinks = st.session_state.analytics_data['backlinks'][-1]
    prev_backlinks = st.session_state.analytics_data['backlinks'][-30]
    backlinks_change = current_backlinks - prev_backlinks
    st.metric("Total Backlinks", f"{current_backlinks:,}", f"{backlinks_change:+d}")

with col4:
    current_da = st.session_state.analytics_data['domain_authority'][-1]
    prev_da = st.session_state.analytics_data['domain_authority'][-30]
    da_change = current_da - prev_da
    st.metric("Domain Authority", current_da, f"{da_change:+d}")

with col5:
    current_conversion = st.session_state.analytics_data['conversion_rate'][-1]
    prev_conversion = st.session_state.analytics_data['conversion_rate'][-30]
    conversion_change = current_conversion - prev_conversion
    st.metric("Conversion Rate", f"{current_conversion:.1f}%", f"{conversion_change:+.1f}%")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Overview", 
    "🔍 Deep Dive", 
    "🎯 Correlations", 
    "📊 Cohort Analysis",
    "🌊 Funnel Analysis",
    "🤖 Predictive"
])

with tab1:
    st.markdown("### 📈 Performance Overview")
    
    # Time range selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        time_range = st.selectbox(
            "Time Range",
            options=['Last 7 Days', 'Last 30 Days', 'Last 90 Days', 'Last 6 Months', 'Last Year'],
            index=2
        )
    
    with col2:
        comparison = st.checkbox("Compare periods", value=False)
    
    # Multi-metric chart
    st.markdown("#### 📊 Key Metrics Trend")
    
    metrics_to_show = st.multiselect(
        "Select metrics to display",
        options=['Organic Traffic', 'Keyword Rankings', 'Backlinks', 'Domain Authority'],
        default=['Organic Traffic', 'Keyword Rankings']
    )
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
    
    for i, metric in enumerate(metrics_to_show):
        metric_key = {
            'Organic Traffic': 'organic_traffic',
            'Keyword Rankings': 'keyword_rankings',
            'Backlinks': 'backlinks',
            'Domain Authority': 'domain_authority'
        }[metric]
        
        fig.add_trace(
            go.Scatter(
                x=st.session_state.analytics_data['dates'],
                y=st.session_state.analytics_data[metric_key],
                mode='lines+markers',
                name=metric,
                line=dict(color=colors[i], width=2),
                marker=dict(size=4)
            ),
            secondary_y=(i % 2 == 1)
        )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Growth metrics
    st.markdown("#### 📈 Growth Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Traffic Growth**")
        
        growth_30d = ((st.session_state.analytics_data['organic_traffic'][-1] - 
                      st.session_state.analytics_data['organic_traffic'][-30]) / 
                      st.session_state.analytics_data['organic_traffic'][-30]) * 100
        
        growth_90d = ((st.session_state.analytics_data['organic_traffic'][-1] - 
                      st.session_state.analytics_data['organic_traffic'][-90]) / 
                      st.session_state.analytics_data['organic_traffic'][-90]) * 100
        
        st.metric("30 Days", f"{growth_30d:+.1f}%")
        st.metric("90 Days", f"{growth_90d:+.1f}%")
    
    with col2:
        st.markdown("**Keyword Growth**")
        
        keyword_growth_30d = ((st.session_state.analytics_data['keyword_rankings'][-1] - 
                              st.session_state.analytics_data['keyword_rankings'][-30]) / 
                              st.session_state.analytics_data['keyword_rankings'][-30]) * 100
        
        keyword_growth_90d = ((st.session_state.analytics_data['keyword_rankings'][-1] - 
                              st.session_state.analytics_data['keyword_rankings'][-90]) / 
                              st.session_state.analytics_data['keyword_rankings'][-90]) * 100
        
        st.metric("30 Days", f"{keyword_growth_30d:+.1f}%")
        st.metric("90 Days", f"{keyword_growth_90d:+.1f}%")
    
    with col3:
        st.markdown("**Backlink Growth**")
        
        backlink_growth_30d = ((st.session_state.analytics_data['backlinks'][-1] - 
                               st.session_state.analytics_data['backlinks'][-30]) / 
                               st.session_state.analytics_data['backlinks'][-30]) * 100
        
        backlink_growth_90d = ((st.session_state.analytics_data['backlinks'][-1] - 
                               st.session_state.analytics_data['backlinks'][-90]) / 
                               st.session_state.analytics_data['backlinks'][-90]) * 100
        
        st.metric("30 Days", f"{backlink_growth_30d:+.1f}%")
        st.metric("90 Days", f"{backlink_growth_90d:+.1f}%")
    
    # Distribution charts
    st.markdown("#### 📊 Traffic Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Traffic by channel
        st.markdown("**By Channel**")
        
        channel_data = {
            'Channel': ['Organic Search', 'Direct', 'Referral', 'Social', 'Email'],
            'Sessions': [12500, 3200, 2800, 1500, 1000]
        }
        
        fig_channel = go.Figure(data=[go.Pie(
            labels=channel_data['Channel'],
            values=channel_data['Sessions'],
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe'])
        )])
        
        fig_channel.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        # Traffic by device
        st.markdown("**By Device**")
        
        device_data = {
            'Device': ['Desktop', 'Mobile', 'Tablet'],
            'Sessions': [10500, 8200, 2300]
        }
        
        fig_device = go.Figure(data=[go.Pie(
            labels=device_data['Device'],
            values=device_data['Sessions'],
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb'])
        )])
        
        fig_device.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_device, use_container_width=True)

with tab2:
    st.markdown("### 🔍 Deep Dive Analysis")
    
    # Metric selector
    deep_dive_metric = st.selectbox(
        "Select metric for deep analysis",
        options=['Organic Traffic', 'Bounce Rate', 'Page Speed', 'Conversion Rate']
    )
    
    metric_key_map = {
        'Organic Traffic': 'organic_traffic',
        'Bounce Rate': 'bounce_rate',
        'Page Speed': 'page_speed',
        'Conversion Rate': 'conversion_rate'
    }
    
    selected_key = metric_key_map[deep_dive_metric]
    
    # Detailed time series
    st.markdown(f"#### 📈 {deep_dive_metric} Over Time")
    
    fig = go.Figure()
    
    # Main line
    fig.add_trace(go.Scatter(
        x=st.session_state.analytics_data['dates'],
        y=st.session_state.analytics_data[selected_key],
        mode='lines+markers',
        name=deep_dive_metric,
        line=dict(color='#667eea', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    # Add moving average
    ma_values = pd.Series(st.session_state.analytics_data[selected_key]).rolling(window=7).mean()
    
    fig.add_trace(go.Scatter(
        x=st.session_state.analytics_data['dates'],
        y=ma_values,
        mode='lines',
        name='7-day Moving Average',
        line=dict(color='#764ba2', width=2, dash='dash')
    ))
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistical analysis
    col1, col2, col3, col4 = st.columns(4)
    
    data_values = st.session_state.analytics_data[selected_key]
    
    with col1:
        st.metric("Mean", f"{sum(data_values)/len(data_values):.2f}")
    with col2:
        st.metric("Median", f"{sorted(data_values)[len(data_values)//2]:.2f}")
    with col3:
        st.metric("Std Dev", f"{pd.Series(data_values).std():.2f}")
    with col4:
        st.metric("Variance", f"{pd.Series(data_values).var():.2f}")
    
    # Anomaly detection
    st.markdown("#### 🚨 Anomaly Detection")
    
    anomalies = []
    mean_val = sum(data_values) / len(data_values)
    std_val = pd.Series(data_values).std()
    
    for i, val in enumerate(data_values):
        if abs(val - mean_val) > 2 * std_val:
            anomalies.append({
                'date': st.session_state.analytics_data['dates'][i],
                'value': val,
                'deviation': abs(val - mean_val) / std_val
            })
    
    if anomalies:
        st.warning(f"⚠️ Found {len(anomalies)} anomalies in the data")
        
        for anomaly in anomalies[:5]:  # Show top 5
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Date:** {anomaly['date']}")
            with col2:
                st.markdown(f"**Value:** {anomaly['value']:.2f}")
            with col3:
                st.markdown(f"**Deviation:** {anomaly['deviation']:.2f}σ")
    else:
        st.success("✅ No significant anomalies detected")
    
    # Hourly/Daily patterns
    st.markdown("#### 🕐 Time-based Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Day of Week Analysis**")
        
        dow_data = {
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            'Traffic': [random.randint(500, 800) for _ in range(7)]
        }
        
        fig_dow = go.Figure(data=[go.Bar(
            x=dow_data['Day'],
            y=dow_data['Traffic'],
            marker_color='#667eea'
        )])
        
        fig_dow.update_layout(height=300)
        st.plotly_chart(fig_dow, use_container_width=True)
    
    with col2:
        st.markdown("**Hour of Day Analysis**")
        
        hour_data = {
            'Hour': [f"{i:02d}:00" for i in range(24)],
            'Traffic': [random.randint(50, 300) for _ in range(24)]
        }
        
        fig_hour = go.Figure(data=[go.Scatter(
            x=hour_data['Hour'],
            y=hour_data['Traffic'],
            mode='lines+markers',
            line=dict(color='#764ba2', width=2),
            marker=dict(size=4)
        )])
        
        fig_hour.update_layout(height=300)
        st.plotly_chart(fig_hour, use_container_width=True)

with tab3:
    st.markdown("### 🎯 Correlation Analysis")
    
    st.info("💡 Discover relationships between different SEO metrics to understand what drives performance")
    
    # Correlation matrix
    st.markdown("#### 🔗 Correlation Matrix")
    
    # Calculate correlations
    metrics_for_correlation = {
        'Traffic': st.session_state.analytics_data['organic_traffic'],
        'Keywords': st.session_state.analytics_data['keyword_rankings'],
        'Backlinks': st.session_state.analytics_data['backlinks'],
        'DA': st.session_state.analytics_data['domain_authority'],
        'Speed': st.session_state.analytics_data['page_speed'],
        'Bounce': st.session_state.analytics_data['bounce_rate'],
        'Conversion': st.session_state.analytics_data['conversion_rate']
    }
    
    df_corr = pd.DataFrame(metrics_for_correlation)
    correlation_matrix = df_corr.corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Correlation")
    ))
    
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Key insights
    st.markdown("#### 💡 Key Correlations")
    
    correlations = [
        {'metric1': 'Traffic', 'metric2': 'Keywords', 'correlation': 0.87, 'strength': 'High'},
        {'metric1': 'Traffic', 'metric2': 'Backlinks', 'correlation': 0.76, 'strength': 'High'},
        {'metric1': 'Keywords', 'metric2': 'Domain Authority', 'correlation': 0.82, 'strength': 'High'},
        {'metric1': 'Page Speed', 'metric2': 'Bounce Rate', 'correlation': -0.64, 'strength': 'Medium'},
        {'metric1': 'Bounce Rate', 'metric2': 'Conversion', 'correlation': -0.71, 'strength': 'High'},
        {'metric1': 'Backlinks', 'metric2': 'Domain Authority', 'correlation': 0.79, 'strength': 'High'}
    ]
    
    for corr in correlations:
        strength_class = {
            'High': 'correlation-high',
            'Medium': 'correlation-medium',
            'Low': 'correlation-low'
        }[corr['strength']]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{corr['metric1']}** ↔️ **{corr['metric2']}**")
        with col2:
            st.markdown(f"<span class='{strength_class}'>{corr['strength']}</span>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"**r = {corr['correlation']:.2f}**")
        
        st.markdown("---")
    
    # Scatter plot analysis
    st.markdown("#### 📊 Relationship Explorer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_metric = st.selectbox(
            "X-axis metric",
            options=['Traffic', 'Keywords', 'Backlinks', 'DA', 'Speed', 'Bounce', 'Conversion'],
            index=1
        )
    
    with col2:
        y_metric = st.selectbox(
            "Y-axis metric",
            options=['Traffic', 'Keywords', 'Backlinks', 'DA', 'Speed', 'Bounce', 'Conversion'],
            index=0
        )
    
    fig_scatter = go.Figure()
    
    fig_scatter.add_trace(go.Scatter(
        x=df_corr[x_metric],
        y=df_corr[y_metric],
        mode='markers',
        marker=dict(
            size=8,
            color=df_corr[y_metric],
            colorscale='Viridis',
            showscale=True,
            line=dict(width=1, color='white')
        ),
        text=[f"Day {i+1}" for i in range(len(df_corr))],
        hovertemplate=f'<b>%{{text}}</b><br>{x_metric}: %{{x}}<br>{y_metric}: %{{y}}<extra></extra>'
    ))
    
    # Add trend line
    z = pd.Series(df_corr[x_metric]).rolling(window=5).mean()
    fig_scatter.add_trace(go.Scatter(
        x=df_corr[x_metric],
        y=z,
        mode='lines',
        name='Trend',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig_scatter.update_layout(
        xaxis_title=x_metric,
        yaxis_title=y_metric,
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.markdown("### 📊 Cohort Analysis")
    
    st.info("💡 Track how different groups of users behave over time")
    
    # Cohort selector
    cohort_type = st.radio(
        "Cohort Type",
        options=['Acquisition Month', 'Traffic Source', 'Device Type', 'Geographic Location'],
        horizontal=True
    )
    
    # Generate cohort data
    if cohort_type == 'Acquisition Month':
        cohorts = ['November 2025', 'December 2025', 'January 2026']
        
        cohort_data = []
        for cohort in cohorts:
            retention = [100]
            for i in range(1, 6):
                retention.append(retention[-1] * random.uniform(0.7, 0.9))
            cohort_data.append(retention)
        
        # Cohort retention chart
        st.markdown("#### 📈 Cohort Retention")
        
        fig_cohort = go.Figure()
        
        for i, cohort in enumerate(cohorts):
            fig_cohort.add_trace(go.Scatter(
                x=list(range(6)),
                y=cohort_data[i],
                mode='lines+markers',
                name=cohort,
                line=dict(width=2),
                marker=dict(size=8)
            ))
        
        fig_cohort.update_layout(
            xaxis_title="Weeks Since Acquisition",
            yaxis_title="Retention (%)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_cohort, use_container_width=True)
        
        # Heatmap
        st.markdown("#### 🔥 Retention Heatmap")
        
        heatmap_data = [[val for val in cohort] for cohort in cohort_data]
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=[f'Week {i}' for i in range(6)],
            y=cohorts,
            colorscale='YlOrRd',
            text=[[f'{val:.1f}%' for val in cohort] for cohort in cohort_data],
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Retention %")
        ))
        
        fig_heat.update_layout(height=300)
        st.plotly_chart(fig_heat, use_container_width=True)
    
    elif cohort_type == 'Traffic Source':
        sources = ['Organic Search', 'Direct', 'Referral', 'Social']
        
        st.markdown("#### 📊 Performance by Traffic Source")
        
        source_metrics = {
            'Source': sources,
            'Users': [random.randint(5000, 15000) for _ in range(4)],
            'Sessions': [random.randint(8000, 20000) for _ in range(4)],
            'Bounce Rate': [random.uniform(30, 60) for _ in range(4)],
            'Conversion': [random.uniform(2, 8) for _ in range(4)]
        }
        
        df_sources = pd.DataFrame(source_metrics)
        st.dataframe(df_sources, use_container_width=True, hide_index=True)
        
        # Bar chart comparison
        fig_sources = go.Figure()
        
        fig_sources.add_trace(go.Bar(
            name='Users',
            x=sources,
            y=source_metrics['Users'],
            marker_color='#667eea'
        ))
        
        fig_sources.add_trace(go.Bar(
            name='Sessions',
            x=sources,
            y=source_metrics['Sessions'],
            marker_color='#764ba2'
        ))
        
        fig_sources.update_layout(
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_sources, use_container_width=True)

with tab5:
    st.markdown("### 🌊 Funnel Analysis")
    
    st.info("💡 Visualize user journey and identify drop-off points")
    
    # Funnel selector
    funnel_type = st.selectbox(
        "Select Funnel",
        options=['SEO Conversion Funnel', 'Content Engagement Funnel', 'Lead Generation Funnel']
    )
    
    if funnel_type == 'SEO Conversion Funnel':
        funnel_stages = {
            'Stages': ['Organic Search', 'Landing Page', 'Internal Link Click', 'Goal Page', 'Conversion'],
            'Users': [10000, 7500, 5000, 2500, 500],
            'Drop-off': ['-', '25%', '33%', '50%', '80%']
        }
        
        st.markdown("#### 🌊 Conversion Funnel")
        
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_stages['Stages'],
            x=funnel_stages['Users'],
            textposition="inside",
            textinfo="value+percent initial",
            marker=dict(
                color=['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            ),
            connector=dict(line=dict(color="royalblue", width=3))
        ))
        
        fig_funnel.update_layout(height=500)
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Detailed metrics
        st.markdown("#### 📊 Stage Details")
        
        for i, stage in enumerate(funnel_stages['Stages']):
            with st.expander(f"**{stage}** - {funnel_stages['Users'][i]:,} users", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Users", f"{funnel_stages['Users'][i]:,}")
                with col2:
                    if i > 0:
                        conversion_rate = (funnel_stages['Users'][i] / funnel_stages['Users'][i-1]) * 100
                        st.metric("Conversion from Previous", f"{conversion_rate:.1f}%")
                with col3:
                    if i < len(funnel_stages['Users']) - 1:
                        st.metric("Drop-off to Next", funnel_stages['Drop-off'][i+1])
                
                # Recommendations
                if i == 1:
                    st.markdown("**💡 Recommendations:**")
                    st.markdown("• Optimize landing page load time")
                    st.markdown("• Improve above-the-fold content")
                    st.markdown("• Add clear call-to-action buttons")
                elif i == 2:
                    st.markdown("**💡 Recommendations:**")
                    st.markdown("• Add more internal links")
                    st.markdown("• Improve content relevance")
                    st.markdown("• Use better anchor text")

with tab6:
    st.markdown("### 🤖 Predictive Analytics")
    
    st.info("💡 AI-powered forecasts based on historical data and trends")
    
    # Prediction type
    prediction_metric = st.selectbox(
        "Select metric to forecast",
        options=['Organic Traffic', 'Keyword Rankings', 'Backlinks', 'Domain Authority']
    )
    
    forecast_period = st.slider("Forecast period (days)", min_value=7, max_value=90, value=30)
    
    # Generate forecast
    metric_key = {
        'Organic Traffic': 'organic_traffic',
        'Keyword Rankings': 'keyword_rankings',
        'Backlinks': 'backlinks',
        'Domain Authority': 'domain_authority'
    }[prediction_metric]
    
    historical_data = st.session_state.analytics_data[metric_key]
    
    # Simple trend-based forecast
    recent_trend = (historical_data[-1] - historical_data[-30]) / 30
    
    forecast_dates = [(datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(1, forecast_period + 1)]
    forecast_values = [historical_data[-1] + (recent_trend * i) for i in range(1, forecast_period + 1)]
    
    # Add some variance
    forecast_values = [max(0, val + random.uniform(-recent_trend*2, recent_trend*2)) for val in forecast_values]
    
    st.markdown(f"#### 📈 {prediction_metric} Forecast")
    
    fig_forecast = go.Figure()
    
    # Historical data
    fig_forecast.add_trace(go.Scatter(
        x=st.session_state.analytics_data['dates'][-30:],
        y=historical_data[-30:],
        mode='lines+markers',
        name='Historical',
        line=dict(color='#667eea', width=2),
        marker=dict(size=4)
    ))
    
    # Forecast
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates,
        y=forecast_values,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#f5576c', width=2, dash='dash'),
        marker=dict(size=4)
    ))
    
    # Confidence interval
    upper_bound = [val * 1.1 for val in forecast_values]
    lower_bound = [val * 0.9 for val in forecast_values]
    
    fig_forecast.add_trace(go.Scatter(
        x=forecast_dates + forecast_dates[::-1],
        y=upper_bound + lower_bound[::-1],
        fill='toself',
        fillcolor='rgba(245, 87, 108, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval',
        showlegend=True
    ))
    
    fig_forecast.update_layout(
        xaxis_title="Date",
        yaxis_title=prediction_metric,
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Forecast summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Value", f"{historical_data[-1]:.0f}")
    with col2:
        st.metric("Predicted (30d)", f"{forecast_values[29]:.0f}")
    with col3:
        predicted_growth = ((forecast_values[29] - historical_data[-1]) / historical_data[-1]) * 100
        st.metric("Predicted Growth", f"{predicted_growth:+.1f}%")
    with col4:
        confidence = random.uniform(75, 95)
        st.metric("Confidence", f"{confidence:.1f}%")
    
    # Key drivers
    st.markdown("#### 🎯 Key Growth Drivers")
    
    drivers = [
        {'factor': 'Keyword Optimization', 'impact': 'High', 'contribution': '35%'},
        {'factor': 'Backlink Acquisition', 'impact': 'High', 'contribution': '28%'},
        {'factor': 'Content Quality', 'impact': 'Medium', 'contribution': '22%'},
        {'factor': 'Technical SEO', 'impact': 'Medium', 'contribution': '15%'}
    ]
    
    for driver in drivers:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{driver['factor']}**")
        with col2:
            impact_color = '#10b981' if driver['impact'] == 'High' else '#f59e0b'
            st.markdown(f"<span style='background: {impact_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.875rem;'>{driver['impact']}</span>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"**{driver['contribution']}**")
        
        st.markdown("---")
    
    # Recommendations
    st.markdown("#### 💡 AI Recommendations")
    
    recommendations = [
        "📈 **Increase content production** - Current trend shows 23% growth potential with 2x content output",
        "🔗 **Focus on backlink quality** - Target domains with DA 50+ for maximum impact",
        "🎯 **Optimize for long-tail keywords** - 67% lower competition, 34% higher conversion",
        "⚡ **Improve page speed** - 1-second improvement could increase traffic by 12%"
    ]
    
    for rec in recommendations:
        st.markdown(rec)

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Use correlation analysis to discover hidden relationships between metrics and optimize your SEO strategy!")