import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils.auth import login_user

def render_login_page():
    # Hero Title Banner
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <h1 style="font-size: 36px; font-weight: 800; margin-bottom: 6px;">Email Automation Portal</h1>
        <p style="font-size: 16px; font-weight: 500; opacity: 0.8; margin-top: 0;">Smart Recruitment Communication Management</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Split Screen Layout
    col_info, col_login = st.columns([1.2, 1], gap="large")

    with col_info:
        st.markdown("### Executive HR Platform")
        st.markdown("""
        Streamline your recruitment communication workflow from candidate import to document issuance and campaign tracking:
        """)

        # Clean Workflow Steps
        st.markdown("#### Automated Pipeline Workflow")
        
        w_col1, w_col2, w_col3, w_col4, w_col5 = st.columns(5)
        with w_col1:
            st.metric("1. Excel", "Upload")
        with w_col2:
            st.metric("2. Candidate", "Directory")
        with w_col3:
            st.metric("3. Document", "Generate")
        with w_col4:
            st.metric("4. Emails", "Dispatch")
        with w_col5:
            st.metric("5. Analytics", "Track")

        st.markdown("---")
        st.info("💡 **Enterprise Features**: Dynamic placeholder personalization, Word (.docx) & PDF (.pdf) document generation, Demo & Gmail SMTP dispatches, and real-time Plotly reporting.")

    with col_login:
        with st.form("form_executive_login"):
            st.markdown("### HR Admin Sign In")
            st.caption("Enter administrative credentials to access your portal workspace.")

            username_input = st.text_input("Username or Email", value="admin@abctechnologies.com", key="login_user_field")
            password_input = st.text_input("Password", type="password", value="admin123", key="login_pass_field")
            
            chk_remember = st.checkbox("Remember me in this session", value=True, key="login_remember_chk")
            
            btn_submit_login = st.form_submit_button("Sign In to Portal 🚀", type="primary", use_container_width=True)

            if btn_submit_login:
                with st.spinner("Authenticating credentials..."):
                    success, msg = login_user(username_input, password_input)
                    if success:
                        st.success("Authentication successful! Loading workspace...")
                        st.rerun()
                    else:
                        st.error(msg)

        # Demo Access Quick Guide
        with st.expander("🔑 Demo Access Credentials", expanded=True):
            st.markdown("""
            - **Default Username**: `admin@abctechnologies.com`
            - **Default Password**: `admin123`
            """)

        with st.popover("Forgot Password?"):
            st.info("To modify administrative passwords, update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in your `.env` file or Streamlit Secrets configuration.")
