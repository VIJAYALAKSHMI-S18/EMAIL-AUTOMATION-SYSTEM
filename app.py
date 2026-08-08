import streamlit as st
import os
from database.database import init_db
from modules.candidate_manager import seed_sample_candidates_if_empty

# Page Configuration
st.set_page_config(
    page_title="RecruitFlow – Recruitment Email Automation System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Executive CSS Styling
CUSTOM_CSS = """
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header Container */
    .header-banner {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .header-title {
        font-size: 32px;
        font-weight: 700;
        margin: 0;
        color: #FFFFFF;
        letter-spacing: -0.5px;
    }
    .header-tagline {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }
    
    /* Sidebar Branding */
    .sidebar-brand {
        text-align: center;
        padding: 12px 0;
        margin-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-title {
        font-size: 24px;
        font-weight: 800;
        color: #2563EB;
        margin: 0;
    }
    .brand-tagline {
        font-size: 11px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Metric Cards Customization */
    [data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #1E293B;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize SQLite Database & Sample Data
init_db()
seed_sample_candidates_if_empty()

# Sidebar Navigation Header
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="brand-title">RecruitFlow</div>
    <div class="brand-tagline">Automate. Personalize. Communicate.</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation Pages
page_choice = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Dashboard",
        "👥 Candidates",
        "📊 Analytics",
        "📄 Documents",
        "📧 Email Automation",
        "📜 Email Logs",
        "⚙️ Settings"
    ],
    index=0
)

# Footer Info in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
**RecruitFlow v1.0**  
Recruitment Automation System  
Built with Streamlit & Python
""")

# Page Routing Engine
if page_choice == "🏠 Dashboard":
    from pages.dashboard import render_dashboard_page
    render_dashboard_page()

elif page_choice == "👥 Candidates":
    from pages.candidates import render_candidates_page
    render_candidates_page()

elif page_choice == "📊 Analytics":
    from pages.analytics import render_analytics_page
    render_analytics_page()

elif page_choice == "📄 Documents":
    from pages.documents import render_documents_page
    render_documents_page()

elif page_choice == "📧 Email Automation":
    from pages.email_automation import render_email_automation_page
    render_email_automation_page()

elif page_choice == "📜 Email Logs":
    from pages.email_logs import render_email_logs_page
    render_email_logs_page()

elif page_choice == "⚙️ Settings":
    from pages.settings import render_settings_page
    render_settings_page()
