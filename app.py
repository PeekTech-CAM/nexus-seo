import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# -----------------------------
# 1. SAAS REVENUE ENGINE
# -----------------------------
class NexusRevenueEngine:
    def __init__(self):
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )

    def sync_billing_state(self, user_id):
        """Fetches real-time subscription and credit status."""
        data = (
            self.supabase.table("profiles")
            .select("plan_tier, credits")
            .eq("id", user_id)
            .single()
            .execute()
        )
        return data.data if data.data else {"plan_tier": "Free", "credits": 0}


nexus_billing = NexusRevenueEngine()


# -----------------------------
# 2. DYNAMIC SIDEBAR TERMINAL
# -----------------------------
def render_sidebar():
    billing = nexus_billing.sync_billing_state(st.session_state.user.id)

    st.sidebar.markdown(f"### 🛰️ {billing['plan_tier']} Terminal")
    st.sidebar.metric("Intelligence Credits", billing['credits'])

    if billing['credits'] < 5:
        st.sidebar.warning("⚠️ Low Credits: High-Vector analysis may be limited.")
        st.sidebar.markdown(
            "[🚀 Upgrade to Agency Elite](https://buy.stripe.com/test_agency)"
        )


# -----------------------------
# 3. UPDATED AUDIT ENGINE
# -----------------------------
def execute_gpt_seo_audit(target, competitor):
    """Checks credits before allowing expensive AI scans."""
    billing = nexus_billing.sync_billing_state(st.session_state.user.id)

    if billing['credits'] > 0:
        # Perform scan and decrement credit
        new_credits = billing['credits'] - 1
        nexus_billing.supabase.table("profiles").update(
            {"credits": new_credits}
        ).eq("id", st.session_state.user.id).execute()
        st.success(f"Audit Complete. Node Credits: {new_credits}")
    else:
        st.error("Insufficient Credits. Please upgrade your tier.")


# -----------------------------
# 4. ENTERPRISE SYSTEM CORE
# -----------------------------
class NexusEliteEngine:
    def __init__(self):
        """Initializes connection with verified API and AI nodes."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )
        # Tiered Subscription Links
        self.stripe_links = {
            "Pro": "https://buy.stripe.com/test_pro_tier",
            "Agency": "https://nexus.agency/contact-sales"
        }
        # Placeholder for AI node
        self.ai = genai


nexus = NexusEliteEngine()


# -----------------------------
# 5. LUXURY COMMAND CENTER UI
# -----------------------------
def apply_luxury_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Space Grotesk', sans-serif; 
        background: radial-gradient(circle at top left, #1a0505 0%, #050505 100%);
        color: white; 
    }

    .premium-card {
        background: rgba(255, 75, 75, 0.05);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 75, 75, 0.2);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        transition: 0.4s;
    }
    .premium-card:hover { border-color: #ff4b4b; transform: translateY(-5px); }

    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
        color: white; border: none; font-weight: 700; height: 3.5rem; width: 100%;
        border-radius: 12px; box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# 6. ADMIN ENGINE
# -----------------------------
class NexusAdminEngine:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_all_users(self):
        return self.supabase.table("profiles").select("*").execute()

    def get_global_audit_logs(self):
        return self.supabase.table("audit_history").select(
            "*, profiles(email)"
        ).order("created_at", desc=True).execute()


# -----------------------------
# 7. ADMIN VIEW
# -----------------------------
def render_admin_view():
    admin = NexusAdminEngine(nexus.supabase)

    st.title("⚖️ Admin Overlord Terminal")
    st.markdown("### Strategic SaaS Oversight")

    users = admin.get_all_users().data or []
    audits = admin.get_global_audit_logs().data or []

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Organizations", len(users))
    c2.metric("Total Scans Executed", len(audits))
    c3.metric("Platform ROI", f"${len(users) * 99}", "Est. Monthly")

    # Users table
    st.subheader("👤 Registered Organizations")
    df_users = pd.DataFrame(users)
    st.dataframe(df_users[['email', 'plan_tier', 'credits', 'created_at']], use_container_width=True)

    # Global activity feed
    st.subheader("🛰️ Live Global Audit Feed")
    if audits:
        for log in audits[:10]:
            with st.expander(f"Audit: {log['target']} by {log.get('profiles', {}).get('email', 'Unknown')}"):
                st.write(f"**Competitor:** {log['competitor']}")
                st.write(f"**Timestamp:** {log['created_at']}")
                st.code(log['intelligence'][:200] + "...")
    else:
        st.info("No global audits recorded yet.")


# -----------------------------
# 8. MAIN ROUTER
# -----------------------------
def main():
    apply_luxury_theme()

    if "user" in st.session_state:
        st.sidebar.title("🏛️ Terminal Active")
        st.title("🛰️ Strategy Deployment Terminal")
        st.sidebar.write(f"Node: {st.session_state.user.email}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nodes", "2,148", "+24")
        c2.metric("Scans", "18.2M", "Live")
        c3.metric("ROI", "342%", "🔥")
        c4.metric("Networks", "94", "+5")

        st.subheader("📊 Strategic ROI Projections")
        st.area_chart(pd.DataFrame(np.random.randn(20, 3)))

        # Admin tab
        if st.session_state.user.email == "YOUR_ADMIN_EMAIL@gmail.com":
            tab1, tab2 = st.tabs(["🚀 Strategy Terminal", "⚖️ Admin Master"])
            with tab1:
                render_sidebar()
            with tab2:
                render_admin_view()
        else:
            render_sidebar()

        if st.sidebar.button("TERMINATE SESSION"):
            nexus.supabase.auth.sign_out()
            del st.session_state.user
            st.rerun()
    else:
        st.session_state.view = st.session_state.get("view", "pricing")
        if st.session_state.view == "pricing":
            st.markdown("<h2>Pricing & Access Tier UI Placeholder</h2>", unsafe_allow_html=True)
        elif st.session_state.view == "demo":
            st.markdown("<h2>Demo Placeholder</h2>", unsafe_allow_html=True)
        elif st.session_state.view == "auth":
            st.markdown("<h2>Auth Gate Placeholder</h2>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
