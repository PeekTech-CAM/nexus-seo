import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import re
from datetime import datetime

# --- 1. SECURE ENTERPRISE INITIALIZATION ---
@st.cache_resource
def init_enterprise_engine():
    try:
        # Pulling from secure TOML to prevent GitHub leaks
        supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        firecrawl = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gemini = genai.Client(api_key=st.secrets["GEMINI_KEY"])
        return supabase, firecrawl, gemini
    except Exception as e:
        st.error(f"Initialization Failed. Check API URLs in Secrets. Error: {e}")
        st.stop()

supabase, firecrawl, gemini = init_enterprise_engine()

# --- 2. THE "WOW" VISUALIZATION ENGINE ---
def render_live_analytics(score, priorities):
    """Generates high-end interactive charts for real-time engagement."""
    st.markdown("### 📊 Strategic Intelligence Dashboard")
    col1, col2 = st.columns(2)
    
    with col1:
        # Dynamic Gauge Chart for Strategic Health
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "Strategic Health Score", 'font': {'size': 20}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "#FF4B4B"},
                'steps': [
                    {'range': [0, 50], 'color': "#1a1a1a"},
                    {'range': [50, 80], 'color': "#333333"}],
                'threshold': {'line': {'color': "white", 'width': 4}, 'value': 90}}))
        fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Priority Distribution Pie Chart
        df = pd.DataFrame(list(priorities.items()), columns=['Priority', 'Count'])
        fig_pie = px.pie(df, names='Priority', values='Count', 
                         title="Action Priority Distribution",
                         color_discrete_sequence=["#FF4B4B", "#888888", "#333333"])
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 3. ADVANCED AI AUDIT LOGIC (Structured Data Extraction) ---
def execute_strategic_audit(url, tier):
    config = {"Demo": 3000, "Starter": 7000, "Pro": 15000, "Agency": 25000}
    depth = config.get(tier, 3000)
    
    with st.status("⚡ NEXUS AI: Executing Multi-Vector Scan...") as status:
        scrape = firecrawl.scrape(url)
        raw_content = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # Requests JSON for real-time charting + Professional Roadmap
        prompt = f"""
        Act as a Senior SEO Director for an Enterprise Agency. Analyze {url}. 
        Tier: {tier}.
        
        REQUIRED OUTPUT FORMAT:
        1. Start with a JSON block: {{"score": 85, "priorities": {{"High": 5, "Medium": 3, "Low": 8}}}}
        2. Follow with a text-based STRATEGIC ROADMAP focusing on ROI.
        
        Context: {raw_content[:depth]}
        """
        res = gemini.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 4. PRODUCTION AUTHENTICATION & GATING ---
st.set_page_config(page_title="NEXUS Pro | Strategic SEO", layout="wide")

if "user" not in st.session_state:
    st.sidebar.title("🔐 Enterprise Portal")
    mode = st.sidebar.selectbox("Access Mode", ["Login", "Register Organization"])
    email = st.sidebar.text_input("Corporate ID")
    pwd = st.sidebar.text_input("Access Key", type="password")
    
    if mode == "Register Organization":
        if st.sidebar.button("Establish Profile"):
            try:
                supabase.auth.sign_up({"email": email, "password": pwd})
                st.sidebar.success("Registration Sent. Check Email.")
            except: st.sidebar.error("Network Error. Check Supabase URL.")
    else:
        if st.sidebar.button("Authenticate Access"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = res.user
                st.rerun()
            except: st.sidebar.error("Authorization Denied.")

    # Landing Page Visual Engagement
    st.title("⚡ NEXUS Strategic SEO Intelligence")
    st.markdown("### Move from analysis paralysis to prioritized ROI-driven execution.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070")
    st.info("👋 Log in to access the real-time Strategic Dashboard.")

else:
    # Production State Sync
    profile = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    tier, credits = profile['plan_tier'], profile['credits']
    
    st.sidebar.success(f"Enterprise Tier: {tier}")
    if tier != "Agency":
        st.sidebar.link_button("🚀 Upgrade to Agency (€199)", "https://buy.stripe.com/agency_link")

    st.title("⚡ Enterprise Strategy Engine")
    target = st.text_input("Global URL Analysis:", placeholder="https://corporate-site.com")
    
    if st.button("🚀 EXECUTE STRATEGIC ANALYSIS") and target:
        if tier == "Demo" and credits <= 0:
            st.error("License Quota Exhausted. Please upgrade.")
        else:
            full_report = execute_strategic_audit(target, tier)
            
            # Extract JSON for Real-time Charts
            try:
                json_match = re.search(r'\{.*\}', full_report, re.DOTALL)
                viz_data = json.loads(json_match.group())
                render_live_analytics(viz_data['score'], viz_data['priorities'])
            except: st.warning("Visual Data processing incomplete. Reviewing text strategy.")
            
            st.markdown("---")
            st.markdown(re.sub(r'\{.*\}', '', full_report, flags=re.DOTALL))
            
            # Deduct Credits
            if tier == "Demo":
                supabase.table("profiles").update({"credits": credits - 1}).eq("id", st.session_state.user.id).execute()

    if st.sidebar.button("Terminate Session"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
