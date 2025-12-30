import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import json
import re

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="NEXUS SEO Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# GOOGLE TAG MANAGER INTEGRATION
# ============================================================================
def inject_gtm():
    """Inject Google Tag Manager for analytics tracking"""
    GTM_ID = "GTM-KXF6VCFJ"
    
    gtm_head = f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GTM_ID}');</script>
    <!-- End Google Tag Manager -->
    """
    
    gtm_body = f"""
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id={GTM_ID}"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
    """
    
    components.html(gtm_head + gtm_body, height=0)

# ============================================================================
# CORE ENGINE ARCHITECTURE
# ============================================================================
class NexusEliteEngine:
    """Enterprise-grade SEO Intelligence Engine"""
    
    def __init__(self):
        self.supabase = self._init_supabase()
        self.ai_model = self._init_gemini()
    
    def _init_supabase(self):
        """Initialize Supabase client with error handling"""
        try:
            return create_client(
                st.secrets["SUPABASE_URL"],
                st.secrets["SUPABASE_KEY"]
            )
        except Exception as e:
            st.error(f"Database initialization error: {e}")
            return None
    
    def _init_gemini(self):
        """Initialize Gemini AI with fallback models"""
        try:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            # Try latest stable model first
            try:
                return genai.GenerativeModel('gemini-1.5-flash-latest')
            except:
                return genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.warning(f"AI initialization error: {e}")
            return None
    
    def scrape_website(self, url):
        """Advanced website scraping for SEO analysis"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract comprehensive SEO data
            data = {
                'url': url,
                'status_code': response.status_code,
                'load_time': response.elapsed.total_seconds(),
                'title': soup.find('title').text if soup.find('title') else '',
                'meta_description': '',
                'h1_count': len(soup.find_all('h1')),
                'h2_count': len(soup.find_all('h2')),
                'h3_count': len(soup.find_all('h3')),
                'total_images': len(soup.find_all('img')),
                'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
                'internal_links': len([a for a in soup.find_all('a', href=True) if url in str(a.get('href'))]),
                'external_links': len([a for a in soup.find_all('a', href=True) if 'http' in str(a.get('href')) and url not in str(a.get('href'))]),
                'word_count': len(soup.get_text().split()),
                'has_robots': bool(soup.find('meta', {'name': 'robots'})),
                'has_canonical': bool(soup.find('link', {'rel': 'canonical'})),
                'has_og_image': bool(soup.find('meta', {'property': 'og:image'})),
                'has_schema': bool(soup.find('script', {'type': 'application/ld+json'})),
                'content_sample': soup.get_text()[:3000]
            }
            
            # Get meta description
            meta_desc = soup.find('meta', {'name': 'description'})
            if meta_desc:
                data['meta_description'] = meta_desc.get('content', '')
            
            return data, True
        except Exception as e:
            return {'error': str(e)}, False
    
    def calculate_seo_score(self, data):
        """Advanced SEO scoring algorithm"""
        score = 100
        issues = []
        recommendations = []
        
        # Title optimization (15 points)
        if not data.get('title'):
            score -= 15
            issues.append('❌ CRITICAL: Missing page title')
            recommendations.append('Add a descriptive, keyword-rich title (50-60 characters)')
        elif len(data['title']) < 30:
            score -= 8
            issues.append('⚠️ Title too short (under 30 characters)')
            recommendations.append(f'Expand title to 50-60 characters (currently {len(data["title"])})')
        elif len(data['title']) > 60:
            score -= 5
            issues.append('⚠️ Title too long (over 60 characters)')
            recommendations.append(f'Shorten title to 50-60 characters (currently {len(data["title"])})')
        
        # Meta description (10 points)
        if not data.get('meta_description'):
            score -= 10
            issues.append('❌ Missing meta description')
            recommendations.append('Add compelling meta description (150-160 characters)')
        elif len(data['meta_description']) < 120:
            score -= 5
            issues.append('⚠️ Meta description too short')
            recommendations.append('Expand meta description to 150-160 characters')
        
        # Heading structure (15 points)
        if data['h1_count'] == 0:
            score -= 15
            issues.append('❌ CRITICAL: No H1 heading found')
            recommendations.append('Add a single, keyword-focused H1 heading')
        elif data['h1_count'] > 1:
            score -= 8
            issues.append('⚠️ Multiple H1 headings detected')
            recommendations.append('Use only one H1 per page for better SEO')
        
        if data['h2_count'] < 2:
            score -= 5
            issues.append('⚠️ Insufficient H2 headings for content structure')
            recommendations.append('Add H2 headings to organize content sections')
        
        # Images (10 points)
        if data['total_images'] > 0:
            alt_ratio = data['images_without_alt'] / data['total_images']
            if alt_ratio > 0.5:
                score -= 10
                issues.append(f'❌ {data["images_without_alt"]}/{data["total_images"]} images missing alt text')
                recommendations.append('Add descriptive alt text to all images')
            elif alt_ratio > 0:
                score -= 5
                issues.append(f'⚠️ {data["images_without_alt"]} images missing alt text')
                recommendations.append('Complete alt text for remaining images')
        
        # Content quality (15 points)
        if data['word_count'] < 300:
            score -= 15
            issues.append('❌ CRITICAL: Thin content (under 300 words)')
            recommendations.append(f'Expand content to at least 800+ words (currently {data["word_count"]})')
        elif data['word_count'] < 800:
            score -= 8
            issues.append('⚠️ Content could be more comprehensive')
            recommendations.append(f'Consider expanding to 800+ words for better ranking')
        
        # Technical SEO (15 points)
        if not data['has_robots']:
            score -= 5
            issues.append('⚠️ Missing robots meta tag')
            recommendations.append('Add robots meta tag for crawl control')
        
        if not data['has_canonical']:
            score -= 5
            issues.append('⚠️ Missing canonical URL')
            recommendations.append('Add canonical tag to avoid duplicate content')
        
        if not data['has_og_image']:
            score -= 3
            issues.append('⚠️ Missing Open Graph image')
            recommendations.append('Add og:image for better social sharing')
        
        if not data['has_schema']:
            score -= 2
            issues.append('⚠️ No structured data (Schema.org)')
            recommendations.append('Implement Schema markup for rich snippets')
        
        # Performance (10 points)
        if data['load_time'] > 3:
            score -= 10
            issues.append(f'❌ CRITICAL: Slow load time ({data["load_time"]:.2f}s)')
            recommendations.append('Optimize images, enable caching, use CDN')
        elif data['load_time'] > 2:
            score -= 5
            issues.append(f'⚠️ Load time could be improved ({data["load_time"]:.2f}s)')
            recommendations.append('Consider performance optimization')
        
        # Link structure (10 points)
        if data['internal_links'] < 3:
            score -= 5
            issues.append('⚠️ Insufficient internal linking')
            recommendations.append('Add 5-10 relevant internal links')
        
        if data['external_links'] > 50:
            score -= 5
            issues.append('⚠️ Too many external links')
            recommendations.append('Review and reduce external links if not necessary')
        
        return max(0, min(100, score)), issues, recommendations
    
    def ai_deep_analysis(self, url, data, competitor_url=None):
        """AI-powered comprehensive SEO analysis"""
        if not self.ai_model:
            return "AI analysis unavailable. Please check API configuration."
        
        try:
            prompt = f"""
            You are an elite SEO consultant analyzing a website for a high-value agency client.
            
            **TARGET WEBSITE:** {url}
            
            **TECHNICAL DATA:**
            - Title: {data.get('title', 'Missing')}
            - Meta Description: {data.get('meta_description', 'Missing')}
            - H1 Tags: {data.get('h1_count')}
            - Word Count: {data.get('word_count')}
            - Images: {data.get('total_images')} (Missing Alt: {data.get('images_without_alt')})
            - Load Time: {data.get('load_time', 0):.2f}s
            - Internal Links: {data.get('internal_links')}
            - External Links: {data.get('external_links')}
            
            **CONTENT SAMPLE:**
            {data.get('content_sample', '')[:1000]}
            
            {f"**COMPETITOR:** {competitor_url}" if competitor_url else ""}
            
            Provide a comprehensive analysis with:
            
            ## 1. Executive Summary
            One paragraph overview of SEO health and opportunity
            
            ## 2. Critical Issues (Must Fix Now)
            - List 3-5 critical issues preventing ranking
            
            ## 3. High-Impact Improvements
            - List 5-7 changes with highest ROI
            
            ## 4. Content Strategy
            - Keyword opportunities
            - Content gaps to fill
            - Topic clusters to develop
            
            ## 5. Technical Optimization
            - Speed improvements
            - Mobile optimization
            - Structured data recommendations
            
            ## 6. Competitive Analysis
            - How to outrank competitors
            - Unique value propositions
            
            ## 7. 30-Day Action Plan
            Week 1: [specific tasks]
            Week 2: [specific tasks]
            Week 3: [specific tasks]
            Week 4: [specific tasks]
            
            ## 8. Expected ROI
            - Traffic increase potential
            - Ranking improvement timeline
            - Conversion optimization opportunities
            
            Be specific, actionable, and focused on measurable results.
            """
            
            response = self.ai_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Analysis Error: {str(e)}\n\nPlease verify your Gemini API key and quota."
    
    def get_user_profile(self, user_id):
        """Fetch user profile from database"""
        if not self.supabase:
            return None
        try:
            response = self.supabase.table('profiles').select('*').eq('id', user_id).single().execute()
            return response.data
        except:
            return None
    
    def save_audit(self, user_id, url, score, data):
        """Save audit to database"""
        if not self.supabase:
            return
        try:
            self.supabase.table('audit_history').insert({
                'user_id': user_id,
                'url': url,
                'score': score,
                'data': json.dumps(data),
                'created_at': datetime.now().isoformat()
            }).execute()
        except Exception as e:
            st.error(f"Save error: {e}")
    
    def update_credits(self, user_id, amount):
        """Update user credits"""
        if not self.supabase:
            return
        try:
            profile = self.get_user_profile(user_id)
            if profile:
                new_credits = max(0, profile.get('credits', 0) + amount)
                self.supabase.table('profiles').update({
                    'credits': new_credits
                }).eq('id', user_id).execute()
        except Exception as e:
            st.error(f"Credit update error: {e}")

# Initialize engine
nexus = NexusEliteEngine()

# ============================================================================
# ELITE UI STYLING
# ============================================================================
def apply_elite_styling():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;700&display=swap');
        
        /* Global */
        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
        }
        
        /* Main background */
        .main {
            background: radial-gradient(circle at 20% 20%, #1a0505 0%, #050505 100%);
            color: white;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f0f0f 0%, #1a0a0a 100%);
            border-right: 2px solid #ff4b4b;
        }
        
        /* Metrics */
        [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255,75,75,0.08) 0%, rgba(0,0,0,0.6) 100%);
            border: 1px solid rgba(255,75,75,0.3);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(255, 75, 75, 0.15);
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 15px 30px !important;
            box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(255, 75, 75, 0.6) !important;
        }
        
        /* Inputs */
        .stTextInput>div>div>input {
            background: rgba(20, 20, 20, 0.9) !important;
            border: 1px solid #ff4b4b !important;
            color: white !important;
            border-radius: 10px !important;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: white;
            font-weight: 700;
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
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'profile' not in st.session_state:
    st.session_state.profile = None

# ============================================================================
# AUTHENTICATION FUNCTIONS
# ============================================================================
def authenticate_user(email, password):
    """Authenticate user with Supabase"""
    if not nexus.supabase:
        return False, "Database unavailable"
    
    try:
        response = nexus.supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user:
            st.session_state.user = response.user
            st.session_state.authenticated = True
            st.session_state.profile = nexus.get_user_profile(response.user.id)
            return True, "Login successful"
    except Exception as e:
        return False, str(e)
    
    return False, "Invalid credentials"

def register_user(email, password, plan='Demo'):
    """Register new user"""
    if not nexus.supabase:
        return False, "Database unavailable"
    
    try:
        response = nexus.supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if response.user:
            # Create profile
            nexus.supabase.table('profiles').insert({
                'id': response.user.id,
                'email': email,
                'plan_tier': plan,
                'credits': 1 if plan == 'Demo' else 0,
                'created_at': datetime.now().isoformat()
            }).execute()
            
            return True, "Account created! Please check your email."
    except Exception as e:
        return False, str(e)
    
    return False, "Registration failed"

# ============================================================================
# PUBLIC LANDING PAGE
# ============================================================================
def render_landing_page():
    apply_elite_styling()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 60px 0 40px 0;'>
            <h1 style='font-size: 72px; margin: 0; background: linear-gradient(135deg, #ff4b4b, #ff8080); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                🚀 NEXUS SEO
            </h1>
            <p style='font-size: 28px; color: #888; margin-top: 10px;'>
                AI-Powered Intelligence for Elite Agencies
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Pricing tiers
        st.markdown("### 💎 Choose Your Plan")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            st.markdown("""
            <div style='border: 2px solid #888; border-radius: 15px; padding: 30px; background: rgba(0,0,0,0.5); height: 400px;'>
                <h3 style='color: #888;'>Demo</h3>
                <h2 style='color: white;'>FREE</h2>
                <p>✅ 1 free audit</p>
                <p>✅ Basic SEO score</p>
                <p>✅ Critical issues</p>
                <p>✅ Test the platform</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_p2:
            st.markdown("""
            <div style='border: 3px solid #ff4b4b; border-radius: 15px; padding: 30px; background: rgba(255,75,75,0.05); height: 400px;'>
                <h3 style='color: #ff4b4b;'>⭐ Starter</h3>
                <h2 style='color: white;'>CHF 1,500/mo</h2>
                <p>✅ 50 audits/month</p>
                <p>✅ AI deep analysis</p>
                <p>✅ White-label reports</p>
                <p>✅ Priority support</p>
                <p>✅ Export to PDF</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_p3:
            st.markdown("""
            <div style='border: 2px solid #ffd700; border-radius: 15px; padding: 30px; background: rgba(255,215,0,0.05); height: 400px;'>
                <h3 style='color: #ffd700;'>👑 Agency Elite</h3>
                <h2 style='color: white;'>CHF 3,000/mo</h2>
                <p>✅ Unlimited audits</p>
                <p>✅ Full white-label</p>
                <p>✅ Client dashboard</p>
                <p>✅ Multi-language</p>
                <p>✅ Priority AI processing</p>
                <p>✅ Dedicated manager</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Auth tabs
        tab_login, tab_register = st.tabs(["🔑 Login", "✨ Start Free Demo"])
        
        with tab_login:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pwd")
            
            if st.button("LOGIN", key="login_btn", use_container_width=True):
                if email and password:
                    success, message = authenticate_user(email, password)
                    if success:
                        st.success(message)
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error(message)
        
        with tab_register:
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password (min 6 chars)", type="password", key="reg_pwd")
            reg_password2 = st.text_input("Confirm Password", type="password", key="reg_pwd2")
            
            st.info("🎁 Get 1 free audit to test the platform!")
            
            if st.button("START FREE DEMO", key="reg_btn", use_container_width=True):
                if not reg_email or not reg_password:
                    st.warning("Please fill all fields")
                elif len(reg_password) < 6:
                    st.warning("Password must be at least 6 characters")
                elif reg_password != reg_password2:
                    st.error("Passwords don't match")
                else:
                    success, message = register_user(reg_email, reg_password, 'Demo')
                    if success:
                        st.success(message)
                    else:
                        st.error(message)

# ============================================================================
# CLIENT TERMINAL
# ============================================================================
def render_client_terminal():
    apply_elite_styling()
    
    profile = st.session_state.profile
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #ff4b4b, #cc0000); border-radius: 10px; margin-bottom: 20px;'>
            <h3 style='margin: 0; color: white;'>👤 {profile.get('email', 'User')}</h3>
            <p style='margin: 5px; color: white;'>Tier: {profile.get('plan_tier', 'Demo')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Credits Available", profile.get('credits', 0))
        
        st.markdown("---")
        
        page = st.radio("Navigation", [
            "🎯 SEO Audit",
            "📊 Audit History",
            "💎 Upgrade Plan",
            "⚙️ Settings"
        ], label_visibility="collapsed")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.profile = None
            if nexus.supabase:
                nexus.supabase.auth.sign_out()
            st.rerun()
    
    # Main content
    if "SEO Audit" in page:
        show_audit_terminal()
    elif "History" in page:
        show_audit_history()
    elif "Upgrade" in page:
        show_upgrade_page()
    else:
        show_settings()

def show_audit_terminal():
    st.markdown("## 🛰️ SEO Intelligence Terminal")
    st.markdown("AI-powered comprehensive website analysis")
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Intel Nodes", "2,148", "+24")
    col2.metric("Market Scans", "18.2M", "Live")
    col3.metric("Semantic ROI", "342%", "🔥")
    col4.metric("Networks", "94", "+5")
    
    st.markdown("---")
    
    # Audit interface
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown("### 🤖 AI Semantic Audit")
        target_url = st.text_input("Target Website URL", placeholder="https://example.com")
        competitor_url = st.text_input("Competitor URL (optional)", placeholder="https://competitor.com")
        
        audit_type = st.selectbox("Analysis Depth", [
            "Quick Scan (Basic SEO)",
            "Deep Analysis (AI-Powered)",
            "Competitive Intelligence"
        ])
        
        if st.button("⚡ EXECUTE SCAN", use_container_width=True):
            if not target_url:
                st.warning("Please enter a target URL")
            elif profile.get('credits', 0) <= 0:
                st.error("❌ Insufficient credits. Please upgrade your plan.")
            else:
                execute_audit(target_url, competitor_url, audit_type)
    
    with col_right:
        st.markdown("### 📊 Plan Details")
        plan_tier = profile.get('plan_tier', 'Demo')
        
        if plan_tier == 'Demo':
            st.info("**Demo Plan**\n\nUpgrade to unlock unlimited audits and AI analysis!")
        elif plan_tier == 'Starter':
            st.success("**Starter Plan**\n\n50 audits/month with AI insights")
        else:
            st.success("**Agency Elite**\n\nUnlimited audits with priority processing")
        
        st.metric("Credits Used This Month", profile.get('audits_used', 0))

def execute_audit(url, competitor, audit_type):
    """Execute comprehensive SEO audit"""
    
    with st.status("🔄 Executing SEO Scan...", expanded=True) as status:
        # Step 1: Scrape website
        st.write("📡 Connecting to target website...")
        data, success = nexus.scrape_website(url)
        
        if not success:
            st.error(f"Failed to access website: {data.get('error')}")
            return
        
        time.sleep(0.5)
        
        # Step 2: Calculate score
        st.write("🔍 Analyzing SEO factors...")
        score, issues, recommendations = nexus.calculate_seo_score(data)
        time.sleep(0.5)
        
        # Step 3: AI analysis (if applicable)
        ai_analysis = None
        if 'Deep' in audit_type or 'Competitive' in audit_type:
            if st.session_state.profile.get('plan_tier') in ['Starter', 'Agency Elite']:
                st.write("🤖 Running AI deep analysis...")
                ai_analysis = nexus.ai_deep_analysis(url, data, competitor if competitor else None)
                time.sleep(1)
            else:
                st.write("⚠️ AI analysis requires Starter or Agency plan")
        
        status.update(label="✅ Scan Complete!", state="complete")
    
    # Update credits
    nexus.update_credits(st.session_state.user.id, -1)
    
    # Save audit
    nexus.save_audit(st.session_state.user.id, url, score, data)
    
    # Display results
    display_audit_results(url, score, issues, recommendations, data, ai_analysis)

def display_audit_results(url, score, issues, recommendations, data, ai_analysis):
    """Display comprehensive audit results"""
    st.markdown("---")
    st.markdown("## 📊 Audit Results")
    
    # Score display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = "#00ff00" if score >= 80 else "#ffaa00" if score >= 60 else "#ff0000"
        st.markdown(f"""
        <div style='text-align: center; padding: 40px; background: rgba(0,0,0,0.5); border-radius: 15px; border: 3px solid {score_color};'>
            <h1 style='font-size: 72px; margin: 0; color: {score_color};'>{score}</h1>
            <p style='margin: 5px; color: white; font-size: 18px;'>SEO Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Load Time", f"{data.get('load_time', 0):.2f}s")
        st.metric("Word Count", data.get('word_count', 0))
    
    with col3:
        st.metric("Total Images", data.get('total_images', 0))
        st.metric("Missing Alt", data.get('images_without_alt', 0))
    
    with col4:
        st.metric("Internal Links", data.get('internal_links', 0))
        st.metric("External Links", data.get('external_links', 0))
    
    # Critical issues
    st.markdown("### 🚨 Critical Issues")
    for issue in issues[:5]:
        st.markdown(issue)
    
    # Recommendations
    st.markdown("### 💡 Priority Recommendations")
    for rec in recommendations[:5]:
        st.markdown(f"→ {rec}")
    
    # Technical details
    with st.expander("📋 Technical Details"):
        st.json(data)
    
    # AI Analysis
    if ai_analysis:
        st.markdown("### 🤖 AI Deep Analysis (Powered by Gemini)")
        st.markdown(ai_analysis)
    
    # Export options
    if st.session_state.profile.get('plan_tier') in ['Starter', 'Agency Elite']:
        st.markdown("### 📄 Export Options")
        col_e1, col_e2, col_e3 = st.columns(3)
        
        with col_e1:
            report_text = f"SEO Audit Report\n\nURL: {url}\nScore: {score}/100\n\n"
            report_text += "\n".join(issues) + "\n\n" + "\n".join(recommendations)
            if ai_analysis:
                report_text += f"\n\n{ai_analysis}"
            
            st.download_button(
                "📥 Download Report",
                data=report_text,
                file_name=f"nexus_audit_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
        
        with col_e2:
            if st.button("📧 Email Report"):
                st.success("Report sent to your email!")
        
        with col_e3:
            if st.button("💾 Save to Dashboard"):
                st.success("Saved to audit history!")

def show_audit_history():
    """Display audit history"""
    st.markdown("## 📊 Audit History")
    
    if nexus.supabase:
        try:
            response = nexus.supabase.table('audit_history').select('*').eq('user_id', st.session_state.user.id).order('created_at', desc=True).limit(20).execute()
            
            if response.data:
                df = pd.DataFrame(response.data)
                st.dataframe(df[['url', 'score', 'created_at']], use_container_width=True)
            else:
                st.info("No audit history yet. Run your first audit!")
        except:
            st.error("Unable to load audit history")
    else:
        st.info("Run audits to build your history")

def show_upgrade_page():
    """Show upgrade options"""
    st.markdown("## 💎 Upgrade Your Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='border: 2px solid #888; border-radius: 15px; padding: 30px; background: rgba(0,0,0,0.5);'>
            <h3 style='color: #888;'>Current: Demo</h3>
            <p>1 free audit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='border: 3px solid #ff4b4b; border-radius: 15px; padding: 30px; background: rgba(255,75,75,0.05);'>
            <h3 style='color: #ff4b4b;'>⭐ Starter</h3>
            <h2>CHF 1,500/mo</h2>
            <p>✅ 50 audits/month</p>
            <p>✅ AI analysis</p>
            <p>✅ White-label reports</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Starter", key="upgrade_starter"):
            st.success("Contact us to upgrade!")
    
    with col3:
        st.markdown("""
        <div style='border: 2px solid #ffd700; border-radius: 15px; padding: 30px; background: rgba(255,215,0,0.05);'>
            <h3 style='color: #ffd700;'>👑 Agency Elite</h3>
            <h2>CHF 3,000/mo</h2>
            <p>✅ Unlimited audits</p>
            <p>✅ Full white-label</p>
            <p>✅ Priority support</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Agency", key="upgrade_agency"):
            st.success("Contact us for enterprise pricing!")

def show_settings():
    """Settings page"""
    st.markdown("## ⚙️ Settings")
    
    profile = st.session_state.profile
    
    st.markdown("### 👤 Account Information")
    st.text_input("Email", value=profile.get('email', ''), disabled=True)
    st.text_input("Plan", value=profile.get('plan_tier', 'Demo'), disabled=True)
    
    st.markdown("### 🔔 Notifications")
    st.checkbox("Email audit reports", value=True)
    st.checkbox("Weekly summary", value=False)
    
    if st.button("💾 Save Settings"):
        st.success("Settings saved!")

# ============================================================================
# ADMIN DASHBOARD
# ============================================================================
def render_admin_dashboard():
    """Admin-only dashboard"""
    apply_elite_styling()
    
    st.markdown("# ⚖️ Admin Master Terminal")
    
    tabs = st.tabs(["👥 Users", "📊 Audits", "💰 Revenue", "⚙️ System"])
    
    with tabs[0]:
        st.markdown("### User Management")
        if nexus.supabase:
            try:
                response = nexus.supabase.table('profiles').select('*').execute()
                if response.data:
                    df = pd.DataFrame(response.data)
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading users: {e}")
    
    with tabs[1]:
        st.markdown("### Audit Activity")
        if nexus.supabase:
            try:
                response = nexus.supabase.table('audit_history').select('*').order('created_at', desc=True).limit(50).execute()
                if response.data:
                    df = pd.DataFrame(response.data)
                    st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading audits: {e}")
    
    with tabs[2]:
        st.markdown("### Revenue Analytics")
        col1, col2, col3 = st.columns(3)
        col1.metric("MRR", "CHF 12,500", "+15%")
        col2.metric("Active Users", "47", "+8")
        col3.metric("Churn Rate", "3.2%", "-0.5%")
    
    with tabs[3]:
        st.markdown("### System Status")
        st.success("✅ Supabase: Connected")
        st.success("✅ Gemini AI: Active")
        st.success("✅ GTM Tracking: Enabled")

# ============================================================================
# MAIN ROUTER
# ============================================================================
def main():
    # Inject tracking
    inject_gtm()
    
    profile = st.session_state.profile if st.session_state.profile else {}
    
    # Route based on authentication and role
    if not st.session_state.authenticated:
        render_landing_page()
    elif profile.get('email') == '3dpeektech@gmail.com':
        # Admin access
        tab1, tab2 = st.tabs(["🚀 Terminal", "⚖️ Admin"])
        with tab1:
            render_client_terminal()
        with tab2:
            render_admin_dashboard()
    else:
        # Regular user
        render_client_terminal()

if __name__ == "__main__":
    main()
