import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Page Configuration
st.set_page_config(
    page_title="NEXUS Elite Command",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. ENTERPRISE CORE ARCHITECTURE ---
@st.cache_resource
def init_supabase():
    """Initialize Supabase client with proper error handling"""
    try:
        return create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
    except Exception as e:
        st.error(f"⚠️ Supabase connection error: {e}")
        return None

supabase = init_supabase()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'temp_users' not in st.session_state:
    # Temporary storage for demo/testing (remove in production)
    st.session_state.temp_users = {}

# --- 2. ELITE CSS STYLING ---
st.markdown("""
<style>
    /* Main Background */
    .main { 
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 100%);
        color: white; 
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a0a0a 100%);
        border-right: 2px solid #ff4b4b;
    }
    
    /* Buttons */
    .stButton>button {
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
        height: 3.5rem;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 40px #ff4b4b;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Metric Cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,75,75,0.1) 0%, rgba(0,0,0,0.8) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ff4b4b;
        box-shadow: 0 8px 32px rgba(255, 75, 75, 0.2);
    }
    
    /* Container with border */
    .element-container:has(.terminal-box) {
        border: 2px solid #ff4b4b;
        border-radius: 15px;
        padding: 20px;
        background: rgba(255,75,75,0.05);
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. VISUALIZATION FUNCTIONS ---

def render_intelligence_globe():
    """3D Globe with country markers"""
    data = pd.DataFrame({
        'Country': ['Brazil', 'Morocco', 'USA', 'Spain', 'UAE', 'Singapore', 'Japan', 'UK', 'Germany', 'Australia'],
        'Lat': [-14.23, 31.79, 37.09, 40.46, 23.42, 1.35, 36.20, 55.37, 51.16, -25.27],
        'Lon': [-51.92, -7.09, -95.71, -3.74, 53.84, 103.81, 138.25, -3.43, 10.45, 133.77],
        'Traffic': [88, 83, 95, 91, 99, 94, 85, 92, 87, 78]
    })
    
    fig = go.Figure()
    
    # Add markers
    fig.add_trace(go.Scattergeo(
        lon=data['Lon'],
        lat=data['Lat'],
        text=data['Country'] + '<br>Traffic: ' + data['Traffic'].astype(str) + '%',
        mode='markers+text',
        marker=dict(
            size=data['Traffic']/5,
            color=data['Traffic'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Traffic %"),
            line=dict(width=2, color='white')
        ),
        textposition="top center"
    ))
    
    # Add connection lines
    for i in range(len(data)-1):
        fig.add_trace(go.Scattergeo(
            lon=[data.iloc[i]['Lon'], data.iloc[i+1]['Lon']],
            lat=[data.iloc[i]['Lat'], data.iloc[i+1]['Lat']],
            mode='lines',
            line=dict(width=1, color='rgba(255,75,75,0.4)'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_geos(
        projection_type="orthographic",
        showcoastlines=True,
        coastlinecolor="#333",
        showland=True,
        landcolor="#0a0a0a",
        showocean=True,
        oceancolor="#050505",
        showcountries=True,
        countrycolor="#222",
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    return fig

def create_realtime_chart():
    """Real-time activity chart"""
    hours = 24
    now = datetime.now()
    times = [now - timedelta(hours=i) for i in range(hours, 0, -1)]
    
    data = pd.DataFrame({
        'Time': times,
        'Activity': np.random.randint(1000, 5000, hours) + np.sin(np.linspace(0, 4*np.pi, hours)) * 1000
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Time'],
        y=data['Activity'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#ff4b4b', width=3),
        fillcolor='rgba(255, 75, 75, 0.2)'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255, 75, 75, 0.1)'),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

# --- 4. AUTHENTICATION FUNCTIONS ---

def register_user(email, password):
    """
    Handle user registration with multiple fallback methods
    """
    try:
        # Method 1: Try Supabase registration
        if supabase:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "email_redirect_to": None,  # Disable redirect
                }
            })
            
            # Check if email confirmation is required
            if response.user and not response.session:
                return "verification_required", "Please check your email to verify your account."
            elif response.session:
                # Auto-login if email confirmation is disabled
                st.session_state.user = response.user
                st.session_state.authenticated = True
                return "success", "Account created and logged in!"
            
    except Exception as e:
        error_msg = str(e).lower()
        
        # Handle specific Supabase errors
        if "user already registered" in error_msg or "already exists" in error_msg:
            return "error", "Email already registered. Please login instead."
        elif "email" in error_msg and "confirm" in error_msg:
            return "info", "Email confirmation disabled. You can now login directly."
        
    # Method 2: Fallback - Store temporarily (for demo/testing only)
    if email not in st.session_state.temp_users:
        st.session_state.temp_users[email] = password
        return "demo_success", "⚠️ Demo mode: Account created locally. In production, check Supabase email settings."
    
    return "error", "Registration failed. Please try again."

def login_user(email, password):
    """
    Handle user login with fallback
    """
    try:
        # Method 1: Try Supabase login
        if supabase:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                st.session_state.user = response.user
                st.session_state.authenticated = True
                return "success", "Welcome back!"
                
    except Exception as e:
        error_msg = str(e).lower()
        
        if "invalid" in error_msg or "credentials" in error_msg:
            # Method 2: Check temporary storage (demo mode)
            if email in st.session_state.temp_users and st.session_state.temp_users[email] == password:
                st.session_state.authenticated = True
                st.session_state.user = {"email": email}
                return "demo_success", "⚠️ Demo login successful"
            return "error", "Invalid credentials"
        elif "not confirmed" in error_msg or "email not confirmed" in error_msg:
            return "error", "Please verify your email first. Check your inbox."
    
    return "error", "Login failed. Please check your credentials."

# --- 5. AUTHENTICATION PAGE ---

def auth_terminal():
    """Beautiful authentication interface"""
    
    st.markdown("<h1 style='text-align: center; font-size: 60px;'>⚡ NEXUS ELITE COMMAND</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 24px; color: #888;'>Global Intelligence & Strategic ROI Engine</p>", unsafe_allow_html=True)
    
    # Display globe
    st.plotly_chart(render_intelligence_globe(), use_container_width=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Intelligence Nodes", "1,842", "+12")
    with col2:
        st.metric("Active Scans", "15.4M", "Live")
    with col3:
        st.metric("Avg Strategic ROI", "342%", "+28%")
    with col4:
        st.metric("Global Networks", "94", "+5")
    
    st.markdown("---")
    
    # Auth section
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("### 🔐 Access Terminal")
        
        tab_login, tab_register = st.tabs(["🔑 Login", "📝 Register"])
        
        with tab_login:
            login_email = st.text_input("Corporate ID (Email)", key="login_email")
            login_password = st.text_input("Security Token", type="password", key="login_pwd")
            
            if st.button("🚀 AUTHORIZE ACCESS", key="login_btn"):
                if login_email and login_password:
                    with st.spinner("Authenticating..."):
                        status, message = login_user(login_email, login_password)
                        
                        if "success" in status:
                            st.success(message)
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(message)
                else:
                    st.warning("Please enter both email and password")
        
        with tab_register:
            reg_email = st.text_input("Corporate Email", key="reg_email")
            reg_password = st.text_input("Create Security Token (min 6 chars)", type="password", key="reg_pwd")
            reg_confirm = st.text_input("Confirm Security Token", type="password", key="reg_confirm")
            
            st.info("💡 **Email not arriving?** Check spam folder or use demo mode by clicking register then login with same credentials.")
            
            if st.button("✨ CREATE ACCOUNT", key="reg_btn"):
                if not reg_email or not reg_password:
                    st.warning("Please fill all fields")
                elif len(reg_password) < 6:
                    st.warning("Password must be at least 6 characters")
                elif reg_password != reg_confirm:
                    st.error("Passwords don't match")
                else:
                    with st.spinner("Creating account..."):
                        status, message = register_user(reg_email, reg_password)
                        
                        if status == "success":
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        elif status == "demo_success":
                            st.success(message)
                            st.info("You can now login with these credentials!")
                        elif status == "verification_required":
                            st.info(message)
                            st.warning("⚠️ Email not arriving? Check spam or disable email confirmation in Supabase settings.")
                        else:
                            st.error(message)
    
    with col_right:
        st.markdown("""
        <div style='border: 2px solid #ff4b4b; padding: 30px; border-radius: 15px; background: rgba(255,75,75,0.05);'>
            <h2 style='color: #ff4b4b; margin-top: 0;'>💎 Agency Especial</h2>
            <p style='font-size: 18px;'>Strategic white-label intelligence for enterprise organizations.</p>
            
            <div style='margin: 25px 0;'>
                <h3 style='color: #ff4b4b;'>Consultation License: €3,000 / mo</h3>
            </div>
            
            <div style='margin: 20px 0;'>
                <div style='margin: 10px 0;'>✅ 25k Node Analysis</div>
                <div style='margin: 10px 0;'>✅ API Export</div>
                <div style='margin: 10px 0;'>✅ Dedicated Support</div>
                <div style='margin: 10px 0;'>✅ White-Label Dashboard</div>
                <div style='margin: 10px 0;'>✅ Priority AI Processing</div>
            </div>
            
            <button style='width: 100%; padding: 15px; margin-top: 20px; border-radius: 10px; background: linear-gradient(45deg, #ff4b4b, #cc0000); border: none; color: white; font-size: 16px; font-weight: bold; cursor: pointer;'>
                REQUEST PRIVATE ACCESS
            </button>
        </div>
        
        <div style='margin-top: 20px; padding: 20px; border: 1px solid #333; border-radius: 10px; background: rgba(0,0,0,0.5);'>
            <h4 style='color: #ff4b4b;'>🔧 Email Issues?</h4>
            <p style='font-size: 14px;'>If verification emails aren't arriving:</p>
            <ol style='font-size: 14px; color: #ccc;'>
                <li>Check your spam/junk folder</li>
                <li>Disable email confirmation in Supabase → Authentication → Settings</li>
                <li>Use demo mode (register then login immediately)</li>
                <li>Configure SMTP settings in Supabase</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# --- 6. MAIN DASHBOARD ---

def main_dashboard():
    """Main application dashboard after login"""
    
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ff4b4b, #cc0000); border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: white;'>👤 {st.session_state.user.get('email', 'User')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Navigation")
        page = st.radio("", [
            "🏠 Command Center",
            "🌍 Global Intelligence",
            "🤖 AI Analysis",
            "📊 Analytics"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            if supabase:
                try:
                    supabase.auth.sign_out()
                except:
                    pass
            st.rerun()
    
    # Main content
    if "Command Center" in page:
        show_command_center()
    elif "Global Intelligence" in page:
        show_global_intelligence()
    elif "AI Analysis" in page:
        show_ai_analysis()
    else:
        show_analytics()

def show_command_center():
    """Command Center Dashboard"""
    st.markdown("# 🛰️ Intelligence Deployment Node")
    st.markdown("Strategic intelligence and market analysis platform")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Security Score", "98.7%", "↑ 2.3%")
    with col2:
        st.metric("Active Users", "12,483", "+342")
    with col3:
        st.metric("Targets Analyzed", "847", "+23")
    with col4:
        st.metric("Revenue Impact", "$2.4M", "+$340K")
    
    st.markdown("---")
    
    # Analysis section
    st.markdown("### 🎯 Target Intelligence Analysis")
    target = st.text_input("Target Domain or Company:", placeholder="https://example.com")
    
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        if st.button("⚡ EXECUTE SCAN", use_container_width=True) and target:
            with st.status("🔄 Initializing High-Vector Scans...", expanded=True) as status:
                st.write("> Connecting to Global Harvester Nodes...")
                time.sleep(1)
                st.write("> Harvesting Semantic ROI Vectors...")
                time.sleep(1)
                st.write("> Analyzing competitive landscape...")
                time.sleep(0.8)
                st.write("> Generating strategic intelligence...")
                time.sleep(0.8)
                status.update(label="✅ Strategic Intelligence Captured!", state="complete")
            
            st.success(f"Intelligence Report Generated for: **{target}**")
            
            # Display mock results
            st.markdown("#### 📊 Intelligence Summary")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric("Market Position", "8.4/10")
            with col_r2:
                st.metric("Growth Potential", "High")
            with col_r3:
                st.metric("Risk Level", "Moderate")
    
    with col_b:
        st.markdown("#### 🎯 Quick Stats")
        st.metric("Scans Today", "47", "+8")
        st.metric("Success Rate", "94.3%")
    
    # Real-time chart
    st.markdown("### 📈 Real-Time Activity Monitor")
    st.plotly_chart(create_realtime_chart(), use_container_width=True)

def show_global_intelligence():
    """Global Intelligence Page"""
    st.markdown("# 🌍 Global Intelligence Network")
    st.plotly_chart(render_intelligence_globe(), use_container_width=True)
    
    st.markdown("### 📍 Regional Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        regions = pd.DataFrame({
            'Region': ['North America', 'Europe', 'Asia Pacific', 'Middle East', 'Latin America'],
            'Nodes': [342, 287, 415, 198, 156]
        })
        fig = px.bar(regions, x='Region', y='Nodes', color='Nodes', 
                     color_continuous_scale='Reds')
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                         plot_bgcolor='rgba(0,0,0,0)', 
                         font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(regions, values='Nodes', names='Region',
                     color_discrete_sequence=px.colors.sequential.Reds)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', 
                         font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)

def show_ai_analysis():
    """AI Analysis Page"""
    st.markdown("# 🤖 AI-Powered Intelligence")
    st.markdown("Advanced strategic analysis powered by Claude AI")
    
    target = st.text_input("Enter analysis target:", placeholder="Company name or URL")
    analysis_type = st.selectbox("Analysis Type:", [
        "Complete Intelligence Report",
        "Market Position Analysis",
        "Competitive Landscape",
        "Growth Opportunities"
    ])
    
    if st.button("🚀 GENERATE AI REPORT", use_container_width=True):
        if target:
            with st.spinner("AI analyzing data..."):
                time.sleep(2)
            st.success("Analysis complete!")
            st.markdown(f"""
            ### 📋 AI Intelligence Report
            
            **Target:** {target}  
            **Analysis:** {analysis_type}  
            **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            #### Key Findings
            - Market positioning shows strong competitive advantages
            - Growth potential identified in emerging markets
            - Strategic recommendations for expansion
            """)

def show_analytics():
    """Analytics Page"""
    st.markdown("# 📊 Advanced Analytics")
    st.plotly_chart(create_realtime_chart(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Analyses", "1,247", "+89")
        st.metric("Success Rate", "94.3%", "+1.2%")
    with col2:
        st.metric("Avg Response", "2.3s", "-0.4s")
        st.metric("Client Satisfaction", "4.8/5", "+0.2")

# --- 7. MAIN APP LOGIC ---

def main():
    if not st.session_state.authenticated:
        auth_terminal()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
