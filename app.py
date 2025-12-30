# app.py - NEXUS SEO Elite Platform
import streamlit as st
from supabase import create_client
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# ------------------------
# Page configuration
# ------------------------
st.set_page_config(
    page_title="NEXUS SEO Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------
# Initialize Supabase
# ------------------------
@st.cache_resource
def init_supabase():
    try:
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except Exception as e:
        st.error(f"Supabase init error: {e}")
        return None

# ------------------------
# Initialize Gemini AI
# ------------------------
@st.cache_resource
def init_gemini():
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.warning(f"Gemini AI not configured: {e}")
        return None

supabase = init_supabase()
gemini_model = init_gemini()

# ------------------------
# Session state defaults
# ------------------------
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

# ------------------------
# Pricing plans
# ------------------------
PLANS = {
    'free': {
        'name': 'Free Trial', 'price': 0, 'audits': 1,
        'features': ['1 audit', 'Basic SEO score', 'Critical errors only'], 'color': '#888'
    },
    'starter': {
        'name': 'Starter', 'price': 1500, 'audits': 5,
        'features': ['5 audits/month', 'SEO score', 'Critical errors', 'White-label PDF', 'Email support'], 'color': '#ff6b6b'
    },
    'pro': {
        'name': 'Pro', 'price': 2000, 'audits': -1,
        'features': ['Unlimited audits', 'Deep AI audit', 'Prioritized fixes', 'Competitor comparison', 'Export for clients', 'Priority support'], 'color': '#4ecdc4'
    },
    'agency': {
        'name': 'Agency', 'price': 'Custom', 'audits': -1,
        'features': ['Everything in Pro', 'Client dashboard', 'Full white-label', 'Lead reports', 'Multi-language', 'Priority AI processing', 'Dedicated account manager'], 'color': '#ffd700'
    }
}

# ------------------------
# Utility functions
# ------------------------
def scrape_website(url):
    """Scrape website data for SEO analysis."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        data = {
            'url': url,
            'title': soup.title.text if soup.title else 'No title',
            'meta_description': soup.find('meta', {'name': 'description'}).get('content', '') if soup.find('meta', {'name': 'description'}) else '',
            'h1_tags': len(soup.find_all('h1')),
            'h2_tags': len(soup.find_all('h2')),
            'images': len(soup.find_all('img')),
            'images_without_alt': len([img for img in soup.find_all('img') if not img.get('alt')]),
            'internal_links': len([a for a in soup.find_all('a', href=True) if url in a['href']]),
            'external_links': len([a for a in soup.find_all('a', href=True) if url not in a['href'] and a['href'].startswith('http')]),
            'word_count': len(soup.get_text().split()),
            'has_robots': bool(soup.find('meta', {'name': 'robots'})),
            'has_canonical': bool(soup.find('link', {'rel': 'canonical'})),
            'load_time': response.elapsed.total_seconds(),
            'status_code': response.status_code
        }
        return data, soup.get_text()[:5000]
    except Exception as e:
        return None, str(e)

def calculate_seo_score(data):
    """Compute SEO score and critical issues."""
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

    # Content length
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
    if data.get('load_time', 0) > 3:
        score -= 10
        issues.append('❌ Slow page load time (>3s)')

    return max(0, score), issues

def get_ai_analysis(url, scraped_data, content_sample):
    """Generate deep AI SEO analysis via Gemini."""
    if not gemini_model:
        return "AI analysis unavailable. Configure GEMINI_API_KEY in secrets."
    
    try:
        prompt = f"""
        You are an expert SEO consultant. Analyze this website:

        URL: {url}
        Technical Data: {scraped_data}
        Content Sample: {content_sample[:1000]}

        Provide:
        1. SEO Score Breakdown
        2. Critical Issues
        3. Priority Improvements
        4. Content Strategy
        5. Technical Recommendations
        6. Competitive Advantages
        7. 30-Day Action Plan

        Format as markdown.
        """
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI analysis error: {e}"

def save_audit_to_db(user_email, url, score, plan):
    """Save audit results to Supabase."""
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
    """Retrieve user's audit history."""
    if not supabase:
        return []
    try:
        response = supabase.table('audits').select('*').eq('user_email', user_email).order('created_at', desc=True).limit(10).execute()
        return response.data
    except:
        return []

# ------------------------
# Authentication
# ------------------------
def register_user(email, password):
    try:
        if supabase:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                supabase.table('users').insert({
                    'email': email, 'plan': 'free', 'audits_used': 0,
                    'created_at': datetime.now().isoformat()
                }).execute()
                st.session_state.user = res.user
                st.session_state.authenticated = True
                st.session_state.user_plan = 'free'
                return "success", "Account created! 1 free audit."
    except Exception as e:
        if "already" in str(e).lower():
            return "error", "Email already registered"
    
    # Demo fallback
    if email not in st.session_state.temp_users:
        st.session_state.temp_users[email] = {'password': password, 'plan': 'free', 'audits': 0}
        return "demo", "Demo account created! You can login now."
    return "error", "Registration failed"

def login_user(email, password):
    try:
        if supabase:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            if res.user:
                user_data = supabase.table('users').select('*').eq('email', email).execute()
                if user_data.data:
                    st.session_state.user_plan = user_data.data[0].get('plan', 'free')
                    st.session_state.audits_used = user_data.data[0].get('audits_used', 0)
                st.session_state.user = res.user
                st.session_state.authenticated = True
                return "success", "Welcome back!"
    except:
        # Demo fallback
        if email in st.session_state.temp_users and st.session_state.temp_users[email]['password'] == password:
            st.session_state.authenticated = True
            st.session_state.user = {"email": email}
            st.session_state.user_plan = st.session_state.temp_users[email]['plan']
            st.session_state.audits_used = st.session_state.temp_users[email]['audits']
            return "demo", "Demo login successful"
    return "error", "Invalid credentials"

# ------------------------
# Main app
# ------------------------
def main():
    if not st.session_state.authenticated:
        auth_page()
    else:
        main_dashboard()

if __name__ == "__main__":
    main()
