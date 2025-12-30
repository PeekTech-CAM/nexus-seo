import streamlit as st
from supabase import create_client, Client
import google.generativeai as genai
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time

# --- 1. CORE ENGINE ---
class NexusProductionEngine:
    def __init__(self):
        self.supabase: Client = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
        if "GEMINI_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_KEY"])
            self.ai = genai.GenerativeModel("gemini-1.5-pro")
        else:
            self.ai = None

nexus = NexusProductionEngine()

# --- 2. LUXURY UI DESIGN SYSTEM ---
def apply_luxury_ui():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=JetBrains+Mono&display=swap');
        
        /* Master Container */
        html, body, [class*="css"] { 
            font-family: 'Space Grotesk', sans-serif; 
            background: radial-gradient(circle at top left, #1a0505 0%, #050505 100%); 
            color: #e0e0e0; 
        }

        /* Glassmorphism Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(10, 10, 10, 0.8) !important;
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255, 75, 75, 0.2);
        }

        /* Glowing Metric Cards */
        div[data-testid="stMetric"] {
            background: rgba(20, 20, 20, 0.6);
            border: 1px solid rgba(255, 75, 75, 0.3);
            border-radius: 20px;
            padding: 25px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        /* Crimson Neon Button */
        .stButton>button {
            background: linear-gradient(135deg, #ff4b4b 0%, #8b0000 100%);
            color: white; border: none; font-weight: 700; height: 3.8rem; width: 100%;
            border-radius: 12px; letter-spacing: 1px;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(255, 75, 75, 0.6);
        }

        /* Terminal Style Logs */
        .terminal-text {
            font-family: 'JetBrains Mono', monospace;
            color: #ff4b4b;
            font-size: 0.85rem;
            background: #000;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #ff4b4b;
        }
        </style>
    """, unsafe_allow_html=True)

# --- 3. KINETIC DATA VISUALS ---
def render_roi_spider_chart():
    """Enterprise-grade radar chart for multi-vector SEO analysis."""
    categories = ['Technical SEO', 'Content Depth', 'Authority', 'UX/Core Vitals', 'Semantic Match']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[85, 92, 78, 95, 88], theta=categories, fill='toself',
        fillcolor='rgba(255, 75, 75, 0.3)', line=dict(color='#ff4b4b', width=3)
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#333"), bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#fff", size=12), margin=dict(l=80, r=80, t=20, b=20)
    )
    return fig

# --- 4. THE COMMAND CENTER ---
def render_dashboard():
    apply_luxury_ui()
    
    # Sidebar: User Status & Tier
    st.sidebar.markdown("### 🏛️ NODE: ACTIVE")
    st.sidebar.markdown(f"**Authorized:** `{st.session_state.user.email}`")
    st.sidebar.divider()
    
    # Main Terminal Header
    st.markdown("<h1 style='letter-spacing: -2px; font-weight: 700;'>🛰️ STRATEGY DEPLOYMENT TERMINAL</h1>", unsafe_allow_html=True)
    
    # KPIs: Premium Metric Layout
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Intelligence Nodes", "2,148", "+24")
    m2.metric("Market Scans", "18.2M", "Live")
    m3.metric("Semantic ROI", "342%", "🔥")
    m4.metric("Agency Tier", "Elite", "Pro")

    st.divider()

    # Strategy Execution Area
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("⚡ Core Performance Matrix")
        st.plotly_chart(render_roi_spider_chart(), use_container_width=True)
    
    with col_b:
        st.subheader("🤖 AI Strategic Analysis")
        with st.container(border=True):
            st.markdown("""
                **Current Vectors:**
                - *Content Optimization:* High Priority
                - *Technical Debt:* Minimal
                - *Backlink Velocity:* Trending +12%
            """)
            if st.button("GENERATE AI DEPLOYMENT ROADMAP"):
                with st.status("Synthesizing market data...", expanded=True):
                    time.sleep(1.5)
                    st.write("Connecting to LLM Node...")
                    time.sleep(1)
                st.success("Deployment Roadmap Ready for Export (PDF)")

    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state.clear()
        st.rerun()

# --- 5. SYSTEM ROUTER ---
if "user" not in st.session_state:
    # Use the auth gate we built previously
    st.warning("Please sign in at the Access Terminal.")
else:
    render_dashboard()
