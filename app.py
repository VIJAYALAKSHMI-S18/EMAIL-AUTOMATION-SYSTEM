import sys
from pathlib import Path

# Ensure root workspace directory is at the top of sys.path for Streamlit Cloud compatibility
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import os
from database.database import init_db
from modules.candidate_manager import seed_sample_candidates_if_empty
from utils.auth import is_authenticated, logout_user, get_current_user
from utils.theme import get_current_theme, set_theme, inject_custom_theme

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

# 2. Inject Custom Theme Styling
active_theme = get_current_theme()
inject_custom_theme(active_theme)

# 3. Authentication Check
if not is_authenticated():
    from views.login import render_login_page
    render_login_page()
else:
    # Authenticated Main Portal Layout
    user_info = get_current_user()

    # Sidebar Header
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 10px 0; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.15);">
        <h2 style="margin: 0; font-size: 22px; font-weight: 800; color: #3B82F6;">RecruitFlow</h2>
        <div style="margin: 4px 0 0 0; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; color: var(--text-primary);">Enterprise HR Portal</div>
        <div style="margin: 6px 0 0 0; font-size: 13px; font-weight: 600; color: var(--text-primary);">👤 {user_info['name']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Streamlined 5-Item Navigation Menu
    nav_choice = st.sidebar.radio(
        "Main Navigation",
        [
            "🏠 Dashboard",
            "👥 Candidates",
            "📧 Email & Documents",
            "📊 Analytics & Logs",
            "⚙️ Settings & Help"
        ],
        index=0
    )

    st.sidebar.markdown("---")

    # Logout Button
    if st.sidebar.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
        logout_user()
        st.rerun()

    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 11px; color: var(--text-primary); margin-top: 20px; font-weight: 500;">
        RecruitFlow Enterprise v2.5
    </div>
    """, unsafe_allow_html=True)

    # 4. Streamlined Page Router Engine
    if nav_choice == "🏠 Dashboard":
        from views.dashboard import render_dashboard_page
        render_dashboard_page()

    elif nav_choice == "👥 Candidates":
        from views.candidates import render_candidates_page
        render_candidates_page()

    elif nav_choice == "📧 Email & Documents":
        from views.email_documents import render_email_documents_page
        render_email_documents_page()

    elif nav_choice == "📊 Analytics & Logs":
        from views.analytics_logs import render_analytics_logs_page
        render_analytics_logs_page()

    elif nav_choice == "⚙️ Settings & Help":
        from views.settings_help import render_settings_help_page
        render_settings_help_page()
