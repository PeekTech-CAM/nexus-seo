import streamlit as st
from supabase import create_client, Client
from firecrawl import Firecrawl
from google import genai
from fpdf import FPDF
import plotly.graph_objects as go
import plotly.express as px
import json
import re

# --- 1. SECURE INITIALIZATION (Resolving 405 Error) ---
@st.cache_resource
def init_enterprise_engine():
    try:
        # Use ONLY the API URL from Settings > API
        supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        firecrawl = Firecrawl(api_key=st.secrets["FIRE_KEY"])
        gemini = genai.Client(api_key=st.secrets["GEMINI_KEY"])
        return supabase, firecrawl, gemini
    except Exception as e:
        st.error(f"Initialization Failed. Check API URLs in Secrets. Error: {e}")
        st.stop()

supabase, firecrawl, gemini = init_enterprise_engine()

# --- 2. PROFESSIONAL SAAS TIERS ---
PLANS = {
    "Demo": {"depth": 3000, "label": "Free Demo", "credits": 1, "viz": True},
    "Starter": {"depth": 7000, "label": "Starter (€29)", "credits": 5, "viz": True},
    "Pro": {"depth": 18000, "label": "Pro (€79)", "unlimited": True, "viz": True},
    "Agency": {"depth": 25000, "label": "Agency (€199)", "unlimited": True, "white_label": True, "viz": True}
}

st.set_page_config(page_title="NEXUS Pro | Enterprise SEO Intelligence", layout="wide")

# --- 3. DATA VISUALIZATION ENGINE (Live Analysis Charts) ---
def render_analysis_charts(score, priorities):
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge Chart for Strategic Health
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "Strategic Health Score"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ff4b4b"},
                'steps': [
                    {'range': [0, 50], 'color': "#333"},
                    {'range': [50, 80], 'color': "#666"}]}))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Priority Distribution Chart
        labels = list(priorities.keys())
        values = list(priorities.values())
        fig_pie = px.pie(names=labels, values=values, title="Action Priority Distribution",
                         color_discrete_sequence=["#ff4b4b", "#888", "#333"])
        st.plotly_chart(fig_pie, use_container_width=True)

# --- 4. THE PRIORITIZATION ENGINE (JSON Output for Charts) ---
def execute_deep_audit(url, lang, tier):
    config = PLANS[tier]
    with st.status("⚡ Executing Multi-Vector Analysis...") as status:
        scrape = firecrawl.scrape(url)
        raw_data = scrape.markdown if hasattr(scrape, 'markdown') else str(scrape)
        
        # Enterprise Prompt: Requests JSON for real-time charting
        prompt = f"""
        Analyze {url} in {lang}. Role: SEO Director.
        Tier: {tier}.
        
        YOU MUST RETURN A JSON BLOCK FIRST, then the report.
        JSON Format:
        {{
          "score": 85,
          "priorities": {{"High": 5, "Medium": 3, "Low": 8}}
        }}
        
        Report Structure: [ROI Summary], [Technical RoadMap], [Competitor Gap].
        Content: {raw_data[:config['depth']]}
        """
        
        res = gemini.models.generate_content(model="gemini-2.0-flash-exp", contents=prompt)
        return res.text

# --- 5. AUTHENTICATION & PROFILE SYNC ---
def auth_portal():
    st.sidebar.title("🔐 NEXUS Enterprise Access")
    mode = st.sidebar.selectbox("Access Mode", ["Authorize Account", "Register Organization"])
    email = st.sidebar.text_input("Corporate ID")
    pwd = st.sidebar.text_input("Access Key", type="password")

    if mode == "Register Organization":
        if st.sidebar.button("Establish Profile"):
            try:
                supabase.auth.sign_up({"email": email, "password": pwd})
                st.sidebar.success("Registration Initialized. Check Email.")
            except: st.sidebar.error("Network Error. Check Supabase URL.")
    else:
        if st.sidebar.button("Authenticate"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
                st.session_state.user = res.user
                st.rerun()
            except: st.sidebar.error("Authorization Denied.")

# --- 6. MAIN ENTERPRISE INTERFACE ---
if "user" not in st.session_state:
    auth_portal()
    st.title("⚡ NEXUS Strategic Intelligence")
    st.markdown("### Professional-grade SEO audits with real-time data visualization.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=2070")
else:
    # Production Data Sync
    profile = supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute().data
    tier, credits = profile['plan_tier'], profile['credits']
    
    st.sidebar.success(f"Tier: {tier}")
    if not PLANS[tier].get("unlimited"):
        st.sidebar.metric("Quota Remaining", f"{credits} Audits")
        st.sidebar.link_button("🚀 Upgrade License", "https://buy.stripe.com/pro_link")

    st.title("⚡ Enterprise Strategy Dashboard")
    target = st.text_input("Global URL Analysis:", placeholder="https://corporate-site.com")
    
    if st.button("🚀 EXECUTE STRATEGIC ANALYSIS") and target:
        if not PLANS[tier].get("unlimited") and credits <= 0:
            st.error("License Quota Exhausted.")
        else:
            full_res = execute_deep_audit(target, "English", tier)
            
            # Extract JSON for Real-time Charts
            try:
                json_match = re.search(r'\{.*\}', full_res, re.DOTALL)
                data_viz = json.loads(json_match.group())
                render_analysis_charts(data_viz['score'], data_viz['priorities'])
            except: st.warning("Visual Data processing incomplete. Reviewing text strategy.")
            
            st.markdown(re.sub(r'\{.*\}', '', full_res, flags=re.DOTALL))
            
            # Credit Logic
            if not PLANS[tier].get("unlimited"):
                supabase.table("profiles").update({"credits": credits - 1}).eq("id", st.session_state.user.id).execute()

    if st.sidebar.button("Terminate Session"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
