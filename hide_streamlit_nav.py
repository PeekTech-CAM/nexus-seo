"""
CSS to hide Streamlit's default navigation and enhance custom sidebar
Add this to your app.py and all page files
"""

import streamlit as st

def hide_streamlit_navigation():
    """
    Hide Streamlit's default page navigation sidebar.
    Call this in app.py and at the top of every page.
    """
    st.markdown("""
    <style>
        /* Hide Streamlit's default navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Hide the default page list */
        section[data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Alternative selector for newer Streamlit versions */
        .css-1544g2n {
            display: none;
        }
        
        /* Hide hamburger menu on mobile */
        button[kind="header"] {
            display: none;
        }
        
        /* Improve sidebar appearance */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        }
        
        /* Better spacing for sidebar content */
        .css-1d391kg, .css-1lcbmhc {
            padding-top: 1rem;
        }
        
        /* Style custom sidebar buttons */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        /* Hover effect for sidebar buttons */
        .stButton > button:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# ALTERNATIVE: Complete CSS Enhancement Package
# ============================================================================

def apply_custom_styling():
    """
    Complete custom styling including navigation hiding and UI improvements.
    Call this once in app.py
    """
    st.markdown("""
    <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* ============================================
           HIDE STREAMLIT DEFAULT NAVIGATION
           ============================================ */
        
        /* Main navigation container */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Navigation list */
        section[data-testid="stSidebarNav"] > ul {
            display: none !important;
        }
        
        /* Alternative selectors for different Streamlit versions */
        .css-1544g2n,
        .css-17lntkn,
        nav[aria-label="Pages"] {
            display: none !important;
        }
        
        /* Hide deploy button if you don't want it */
        .css-1rs6os {
            display: none;
        }
        
        /* ============================================
           SIDEBAR ENHANCEMENTS
           ============================================ */
        
        /* Sidebar background gradient */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
            box-shadow: 2px 0 10px rgba(0,0,0,0.05);
        }
        
        /* Sidebar content padding */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 2rem;
        }
        
        /* ============================================
           CUSTOM BUTTON STYLING
           ============================================ */
        
        /* All buttons */
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            border: none;
        }
        
        /* Primary buttons (type="primary") */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Primary button hover */
        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Secondary buttons */
        .stButton > button[kind="secondary"] {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        /* Secondary button hover */
        .stButton > button[kind="secondary"]:hover {
            background: rgba(102, 126, 234, 0.2);
            transform: translateX(5px);
        }
        
        /* ============================================
           SECTION HEADERS IN SIDEBAR
           ============================================ */
        
        /* Section headers styling */
        [data-testid="stSidebar"] h3 {
            color: #333;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            padding-left: 0.5rem;
            border-left: 3px solid #667eea;
        }
        
        /* ============================================
           HERO SECTION
           ============================================ */
        
        .hero-section {
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 3rem;
            border-radius: 20px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* ============================================
           METRICS & CARDS
           ============================================ */
        
        /* Metric containers */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        
        /* ============================================
           MOBILE RESPONSIVENESS
           ============================================ */
        
        @media (max-width: 768px) {
            /* Adjust hero on mobile */
            .hero-section {
                padding: 2rem;
            }
            
            /* Adjust sidebar on mobile */
            [data-testid="stSidebar"] {
                box-shadow: none;
            }
        }
        
        /* ============================================
           SCROLL IMPROVEMENTS
           ============================================ */
        
        /* Custom scrollbar for sidebar */
        [data-testid="stSidebar"] ::-webkit-scrollbar {
            width: 6px;
        }
        
        [data-testid="stSidebar"] ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* ============================================
           HIDE UNNECESSARY ELEMENTS
           ============================================ */
        
        /* Hide "Made with Streamlit" footer (optional) */
        footer {
            visibility: hidden;
        }
        
        /* Hide hamburger menu icon on desktop */
        button[kind="header"] {
            display: none;
        }
        
        /* ============================================
           LOADING STATES
           ============================================ */
        
        /* Spinner color */
        .stSpinner > div {
            border-top-color: #667eea !important;
        }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# USAGE IN app.py
# ============================================================================

"""
# At the top of app.py, after imports:

import streamlit as st

st.set_page_config(
    page_title="Nexus SEO Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ADD THIS LINE - Hides default navigation
from hide_streamlit_nav import apply_custom_styling
apply_custom_styling()

# Or just use the function directly:
hide_streamlit_navigation()

# Rest of your app code...
"""


# ============================================================================
# USAGE IN PAGE FILES (e.g., Advanced_Scanner.py)
# ============================================================================

"""
# At the top of each page file:

import streamlit as st

st.set_page_config(
    page_title="Advanced Scanner",
    page_icon="🔍",
    layout="wide"
)

# ADD THIS
from hide_streamlit_nav import hide_streamlit_navigation
hide_streamlit_navigation()

# Or import and call the full styling:
from hide_streamlit_nav import apply_custom_styling
apply_custom_styling()

# Your page code continues...
"""


# ============================================================================
# ALTERNATIVE: Inline CSS (No separate file needed)
# ============================================================================

def hide_nav_inline():
    """
    Simple inline version - copy this into app.py directly.
    No separate file needed.
    """
    st.markdown("""
    <style>
        /* Hide Streamlit navigation */
        [data-testid="stSidebarNav"] {display: none !important;}
        section[data-testid="stSidebarNav"] {display: none !important;}
        .css-1544g2n {display: none !important;}
        nav[aria-label="Pages"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# TESTING - Verify Navigation is Hidden
# ============================================================================

def verify_navigation_hidden():
    """
    Add this temporarily to check if it worked.
    You should NOT see the default Streamlit page list.
    """
    with st.sidebar:
        st.success("✅ Custom sidebar visible")
        st.info("ℹ️ If you see a list of pages above this, the CSS didn't work")
        
        # Show what should be hidden
        st.markdown("---")
        st.caption("Default navigation should be hidden ↑")