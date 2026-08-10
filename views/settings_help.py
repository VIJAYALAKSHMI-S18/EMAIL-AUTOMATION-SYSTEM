import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import os
from database.database import get_setting, set_setting
from utils.auth import get_current_user
from utils.theme import get_current_theme, set_theme

def render_settings_help_page():
    st.markdown("## Settings & Quick Help")
    st.markdown("Configure email transmission, Gmail SMTP credentials, theme preferences, and access the system setup guide.")

    user = get_current_user()
    active_theme = get_current_theme()

    tab_config, tab_smtp, tab_help = st.tabs([
        "⚙️ System Configuration",
        "📧 Gmail SMTP Setup Guide",
        "❓ Quick User Guide"
    ])

    # Tab 1: Configuration
    with tab_config:
        st.markdown("### Profile & Email Transmission Mode")
        current_mode = get_setting("email_mode", "Demo Mode")

        new_mode = st.radio(
            "Transmission Engine",
            ["Demo Mode", "Gmail SMTP"],
            index=0 if current_mode == "Demo Mode" else 1,
            horizontal=True,
            help="Demo Mode simulates sending for testing. Gmail SMTP connects to live Google servers."
        )

        if new_mode != current_mode:
            set_setting("email_mode", new_mode)
            st.toast(f"Mode changed to {new_mode}", icon="✅")
            st.rerun()

        st.markdown("---")

        st.markdown("### Visual Theme")
        selected_theme = st.selectbox(
            "Theme Preference",
            ["Dark Mode", "Light Mode"],
            index=0 if active_theme == "dark" else 1,
            key="sh_theme_select"
        )
        new_theme = "dark" if selected_theme == "Dark Mode" else "light"
        if new_theme != active_theme:
            set_theme(new_theme)
            st.rerun()

    # Tab 2: Gmail SMTP Setup Guide
    with tab_smtp:
        st.markdown("### 📧 Setting Up Gmail SMTP (Live Emails)")
        st.markdown("""
        To send live emails to candidates using your Gmail address:

        1. Go to your **Google Account** at [myaccount.google.com](https://myaccount.google.com).
        2. Click **Security** ➔ Ensure **2-Step Verification** is turned **ON**.
        3. Search for **App Passwords** ➔ Create a 16-character password for `RecruitFlow`.
        4. Configure credentials in **Streamlit Secrets** or `.env` file:
           ```toml
           EMAIL_ADDRESS = "your_email@gmail.com"
           EMAIL_PASSWORD = "abcdefghijklmnop"
           ```
        5. Select **Gmail SMTP** in System Configuration above.
        """)

    # Tab 3: Quick User Guide
    with tab_help:
        st.markdown("### ❓ Quick User Guide")
        st.markdown("""
        - **How to upload candidates**: Go to **👥 Candidates** ➔ Use the Excel Management tab to upload `.xlsx` files.
        - **How to generate offer letters**: Select candidates in **👥 Candidates** ➔ Go to **📧 Email & Documents** ➔ Click Generate.
        - **How to resend failed emails**: Go to **📊 Analytics & Logs** ➔ Click **Retry Send** on failed logs.
        """)
