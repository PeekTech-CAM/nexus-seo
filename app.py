import streamlit as st
from supabase import create_client
import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components
import json

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(
    page_title="NEXUS SEO Intelligence",
    page_icon="🚀",
    layout="wide"
)

# =============================================================================
# CONSTANTS
# =============================================================================
ADMIN_EMAIL = "3dpeektech@gmail.com"
STRIPE_PAYMENT_LINK_STARTER = "https://buy.stripe.com/your-link"
STRIPE_CUSTOMER_PORTAL = "https://billing.stripe.com/p/login/your-link"
GTM_ID = "GTM-KXF6VCFJ"

# =============================================================================
# GOOGLE TAG MANAGER
# =============================================================================
def inject_gtm():
    components.html(f"""
    <script>
    (function(w,d,s,l,i){{
    w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});
    var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';
    j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;
    f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','{GTM_ID}');
    </script>
    """, height=0)

# =============================================================================
# CORE ENGINE
# =============================================================================
class NexusEliteEngine:
    def __init__(self):
        self.supabase = self._init_supabase()
        self.ai = self._init_ai()

    def _init_supabase(self):
        try:
            return create_client(
                st.secrets["SUPABASE_URL"],
                st.secrets["SUPABASE_KEY"]
            )
        except:
            return None

    def _init_ai(self):
        try:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            return genai.GenerativeModel("gemini-1.5-flash")
        except:
            return None

    def scrape(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        return {
            "url": url,
            "load_time": r.elapsed.total_seconds(),
            "title": soup.title.text if soup.title else "",
            "meta_description": soup.find("meta", {"name": "description"})["content"]
                if soup.find("meta", {"name": "description"}) else "",
            "h1": len(soup.find_all("h1")),
            "h2": len(soup.find_all("h2")),
            "images": len(soup.find_all("img")),
            "images_no_alt": len([i for i in soup.find_all("img") if not i.get("alt")]),
            "words": len(text.split()),
            "sample": text[:3000]
        }

    def seo_score(self, d):
        score = 100
        issues = []

        if not d["title"]:
            score -= 15; issues.append("❌ Missing title")
        if not d["meta_description"]:
            score -= 10; issues.append("❌ Missing meta description")
        if d["h1"] == 0:
            score -= 15; issues.append("❌ No H1")
        if d["words"] < 300:
            score -= 15; issues.append("❌ Thin content")
        if d["images_no_alt"] > 0:
            score -= 10; issues.append("⚠️ Images without ALT")
        if d["load_time"] > 3:
            score -= 10; issues.append("❌ Slow load")

        return max(0, score), issues

    def ai_analysis(self, d):
        if not self.ai:
            return "AI unavailable"
        prompt = f"""
SEO audit:
Title: {d['title']}
Words: {d['words']}
Load: {d['load_time']}
Issues: {d['images_no_alt']} images missing alt

Give improvements + 30-day SEO plan + ROI
"""
        return self.ai.generate_content(prompt).text

nexus = NexusEliteEngine()

# =============================================================================
# SESSION
# =============================================================================
for k in ["auth", "user", "profile"]:
    if k not in st.session_state:
        st.session_state[k] = None

# =============================================================================
# AUTH
# =============================================================================
def login(email, pwd):
    r = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
    st.session_state.user = r.user
    st.session_state.profile = nexus.supabase.table("profiles").select("*").eq("id", r.user.id).single().execute().data
    st.session_state.auth = True

def register(email, pwd):
    r = nexus.supabase.auth.sign_up({"email": email, "password": pwd})
    nexus.supabase.table("profiles").insert({
        "id": r.user.id,
        "email": email,
        "plan_tier": "Demo",
        "credits": 1
    }).execute()
    login(email, pwd)

# =============================================================================
# UI PAGES
# =============================================================================
def landing():
    st.markdown("# 🚀 NEXUS SEO")
    t1, t2 = st.tabs(["Login", "Free Trial"])

    with t1:
        e = st.text_input("Email")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            login(e, p)
            st.rerun()

    with t2:
        e = st.text_input("Email", key="r1")
        p = st.text_input("Password", type="password", key="r2")
        if st.button("Start Free"):
            register(e, p)
            st.rerun()

def demo():
    st.sidebar.metric("Credits", st.session_state.profile["credits"])
    url = st.text_input("Website URL")
    if st.button("Run Demo Scan"):
        d = nexus.scrape(url)
        s, i = nexus.seo_score(d)
        st.metric("SEO Score", s)
        for x in i: st.write(x)

def client():
    url = st.text_input("Website")
    if st.button("Deep Scan"):
        d = nexus.scrape(url)
        s, i = nexus.seo_score(d)
        ai = nexus.ai_analysis(d)

        st.metric("SEO Score", s)
        st.write(i)
        st.markdown("### AI Report")
        st.write(ai)

def admin():
    st.markdown("## Admin Panel")
    df = pd.DataFrame(nexus.supabase.table("profiles").select("*").execute().data)
    st.dataframe(df)

# =============================================================================
# MAIN ROUTER
# =============================================================================
def main():
    inject_gtm()

    if not st.session_state.auth:
        landing()
        return

    profile = st.session_state.profile
    email = profile["email"]
    plan = profile["plan_tier"]

    if email == ADMIN_EMAIL:
        t1, t2 = st.tabs(["App", "Admin"])
        with t1:
            demo() if plan == "Demo" else client()
        with t2:
            admin()
    else:
        demo() if plan == "Demo" else client()

# =============================================================================
# ENTRY
# =============================================================================
if __name__ == "__main__":
    main()
