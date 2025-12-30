import streamlit as st
from supabase import create_client, Client
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="NEXUS SEO Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURATION ---
@st.cache_resource
def init_supabase():
    try:
        return create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
    except:
        return None

@st.cache_resource
def init_gemini():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel('gemini-pro')
    except:
        return None

supabase = init_supabase()
gemini_model = init_gemini()

# Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'user_plan' not in st.session_state:
    st.session_state.user_plan = 'free'
if 'audits_used' not in st.session_state:
    st.session_state.audits_used = 0
if 'temp_users' not in st.session_state:
    st.session_state.temp_users = {}

# Pricing Plans
PLANS = {
    'free': {
        'name': 'Free Trial',
        'price': 0,
        'audits': 1,
        'features': ['1 audit', 'Basic SEO score', 'Critical errors only'],
        'color': '#888'
    },
    'starter': {
        'name': 'Starter',
        'price': 1500,
        'audits': 5,
        'features': ['5 audits/month', 'SEO score', 'Critical errors', 'White-label PDF', 'Email support'],
        'color': '#ff6b6b'
    },
    'pro': {
        'name': 'Pro',
        'price': 2000,
        'audits': -1,  # Unlimited
        'features': ['Unlimited audits', 'Deep AI audit', 'Prioritized fixes', 'Competitor comparison', 'Export for clients', 'Priority support'],
        'color': '#4ecdc4'
    },
    'agency': {
        'name': 'Agency',
        'price': 'Custom',
        'audits': -1,
        'features': ['Everything in Pro', 'Client dashboard', 'Full white-label', 'Lead reports', 'Multi-language', 'Priority AI processing', 'Dedicated account manager'],
        'color': '#ffd700'
    }
}

# --- ELITE STYLING ---
st.markdown("""
<style>
    /* Main */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0000 100%);
        color: white;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a0a0a 100%);
        border-right: 2px solid #ff4b4b;
    }
    
    /* Headers */
    h1, h2, h3 { color: #ffffff; }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #ff4b4b, #cc0000);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 15px 30px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.6);
    }
    
    /* Input */
    .stTextInput>div>div>input {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 12px;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,75,75,0.1) 0%, rgba(0,0,0,0.8) 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ff4b4b;
        box-shadow: 0 8px 32px rgba(255, 75, 75, 0.2);
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
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(255,75,75,0.2) 0%, rgba(0,0,0,0.4) 100%);
        border-radius: 10px;
        color: white;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(45deg, #ff4b4b, #cc0000);
    }
</style>
""", unsafe_allow_html=True)

# --- CORE FUNCTIONS ---

def scrape_website(url):
    """Scrape website for SEO analysis"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'url': url,
            'title': soup.find('title').text if soup.find('title') else 'No title',
            'meta_description': '',
            'h1_tags': len(soup.find_all('h1')),
            'h2_tags': len(soup.find_all('h2')),
            'images': len(soup.find_all('img')),
            'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
            'internal_links': len([a for a in soup.find_all('a', href=True) if url in a['href']]),
            'external_links': len([a for a in soup.find_all('a', href=True) if url not in a['href'] and a['href'].startswith('http')]),
            'word_count': len(soup.get_text().split()),
            'has_robots': soup.find('meta', {'name': 'robots'}) is not None,
            'has_canonical': soup.find('link', {'rel': 'canonical'}) is not None,
            'load_time': response.elapsed.total_seconds(),
            'status_code': response.status_code
        }
        
        # Meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        return data, soup.get_text()[:5000]  # First 5000 chars for AI analysis
    except Exception as e:
        return None, str(e)

def calculate_seo_score(data):
    """Calculate SEO score based on multiple factors"""
    score = 100
    issues = []
    
    # Title
    if not data.get('title') or data['title'] == 'No title':
        score -= 15
        issues.append('❌ Missing page title')
    elif len(data['title']) < 30 or len(data['title']) > 60:
        score -= 5
        issues.append('⚠️ Title length not optimal (30-60 chars)')
    
    # Meta description
    if not data.get('meta_description'):
        score -= 10
        issues.append('❌ Missing meta description')
    elif len(data['meta_description']) < 120 or len(data['meta_description']) > 160:
        score -= 5
        issues.append('⚠️ Meta description length not optimal (120-160 chars)')
    
    # H1 tags
    if data['h1_tags'] == 0:
        score -= 10
        issues.append('❌ No H1 tag found')
    elif data['h1_tags'] > 1:
        score -= 5
        issues.append('⚠️ Multiple H1 tags found')
    
    # Images
    if data['images_without_alt'] > 0:
        score -= min(10, data['images_without_alt'] * 2)
        issues.append(f'⚠️ {data["images_without_alt"]} images without alt text')
    
    # Content
    if data['word_count'] < 300:
        score -= 10
        issues.append('❌ Thin content (less than 300 words)')
    
    # Technical
    if not data.get('has_robots'):
        score -= 5
        issues.append('⚠️ Missing robots meta tag')
    
    if not data.get('has_canonical'):
        score -= 5
        issues.append('⚠️ Missing canonical URL')
    
    # Load time
    if data.get('load_time', 0) > 3:
        score -= 10
        issues.append('❌ Slow page load time (>3 seconds)')
    
    return max(0, score), issues

def get_ai_analysis(url, scraped_data, content_sample):
    """Get AI-powered deep analysis using Gemini"""
    if not gemini_model:
        return "AI analysis unavailable. Please configure GEMINI_API_KEY."
    
    try:
        prompt = f"""
        You are an expert SEO consultant. Analyze this website comprehensively:
        
        URL: {url}
        
        Technical Data:
        - Title: {scraped_data.get('title')}
        - Meta Description: {scraped_data.get('meta_description')}
        - H1 Tags: {scraped_data.get('h1_tags')}
        - Word Count: {scraped_data.get('word_count')}
        - Images: {scraped_data.get('images')} (without alt: {scraped_data.get('images_without_alt')})
        - Internal Links: {scraped_data.get('internal_links')}
        - External Links: {scraped_data.get('external_links')}
        - Load Time: {scraped_data.get('load_time')}s
        
        Content Sample:
        {content_sample[:1000]}
        
        Provide a detailed analysis with:
        1. **SEO Score Breakdown** (0-100)
        2. **Critical Issues** (must fix immediately)
        3. **Priority Improvements** (high impact)
        4. **Content Strategy** (keywords, topics, structure)
        5. **Technical Recommendations** (speed, mobile, security)
        6. **Competitive Advantages** (what to leverage)
        7. **30-Day Action Plan** (specific steps)
        
        Format as markdown with clear sections and bullet points.
        """
        
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI analysis error: {str(e)}"

def save_audit_to_db(user_email, url, score, plan):
    """Save audit to Supabase"""
    if not supabase:
        return
    
    try:
        supabase.table('audits').insert({
            'user_email': user_email,
            'url': url,
            'score': score,
            'plan': plan,
            'created_at': datetime.now().isoformat()
        }).execute()
    except Exception as e:
        st.error(f"Database error: {e}")

def get_user_audits(user_email):
    """Get user's audit history"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('audits').select('*').eq('user_email', user_email).order('created_at', desc=True).limit(10).execute()
        return response.data
    except:
        return []

# --- AUTHENTICATION ---

def register_user(email, password):
    try:
        if supabase:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Initialize user in database
                try:
                    supabase.table('users').insert({
                        'email': email,
                        'plan': 'free',
                        'audits_used': 0,
                        'created_at': datetime.now().isoformat()
                    }).execute()
                except:
                    pass
                
                st.session_state.user = response.user
                st.session_state.authenticated = True
                st.session_state.user_plan = 'free'
                return "success", "Account created! You have 1 free audit."
    except Exception as e:
        if "already" in str(e).lower():
            return "error", "Email already registered"
    
    # Fallback demo mode
    if email not in st.session_state.temp_users:
        st.session_state.temp_users[email] = {'password': password, 'plan': 'free', 'audits': 0}
        return "demo", "Demo account created! You can login now."
    
    return "error", "Registration failed"

def login_user(email, password):
    try:
        if supabase:
            response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Get user plan
                try:
                    user_data = supabase.table('users').select('*').eq('email', email).execute()
                    if user_data.data:
                        st.session_state.user_plan = user_data.data[0].get('plan', 'free')
                        st.session_state.audits_used = user_data.data[0].get('audits_used', 0)
                except:
                    st.session_state.user_plan = 'free'
                
                st.session_state.user = response.user
                st.session_state.authenticated = True
                return "success", "Welcome back!"
    except Exception as e:
        # Demo mode fallback
        if email in st.session_state.temp_users and st.session_state.temp_users[email]['password'] == password:
            st.session_state.authenticated = True
            st.session_state.user = {"email": email}
            st.session_state.user_plan = st.session_state.temp_users[email]['plan']
            st.session_state.audits_used = st.session_state.temp_users[email]['audits']
            return "demo", "Demo login successful"
    
    return "error", "Invalid credentials"

# --- UI PAGES ---

def auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 50px 0;'>
            <h1 style='font-size: 60px; margin-bottom: 10px;'>🚀 NEXUS SEO</h1>
            <p style='font-size: 24px; color: #888;'>AI-Powered SEO Intelligence for Agencies</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show pricing tiers
        show_pricing_cards()
        
        st.markdown("---")
        
        # Auth forms
        tab_login, tab_register = st.tabs(["🔑 Login", "✨ Start Free Trial"])
        
        with tab_login:
            login_email = st.text_input("Email", key="login_email")
            login_pwd = st.text_input("Password", type="password", key="login_pwd")
            
            if st.button("LOGIN", key="login_btn"):
                if login_email and login_pwd:
                    status, msg = login_user(login_email, login_pwd)
                    if "success" in status or "demo" in status:
                        st.success(msg)
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.warning("Please fill all fields")
        
        with tab_register:
            reg_email = st.text_input("Email", key="reg_email")
            reg_pwd = st.text_input("Password (min 6 chars)", type="password", key="reg_pwd")
            reg_pwd2 = st.text_input("Confirm Password", type="password", key="reg_pwd2")
            
            st.info("💡 Start with 1 free audit. No credit card required!")
            
            if st.button("START FREE TRIAL", key="reg_btn"):
                if not reg_email or not reg_pwd:
                    st.warning("Please fill all fields")
                elif len(reg_pwd) < 6:
                    st.warning("Password must be at least 6 characters")
                elif reg_pwd != reg_pwd2:
                    st.error("Passwords don't match")
                else:
                    status, msg = register_user(reg_email, reg_pwd)
                    if "success" in status:
                        st.success(msg)
                        time.sleep(1)
                        st.rerun()
                    elif "demo" in status:
                        st.success(msg)
                    else:
                        st.error(msg)

def show_pricing_cards():
    st.markdown("### 💎 Choose Your Plan")
    
    cols = st.columns(4)
    
    for idx, (key, plan) in enumerate(PLANS.items()):
        with cols[idx]:
            price_display = f"€{plan['price']}/mo" if isinstance(plan['price'], int) else plan['price']
            
            st.markdown(f"""
            <div style='
                border: 2px solid {plan["color"]};
                border-radius: 15px;
                padding: 25px;
                background: rgba(0,0,0,0.5);
                height: 400px;
                display: flex;
                flex-direction: column;
            '>
                <h3 style='color: {plan["color"]}; margin-top: 0;'>{plan["name"]}</h3>
                <h2 style='color: white; margin: 10px 0;'>{price_display}</h2>
                <div style='flex-grow: 1;'>
            """, unsafe_allow_html=True)
            
            for feature in plan['features']:
                st.markdown(f"✅ {feature}")
            
            st.markdown("</div></div>", unsafe_allow_html=True)

def main_dashboard():
    # Sidebar
    with st.sidebar:
        user_email = st.session_state.user.get('email', 'User') if isinstance(st.session_state.user, dict) else st.session_state.user.email
        
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ff4b4b, #cc0000); border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: white;'>👤 {user_email}</h3>
            <p style='margin: 5px 0; color: white;'>Plan: {PLANS[st.session_state.user_plan]["name"]}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Audit usage
        plan_audits = PLANS[st.session_state.user_plan]['audits']
        if plan_audits == -1:
            st.success("✅ Unlimited audits")
        else:
            remaining = plan_audits - st.session_state.audits_used
            st.metric("Audits Remaining", f"{remaining}/{plan_audits}")
            if remaining == 0:
                st.error("❌ No audits left. Upgrade your plan!")
        
        st.markdown("---")
        
        page = st.radio("Navigation", [
            "🎯 New Audit",
            "📊 Audit History",
            "💎 Upgrade Plan",
            "⚙️ Settings"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            if supabase:
                try:
                    supabase.auth.sign_out()
                except:
                    pass
            st.rerun()
    
    # Main content
    if "New Audit" in page:
        show_audit_page()
    elif "History" in page:
        show_history_page()
    elif "Upgrade" in page:
        show_upgrade_page()
    else:
        show_settings_page()

def show_audit_page():
    st.markdown("# 🎯 SEO Audit Intelligence")
    st.markdown("AI-powered comprehensive SEO analysis powered by Google Gemini Pro")
    
    # Check audit limits
    plan_audits = PLANS[st.session_state.user_plan]['audits']
    can_audit = plan_audits == -1 or st.session_state.audits_used < plan_audits
    
    if not can_audit:
        st.error("❌ You've reached your audit limit. Please upgrade your plan.")
        if st.button("⬆️ Upgrade Now"):
            st.rerun()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        url = st.text_input("🌐 Website URL", placeholder="https://example.com")
        
        audit_type = st.selectbox("Analysis Type", [
            "Quick Audit (Basic SEO)",
            "Deep Audit (AI-Powered)",
            "Competitor Analysis",
            "Full Report (PDF)"
        ])
        
        if st.button("🚀 START AUDIT", use_container_width=True):
            if not url:
                st.warning("Please enter a URL")
            elif not url.startswith('http'):
                st.warning("Please include http:// or https://")
            else:
                run_audit(url, audit_type)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.metric("Audits This Month", st.session_state.audits_used)
        st.metric("Current Plan", PLANS[st.session_state.user_plan]['name'])
        st.metric("AI Model", "Gemini Pro")

def run_audit(url, audit_type):
    with st.status("🔄 Running SEO Audit...", expanded=True) as status:
        # Step 1: Scrape
        st.write("📡 Connecting to website...")
        scraped_data, content = scrape_website(url)
        
        if not scraped_data:
            st.error(f"❌ Failed to access website: {content}")
            return
        
        time.sleep(0.5)
        
        # Step 2: Calculate score
        st.write("🔍 Analyzing SEO factors...")
        score, issues = calculate_seo_score(scraped_data)
        time.sleep(0.5)
        
        # Step 3: AI Analysis (for Pro/Agency)
        ai_analysis = None
        if st.session_state.user_plan in ['pro', 'agency'] and 'Deep' in audit_type:
            st.write("🤖 Running AI deep analysis...")
            ai_analysis = get_ai_analysis(url, scraped_data, content)
            time.sleep(1)
        
        status.update(label="✅ Audit Complete!", state="complete")
    
    # Update usage
    st.session_state.audits_used += 1
    
    # Save to database
    user_email = st.session_state.user.get('email', 'demo') if isinstance(st.session_state.user, dict) else st.session_state.user.email
    save_audit_to_db(user_email, url, score, st.session_state.user_plan)
    
    # Display results
    display_audit_results(url, score, issues, scraped_data, ai_analysis)

def display_audit_results(url, score, issues, data, ai_analysis):
    st.markdown("---")
    st.markdown("## 📊 Audit Results")
    
    # Score display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = "#00ff00" if score >= 80 else "#ffaa00" if score >= 60 else "#ff0000"
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: rgba(0,0,0,0.5); border-radius: 15px; border: 3px solid {score_color};'>
            <h1 style='font-size: 60px; margin: 0; color: {score_color};'>{score}</h1>
            <p style='margin: 5px; color: white;'>SEO Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Page Load", f"{data.get('load_time', 0):.2f}s")
        st.metric("Word Count", data.get('word_count', 0))
    
    with col3:
        st.metric("Images", data.get('images', 0))
        st.metric("Missing Alt", data.get('images_without_alt', 0))
    
    with col4:
        st.metric("Internal Links", data.get('internal_links', 0))
        st.metric("External Links", data.get('external_links', 0))
    
    # Issues
    st.markdown("### 🚨 Critical Issues & Recommendations")
    for issue in issues:
        st.markdown(issue)
    
    # Technical details
    with st.expander("📋 Technical Details"):
        st.json(data)
    
    # AI Analysis (Pro/Agency only)
    if ai_analysis:
        st.markdown("### 🤖 AI Deep Analysis (Powered by Gemini Pro)")
        st.markdown(ai_analysis)
    elif st.session_state.user_plan == 'free':
        st.info("💎 Upgrade to Pro or Agency plan to unlock AI-powered deep analysis with actionable insights!")
    
    # Export options (Pro/Agency)
    if st.session_state.user_plan in ['pro', 'agency']:
        st.markdown("### 📄 Export Report")
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            if st.button("📊 Export as PDF"):
                st.success("PDF generation coming soon!")
        with col_e2:
            if st.button("📧 Email Report"):
                st.success("Email sent!")
        with col_e3:
            if st.button("💾 Save to Dashboard"):
                st.success("Saved!")

def show_history_page():
    st.markdown("# 📊 Audit History")
    
    user_email = st.session_state.user.get('email', 'demo') if isinstance(st.session_state.user, dict) else st.session_state.user.email
    audits = get_user_audits(user_email)
    
    if audits:
        df = pd.DataFrame(audits)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No audits yet. Run your first audit!")

def show_upgrade_page():
    st.markdown("# 💎 Upgrade Your Plan")
    show_pricing_cards()
    
    st.markdown("---")
    st.markdown("### 🎯 Why Upgrade?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🚀 Starter Benefits
        - Perfect for freelancers
        - 5 audits per month
        - White-label reports
        - Build client trust
        - ROI: €300+ per audit
        """)
    
    with col2:
        st.markdown("""
        #### ⚡ Pro Benefits
        - Unlimited audits
        - AI-powered insights
        - Competitor analysis
        - Priority support
        - 10x your agency value
        """)

def show_settings_page():
    st.markdown("# ⚙️ Settings")
    
    st.markdown("### 👤 Account")
    user_email = st.session_state.user.get('email', 'demo') if isinstance(st.session_state.user, dict) else st.session_state.user.email
    st.text_input("Email", value=user_email, disabled=True)
    
    st.markdown("### 🔔 Notifications")
    st.checkbox("Email reports", value=True)
    st.checkbox("Weekly summaries", value=False)
    
    st.markdown("### 🎨 Branding (Agency Plan)")
    if st.session_state.user_plan == 'agency':
        st.text_input("Company Name")
        st.color_picker("Brand Color")
        st.file_uploader("Upload Logo")
    else:
        st.info("Upgrade to Agency plan for white-label branding")

# --- MAIN ---

def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
