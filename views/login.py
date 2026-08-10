import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils.auth import login_user

def render_login_page():
    # Use centered columns for a sleek, minimal, clutter-free login card
    _, col_center, _ = st.columns([1, 1.2, 1])

    with col_center:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # Header Brand Logo & Title
        st.markdown("""
        <div style="text-align: center; margin-bottom: 25px;">
            <div style="font-size: 40px; margin-bottom: 5px;">⚡</div>
            <h2 style="font-size: 26px; font-weight: 800; margin: 0;">RecruitFlow</h2>
            <p style="font-size: 13px; opacity: 0.75; margin-top: 4px;">Recruitment Email Automation Portal</p>
        </div>
        """, unsafe_allow_html=True)

        # Minimal Sign In Form Card
        with st.form("form_clean_login"):
            username_input = st.text_input(
                "Username or Email",
                value="",
                placeholder="e.g. admin@abctechnologies.com",
                key="login_user_field"
            )
            password_input = st.text_input(
                "Password",
                type="password",
                value="",
                placeholder="Enter password",
                key="login_pass_field"
            )

            chk_remember = st.checkbox("Remember me", value=True, key="login_remember_chk")
            btn_submit_login = st.form_submit_button("Sign In 🚀", type="primary", use_container_width=True)

            if btn_submit_login:
                if not username_input or not password_input:
                    st.error("Please enter both username and password.")
                else:
                    with st.spinner("Authenticating..."):
                        success, msg = login_user(username_input, password_input)
                        if success:
                            st.success("Welcome back!")
                            st.rerun()
                        else:
                            st.error(msg)

        # Minimal Demo Hint Box (No walls of text)
        st.markdown("""
        <div class="exec-card" style="text-align: center; padding: 12px; margin-top: 15px;">
            <span style="font-size: 12px; font-weight: 600;">🔑 Demo Credentials:</span><br/>
            <code style="font-size: 12px;">admin@abctechnologies.com</code> &nbsp;|&nbsp; <code style="font-size: 12px;">admin123</code>
        </div>
        """, unsafe_allow_html=True)
