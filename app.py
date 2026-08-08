import streamlit as st
import os
from database.database import init_db
from modules.candidate_manager import seed_sample_candidates_if_empty
from utils.auth import is_authenticated, logout_user, get_current_user

# Page Configuration
st.set_page_config(
    page_title="Email Automation Portal - Smart Recruitment Communication Management",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Executive SaaS CSS Styling
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header & Branding */
    .sidebar-brand {
        text-align: center;
        padding: 12px 0;
        margin-bottom: 12px;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-title {
        font-size: 22px;
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
        font-size: 26px;
        font-weight: 700;
        color: #1E293B;
    }

    /* General Card Styling */
    .saas-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize Database & Sample Data
init_db()
seed_sample_candidates_if_empty()

# 1. Authentication Check
if not is_authenticated():
    from pages.login import render_login_page
    render_login_page()
else:
    # 2. Main Authenticated Application Sidebar Navigation
    user_info = get_current_user()

    st.sidebar.markdown(f"""
    <div class="sidebar-brand">
        <div class="brand-title">RecruitFlow Portal</div>
        <div class="brand-tagline">Recruitment Automation</div>
        <div style="margin-top: 8px; font-size: 12px; color: #475569; font-weight: 600;">
            👤 {user_info['name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    nav_choice = st.sidebar.radio(
        "Main Navigation",
        [
            "🏠 Dashboard",
            "👥 Candidates",
            "📧 Email Automation",
            "📅 Campaigns & Scheduling",
            "📜 Email History",
            "📄 Documents",
            "📊 Analytics",
            "🔔 Notifications",
            "⚙️ Settings"
        ],
        index=0
    )

    st.sidebar.markdown("---")

    # Logout Action Button in Sidebar
    if st.sidebar.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
        logout_user()
        st.rerun()

    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 11px; color: #94A3B8; margin-top: 20px;">
        Email Automation Portal v2.0<br/>Streamlit Enterprise Edition
    </div>
    """, unsafe_allow_html=True)

    # 3. Page Routing Engine
    if nav_choice == "🏠 Dashboard":
        from pages.dashboard import render_dashboard_page
        render_dashboard_page()

    elif nav_choice == "👥 Candidates":
        from pages.candidates import render_candidates_page
        render_candidates_page()

    elif nav_choice == "📧 Email Automation":
        from pages.email_automation import render_email_automation_page
        render_email_automation_page()

    elif nav_choice == "📅 Campaigns & Scheduling":
        from pages.campaigns import render_campaigns_page
        render_campaigns_page()

    elif nav_choice == "📜 Email History":
        from pages.email_logs import render_email_logs_page
        render_email_logs_page()

    elif nav_choice == "📄 Documents":
        from pages.documents import render_documents_page
        render_documents_page()

    elif nav_choice == "📊 Analytics":
        from pages.analytics import render_analytics_page
        render_analytics_page()

    elif nav_choice == "🔔 Notifications":
        from pages.notifications import render_notifications_page
        render_notifications_page()

    elif nav_choice == "⚙️ Settings":
        from pages.settings import render_settings_page
        render_settings_page()
