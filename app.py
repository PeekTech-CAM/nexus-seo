import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json

# Page Configuration
st.set_page_config(
    page_title="NEXUS Elite Command",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'animation_frame' not in st.session_state:
    st.session_state.animation_frame = 0

# Elite CSS Styling
st.markdown("""
<style>
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 100%);
        color: #ffffff;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a0a0a 100%);
        border-right: 2px solid #ff4b4b;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.5);
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,75,75,0.1) 0%, rgba(0,0,0,0.8) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ff4b4b;
        box-shadow: 0 8px 32px rgba(255, 75, 75, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff4b4b, #cc0000);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.6);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(255,75,75,0.2) 0%, rgba(0,0,0,0.4) 100%);
        border-radius: 10px;
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 75, 75, 0.1);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff4b4b, #cc0000);
    }
    
    /* Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Glowing effect */
    .glow {
        box-shadow: 0 0 20px #ff4b4b, 0 0 40px #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# === VISUALIZATION FUNCTIONS ===

def create_3d_globe():
    """Create stunning 3D rotating globe with country markers"""
    
    # Global locations with real data
    locations = pd.DataFrame({
        'Country': ['USA', 'Brazil', 'UK', 'Germany', 'UAE', 'Singapore', 
                    'Japan', 'Australia', 'Spain', 'Morocco', 'Canada', 'India'],
        'Lat': [37.09, -14.23, 55.37, 51.16, 23.42, 1.35, 
                36.20, -25.27, 40.46, 31.79, 56.13, 20.59],
        'Lon': [-95.71, -51.92, -3.43, 10.45, 53.84, 103.81, 
                138.25, 133.77, -3.74, -7.09, -106.34, 78.96],
        'Activity': [95, 88, 92, 87, 99, 94, 85, 78, 91, 83, 89, 96],
        'Status': ['Active', 'Active', 'Active', 'Active', 'Active', 'Active',
                   'Monitoring', 'Monitoring', 'Active', 'Active', 'Active', 'Active']
    })
    
    fig = go.Figure()
    
    # Add country markers
    fig.add_trace(go.Scattergeo(
        lon=locations['Lon'],
        lat=locations['Lat'],
        text=locations['Country'] + '<br>Activity: ' + locations['Activity'].astype(str) + '%',
        mode='markers+text',
        marker=dict(
            size=locations['Activity'] / 5,
            color=locations['Activity'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Activity %", x=1.1),
            line=dict(width=2, color='white'),
            symbol='circle'
        ),
        textposition="top center",
        textfont=dict(size=10, color='white'),
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))
    
    # Add connection lines between major hubs
    connections = [
        (locations.iloc[0], locations.iloc[1]),  # USA-Brazil
        (locations.iloc[0], locations.iloc[2]),  # USA-UK
        (locations.iloc[2], locations.iloc[3]),  # UK-Germany
        (locations.iloc[4], locations.iloc[5]),  # UAE-Singapore
    ]
    
    for start, end in connections:
        fig.add_trace(go.Scattergeo(
            lon=[start['Lon'], end['Lon']],
            lat=[start['Lat'], end['Lat']],
            mode='lines',
            line=dict(width=2, color='rgba(255, 75, 75, 0.6)'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_geos(
        projection_type="orthographic",
        showcountries=True,
        countrycolor="rgba(100, 100, 100, 0.3)",
        showcoastlines=True,
        coastlinecolor="rgba(255, 255, 255, 0.2)",
        showland=True,
        landcolor="rgba(20, 20, 20, 0.9)",
        showocean=True,
        oceancolor="rgba(10, 10, 10, 1)",
        bgcolor="rgba(0, 0, 0, 0)",
        projection_rotation=dict(lon=30, lat=20, roll=0)
    )
    
    fig.update_layout(
        height=700,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)')
    )
    
    return fig

def create_realtime_chart():
    """Create animated real-time data stream"""
    hours = 24
    now = datetime.now()
    times = [now - timedelta(hours=i) for i in range(hours, 0, -1)]
    
    data = pd.DataFrame({
        'Time': times,
        'Traffic': np.random.randint(1000, 5000, hours) + np.sin(np.linspace(0, 4*np.pi, hours)) * 1000,
        'Conversions': np.random.randint(100, 800, hours) + np.sin(np.linspace(0, 4*np.pi, hours)) * 200,
        'Revenue': np.random.randint(5000, 20000, hours) + np.sin(np.linspace(0, 4*np.pi, hours)) * 5000
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['Time'], y=data['Traffic'],
        name='Traffic',
        line=dict(color='#ff4b4b', width=3),
        fill='tonexty',
        fillcolor='rgba(255, 75, 75, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=data['Time'], y=data['Conversions'],
        name='Conversions',
        line=dict(color='#00ff88', width=3),
        fill='tonexty',
        fillcolor='rgba(0, 255, 136, 0.2)'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, gridcolor='rgba(255, 75, 75, 0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 75, 75, 0.1)'),
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_3d_surface():
    """Create stunning 3D surface plot"""
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2)) * np.cos(X) * np.sin(Y)
    
    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y,
        colorscale='Reds',
        showscale=False
    )])
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="black", gridcolor="rgba(255, 75, 75, 0.2)"),
            yaxis=dict(backgroundcolor="black", gridcolor="rgba(255, 75, 75, 0.2)"),
            zaxis=dict(backgroundcolor="black", gridcolor="rgba(255, 75, 75, 0.2)"),
            bgcolor="rgba(0, 0, 0, 0)"
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        height=500,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def create_heatmap():
    """Create activity heatmap"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(24))
    data = np.random.randint(10, 100, (7, 24))
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=hours,
        y=days,
        colorscale='Reds',
        hoverongaps=False
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        height=400
    )
    
    return fig

def create_gauge_chart(value, title):
    """Create gauge chart for metrics"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': 'white'}},
        delta={'reference': 80, 'increasing': {'color': "#00ff88"}},
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': "white"},
            'bar': {'color': "#ff4b4b"},
            'bgcolor': "rgba(0,0,0,0.3)",
            'borderwidth': 2,
            'bordercolor': "white",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(255, 75, 75, 0.2)'},
                {'range': [50, 80], 'color': 'rgba(255, 165, 0, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(0, 255, 136, 0.2)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font={'color': 'white'},
        height=300
    )
    
    return fig

# === AUTHENTICATION SYSTEM ===

def auth_page():
    """Beautiful authentication page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1 style='font-size: 60px; margin-bottom: 10px;'>⚡ NEXUS ELITE</h1>
            <p style='font-size: 24px; color: #888;'>Global Intelligence Command Center</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display 3D Globe on login page
        st.plotly_chart(create_3d_globe(), use_container_width=True)
        
        # Live metrics preview
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Intelligence Nodes", "1,842", "+12")
        with col_m2:
            st.metric("Active Scans", "15.4M", "Live")
        with col_m3:
            st.metric("Avg ROI", "342%", "+28%")
        with col_m4:
            st.metric("Networks", "94", "+5")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Auth form
        with st.container():
            st.markdown("### 🔐 Secure Access Portal")
            
            tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])
            
            with tab1:
                email = st.text_input("Corporate ID (Email)", key="login_email")
                password = st.text_input("Security Token", type="password", key="login_pwd")
                
                if st.button("🚀 AUTHORIZE ACCESS", key="login_btn"):
                    if email and password:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.rerun()
                    else:
                        st.error("⚠️ Please enter credentials")
            
            with tab2:
                reg_email = st.text_input("Corporate Email", key="reg_email")
                reg_pwd = st.text_input("Create Security Token", type="password", key="reg_pwd")
                reg_pwd2 = st.text_input("Confirm Token", type="password", key="reg_pwd2")
                
                if st.button("✨ CREATE ACCOUNT", key="reg_btn"):
                    if reg_email and reg_pwd and reg_pwd == reg_pwd2:
                        st.success("✅ Account created! Please login.")
                    else:
                        st.error("⚠️ Please check your information")

# === MAIN DASHBOARD ===

def main_dashboard():
    """Main application dashboard"""
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ff4b4b, #cc0000); border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: white;'>👤 {st.session_state.user_email}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Navigation")
        page = st.radio("", [
            "📊 Command Center",
            "🌍 Global Intelligence",
            "🤖 AI Analysis",
            "📈 Advanced Analytics",
            "⚙️ Settings"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.rerun()
    
    # Main content
    if page == "📊 Command Center":
        show_command_center()
    elif page == "🌍 Global Intelligence":
        show_global_intelligence()
    elif page == "🤖 AI Analysis":
        show_ai_analysis()
    elif page == "📈 Advanced Analytics":
        show_advanced_analytics()
    else:
        show_settings()

def show_command_center():
    """Command Center Dashboard"""
    st.markdown("# ⚡ NEXUS COMMAND CENTER")
    st.markdown("Real-time Intelligence & Strategic Operations")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🛡️ Security Score", "98.7%", "↑ 2.3%")
    with col2:
        st.metric("👥 Active Users", "12,483", "+342")
    with col3:
        st.metric("🎯 Targets Analyzed", "847", "+23")
    with col4:
        st.metric("💰 Revenue Impact", "$2.4M", "+$340K")
    
    st.markdown("---")
    
    # Real-time chart
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Real-Time Intelligence Stream")
        st.plotly_chart(create_realtime_chart(), use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Performance Gauges")
        st.plotly_chart(create_gauge_chart(94, "System Health"), use_container_width=True)
    
    # Activity heatmap
    st.markdown("### 🔥 Activity Heatmap")
    st.plotly_chart(create_heatmap(), use_container_width=True)

def show_global_intelligence():
    """Global Intelligence with 3D Globe"""
    st.markdown("# 🌍 GLOBAL INTELLIGENCE NETWORK")
    st.markdown("Real-time monitoring of worldwide operations")
    
    # 3D Globe
    st.plotly_chart(create_3d_globe(), use_container_width=True)
    
    # Regional breakdown
    st.markdown("### 📍 Regional Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    regions_data = {
        'Region': ['North America', 'Europe', 'Asia Pacific', 'Middle East', 'Latin America', 'Africa'],
        'Nodes': [342, 287, 415, 198, 156, 89],
        'Activity': [95, 92, 98, 88, 85, 79],
        'Revenue': [1.2, 0.9, 1.5, 0.7, 0.4, 0.3]
    }
    
    df = pd.DataFrame(regions_data)
    
    with col1:
        st.markdown("#### Active Nodes")
        fig = px.bar(df, x='Region', y='Nodes', color='Nodes', color_continuous_scale='Reds')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Activity Level")
        fig = px.pie(df, values='Activity', names='Region', color_discrete_sequence=px.colors.sequential.Reds)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("#### Revenue Distribution")
        fig = px.funnel(df, x='Revenue', y='Region', color_discrete_sequence=['#ff4b4b'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)

def show_ai_analysis():
    """AI-Powered Analysis"""
    st.markdown("# 🤖 AI INTELLIGENCE ANALYSIS")
    st.markdown("Powered by Claude Sonnet 4 - Advanced Strategic Intelligence")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🎯 Target Analysis")
        target = st.text_input("Enter Target URL or Company Name:", placeholder="https://example.com")
        
        analysis_type = st.selectbox("Analysis Type:", [
            "Complete Intelligence Report",
            "Market Position Analysis",
            "Competitive Landscape",
            "Growth Opportunities",
            "Risk Assessment",
            "Strategic Recommendations"
        ])
        
        if st.button("🚀 EXECUTE AI ANALYSIS", use_container_width=True):
            if target:
                with st.spinner("🔄 AI Processing Intelligence Data..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress_bar.progress(i + 1)
                    
                    # Simulated AI response (replace with actual API call)
                    st.success("✅ Analysis Complete!")
                    
                    st.markdown("""
                    ### 📊 Intelligence Report
                    
                    **Target:** {}
                    **Analysis Type:** {}
                    **Timestamp:** {}
                    
                    #### Executive Summary
                    Based on comprehensive analysis, the target demonstrates strong market positioning with 
                    significant growth potential in emerging markets. Key competitive advantages identified 
                    include technological innovation and strategic partnerships.
                    
                    #### Key Findings
                    - **Market Share:** 23.4% (↑ 3.2%)
                    - **Growth Rate:** 18.7% YoY
                    - **Risk Level:** Moderate
                    - **Opportunity Score:** 8.4/10
                    
                    #### Strategic Recommendations
                    1. Expand digital presence in Asian markets
                    2. Strengthen partnership ecosystem
                    3. Invest in AI/ML capabilities
                    4. Optimize customer acquisition funnel
                    
                    *Report generated by NEXUS AI Engine powered by Claude Sonnet 4*
                    """.format(target, analysis_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                st.error("⚠️ Please enter a target")
    
    with col2:
        st.markdown("### 📊 Analysis Metrics")
        st.plotly_chart(create_gauge_chart(87, "Confidence"), use_container_width=True)
        
        st.markdown("### 🎯 Quick Stats")
        st.metric("Reports Generated", "1,247", "+89")
        st.metric("Accuracy Rate", "94.3%", "+1.2%")
        st.metric("Avg Processing", "2.3s", "-0.4s")

def show_advanced_analytics():
    """Advanced Analytics Dashboard"""
    st.markdown("# 📈 ADVANCED ANALYTICS")
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "🔮 Predictions", "🎨 3D Visualization"])
    
    with tab1:
        st.markdown("### Performance Trends")
        st.plotly_chart(create_realtime_chart(), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Activity Heatmap")
            st.plotly_chart(create_heatmap(), use_container_width=True)
        with col2:
            st.markdown("### Regional Distribution")
            data = pd.DataFrame({
                'Region': ['Americas', 'EMEA', 'APAC', 'LATAM'],
                'Value': [45, 28, 18, 9]
            })
            fig = px.pie(data, values='Value', names='Region', 
                        color_discrete_sequence=px.colors.sequential.Reds)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔮 Predictive Intelligence")
        
        # Generate prediction data
        dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        actual = np.random.randint(1000, 3000, 15)
        predicted = np.random.randint(2000, 4000, 15)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates[:15], y=actual, name='Actual', line=dict(color='#ff4b4b', width=3)))
        fig.add_trace(go.Scatter(x=dates[15:], y=predicted, name='Predicted', 
                                line=dict(color='#00ff88', width=3, dash='dash')))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                         font=dict(color='white'), hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎨 3D Data Visualization")
        st.plotly_chart(create_3d_surface(), use_container_width=True)

def show_settings():
    """Settings page"""
    st.markdown("# ⚙️ SETTINGS")
    
    st.markdown("### 👤 Account Settings")
    st.text_input("Email", value=st.session_state.user_email, disabled=True)
    st.text_input("New Password", type="password")
    st.text_input("Confirm Password", type="password")
    
    if st.button("💾 Save Changes"):
        st.success("✅ Settings updated successfully!")
    
    st.markdown("---")
    st.markdown("### 🎨 Theme Settings")
    theme = st.selectbox("Color Theme", ["Red Elite (Default)", "Blue Corporate", "Green Matrix", "Purple Cyber"])
    st.slider("Animation Speed", 0, 100, 50)
    
    st.markdown("---")
    st.markdown("### 🔔 Notifications")
    st.checkbox("Email Alerts", value=True)
    st.checkbox("Push Notifications", value=True)
    st.checkbox("Weekly Reports", value=True)

# === MAIN APP LOGIC ===

def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
