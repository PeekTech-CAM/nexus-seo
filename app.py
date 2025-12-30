import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import pandas as pd
import numpy as np
import time

# -----------------------------
# 1. CORE SYSTEM ENGINE
# -----------------------------
class NexusSaaSCommand:
    def __init__(self):
        """Connected to verified Supabase Project."""
        self.supabase: Client = create_client(
            st.secrets["SUPABASE_URL"], 
            st.secrets["SUPABASE_KEY"]
        )

        # Configure Gemini AI if key exists
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            self.ai = genai.GenerativeModel("gemini-1.5-pro")

        # Stripe links for upgrades
        self.stripe_links = {
            "Pro": "https://buy.stripe.com/YOUR_LIVE_LINK",
            "Agency": "https://nexus.agency/contact-sales"
        }

    def sync_metrics(self):
        """Fetches live scan counts for the terminal."""
        res = self.supabase.table("audit_history").select("id", count="exact").execute()
        return res.count or 0


nexus = NexusSaaSCommand()


# -----------------------------
# 2. ELITE GLASSMORPHIC UI
# -----------------------------
def apply_elite_ui():
    """Applies premium crimson-dark theme."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=JetBrains+Mono&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Space Grotesk', sans-serif; 
        background: radial-gradient(circle at top, #1a0505 0%, #050505 100%); 
        color: white; 
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 75, 75, 0.05);
        border: 1px solid rgba(255, 75, 75, 0.2);
        padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
        color: white; border: none; font-weight: 700; border-radius: 10px;
        height: 3rem; width: 100%; transition: 0.3s ease;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4); }
    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# 3. INTERNAL DASHBOARD
# -----------------------------
def render_dashboard():
    apply_elite_ui()
    live_count = nexus.sync_metrics()

    st.markdown("## 🛰️ Strategy Deployment Terminal")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nodes", "2,148", "+24")
    c2.metric("Scans", f"{live_count + 18_200_000:,}", "Live")
    c3.metric("ROI", "342%", "🔥")
    c4.metric("Networks", "94", "+5")

    st.divider()

    # GPT-SEO Audit
    col_l, col_r = st.columns([1, 1.2])
    with col_l:
        st.subheader("🤖 GPT-SEO Audit")
        target = st.text_input("Target Domain", placeholder="example.com")
        competitor = st.text_input("Competitor", placeholder="competitor.com")

        if st.button("EXECUTE SEMANTIC SCAN"):
            if target and competitor:
                with st.spinner("Analyzing semantic vectors..."):
                    prompt = f"Perform an expert SEO audit for {target} vs {competitor}. Identify semantic gaps."
                    intel = nexus.ai.generate_content(prompt).text
                    nexus.supabase.table("audit_history").insert({
                        "user_id": st.session_state.user.id,
                        "target": target,
                        "competitor": competitor,
                        "intelligence": intel
                    }).execute()
                    st.session_state.current_audit = intel
                st.success("Audit Complete!")
            else:
                st.warning("Please provide both Target and Competitor domains.")

        st.markdown("---")
        st.markdown(f"[🚀 Upgrade to Pro Tier]({nexus.stripe_links['Pro']})")

    with col_r:
        if "current_audit" in st.session_state:
            st.info(st.session_state.current_audit)
            st.download_button(
                "📥 DOWNLOAD BRANDED PDF",
                data=st.session_state.current_audit,
                file_name="Nexus_Audit.txt"
            )
        else:
            st.markdown(
                "<div style='border:1px dashed #444; padding:40px; text-align:center; border-radius:10px; color:#888;'>Awaiting Audit Initialization...</div>",
                unsafe_allow_html=True
            )


# -----------------------------
# 4. ADMIN MASTER VIEW
# -----------------------------
def render_admin_view():
    st.title("⚖️ Admin Overlord Terminal")
    users = nexus.supabase.table("profiles").select("*").execute().data
    st.subheader("👤 Registered Organizations")
    if users:
        df_users = pd.DataFrame(users)
        st.dataframe(df_users[['email', 'plan_tier', 'created_at']], use_container_width=True)
    else:
        st.info("No organizations registered yet.")


# -----------------------------
# 5. SYSTEM ROUTER
# -----------------------------
def main():
    if "user" not in st.session_state:
        st.warning("Authorize terminal access to begin.")
    else:
        if st.session_state.user.email == "3dpeektech@gmail.com":
            tab1, tab2 = st.tabs(["🚀 Terminal", "⚖️ Admin Master"])
            with tab1:
                render_dashboard()
            with tab2:
                render_admin_view()
        else:
            render_dashboard()


if __name__ == "__main__":
    main()
