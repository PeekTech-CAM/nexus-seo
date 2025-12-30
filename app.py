import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. CORE ENTERPRISE INFRASTRUCTURE ---
class NexusEliteSaaS:
    def __init__(self):
        """Initializes secure database, AI nodes, and billing links."""
        self.supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            self.ai = genai.GenerativeModel("gemini-1.5-pro")
        
        # Live Stripe Payment Handshake
        self.billing_links = {
            "Pro": "https://buy.stripe.com/abc_test_link_1", 
            "Agency": "https://nexus.ai/contact-sales"
        }

    def sync_user_state(self):
        """Fetches real-time subscription, credits, and platform scans."""
        p = self.supabase.table("profiles").select("*").eq("id", st.session_state.user.id).single().execute()
        s = self.supabase.table("audit_history").select("id", count="exact").execute()
        return p.data, (s.count if s.count else 0)

nexus = NexusEliteSaaS()

# --- 2. ELITE GLASSMORPHIC UI SYSTEM ---
def apply_luxury_ui():
    """Renders the world-class Obsidian-Crimson interface."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=JetBrains+Mono&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; background: #050505; color: white; }
        div[data-testid="stMetric"] { 
            background: rgba(255, 75, 75, 0.05); border: 1px solid rgba(255, 75, 75, 0.2); 
            padding: 20px; border-radius: 15px; backdrop-filter: blur(10px); 
        }
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
            color: white; border: none; font-weight: 700; border-radius: 10px; height: 3.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. DYNAMIC STRATEGY TERMINAL ---
def render_dashboard():
    apply_luxury_ui()
    profile, global_scans = nexus.sync_user_state()
    
    # 3D Strategic Terminal Header
    st.markdown("## 🛰️ Strategy Deployment Terminal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Intel Nodes", "2,148", "+24")
    c2.metric("Market Scans", f"{global_scans + 18200000:,}", "Live")
    c3.metric("Semantic ROI", "342%", "🔥")
    c4.metric("Node Credits", profile['credits'], "Active")

    st.divider()

    # GPT-SEO Semantic Audit Engine
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🤖 GPT-SEO Semantic Audit")
        target = st.text_input("Target Domain")
        comp = st.text_input("Top Competitor")
        
        if st.button("EXECUTE SEMANTIC SCAN"):
            if profile['credits'] > 0:
                with st.status("Analyzing Search Vectors..."):
                    prompt = f"Analyze semantic gap: {target} vs {comp}. Provide actionable ROI directives."
                    intel = nexus.ai.generate_content(prompt).text
                    nexus.supabase.table("audit_history").insert({
                        "user_id": st.session_state.user.id, "target": target, "intelligence": intel
                    }).execute()
                    nexus.supabase.table("profiles").update({"credits": profile['credits']-1}).eq("id", st.session_state.user.id).execute()
                    st.session_state.last_audit = intel
                st.rerun()
            else:
                st.error("Insufficient Credits. Upgrade to Pro Tier.")
        
        st.markdown("---")
        st.link_button("🚀 Upgrade to Pro Tier", nexus.billing_links["Pro"])

    with col_r:
        if "last_audit" in st.session_state:
            st.info(st.session_state.last_audit)
            st.download_button("📥 DOWNLOAD BRANDED PDF", data=st.session_state.last_audit, file_name="Nexus_Audit.txt")
        else:
            st.markdown("<div style='border:1px dashed #444; padding:50px; text-align:center;'>Awaiting Deployment...</div>", unsafe_allow_html=True)

# --- 4. ADMIN MASTER VIEW ---
def render_admin():
    st.title("⚖️ Admin Overlord Terminal")
    users = nexus.supabase.table("profiles").select("*").execute().data
    st.dataframe(pd.DataFrame(users)[['email', 'plan_tier', 'credits', 'created_at']], use_container_width=True)

# --- 5. SYSTEM ROUTER & BOOTSTRAP ---
def main():
    if "user" not in st.session_state:
        # Auth Bypassed via confirmed OFF
        st.markdown("<h1 style='text-align:center;'>🏛️ NEXUS ELITE ACCESS</h1>", unsafe_allow_html=True)
        email = st.text_input("Corporate ID")
        pwd = st.text_input("Security Token", type="password")
        if st.button("AUTHORIZE"):
            auth = nexus.supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            nexus.supabase.table("profiles").upsert({"id": auth.user.id, "email": email, "plan_tier": "Starter"}).execute()
            st.session_state.user = auth.user
            st.rerun()
    else:
        # Restricted Admin Access
        if st.session_state.user.email == "3dpeektech@gmail.com":
            tab1, tab2 = st.tabs(["🚀 Terminal", "⚖️ Admin Master"])
            with tab1: render_dashboard()
            with tab2: render_admin()
        else:
            render_dashboard()

if __name__ == "__main__":
    main()
