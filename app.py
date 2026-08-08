import streamlit as st
import os
from database.database import init_db
from modules.candidate_manager import seed_sample_candidates_if_empty
from utils.auth import is_authenticated, logout_user, get_current_user
from utils.theme import get_current_theme, toggle_theme, get_theme_css

# Page Configuration
st.set_page_config(
    page_title="RecruitFlow Enterprise Portal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Initialize Database & Sample Data
init_db()
seed_sample_candidates_if_empty()

# 2. Inject Dynamic Theme CSS & Custom Cursor
active_theme = get_current_theme()
theme_css = get_theme_css(active_theme)
st.markdown(theme_css, unsafe_allow_html=True)

# 3. Authentication Check
if not is_authenticated():
    from pages.login import render_login_page
    render_login_page()
else:
    # Authenticated Main Portal Layout
    user_info = get_current_user()

    # Sidebar Header & Theme Toggle Switcher
    st.sidebar.markdown(f"""
    <div class="sidebar-brand">
        <div class="brand-title">RecruitFlow</div>
        <div class="brand-tagline">Enterprise HR Portal</div>
        <div style="margin-top: 8px; font-size: 12px; color: var(--text-secondary); font-weight: 600;">
            👤 {user_info['name']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stylish Theme Switcher Toggle Button in Sidebar
    t_col1, t_col2 = st.sidebar.columns([3, 1])
    with t_col1:
        st.markdown(f"**Theme**: {'🌙 Dark' if active_theme == 'dark' else '☀️ Light'}")
    with t_col2:
        if st.button("🔄", key="theme_toggle_btn", help="Switch between Dark & Light Mode"):
            toggle_theme()
            st.rerun()

    st.sidebar.markdown("---")

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

    # Logout Button
    if st.sidebar.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
        logout_user()
        st.toast("Signed out successfully.", icon="👋")
        st.rerun()

    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 11px; color: var(--text-secondary); margin-top: 20px;">
        RecruitFlow Enterprise v2.5<br/>SaaS Edition
    </div>
    """, unsafe_allow_html=True)

    # 4. Page Routing Engine
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
