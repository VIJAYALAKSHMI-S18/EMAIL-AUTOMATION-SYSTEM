import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from utils.auth import login_user

def render_login_page():
    # Hero Title Header
    st.markdown("""
    <div style="text-align: center; padding: 15px 0 25px 0;">
        <h1 style="font-size: 34px; font-weight: 800; margin-bottom: 6px;">Email Automation Portal</h1>
        <p style="font-size: 15px; opacity: 0.85; margin-top: 0;">Smart Recruitment Communication Management</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Two-Column Layout
    col_info, col_login = st.columns([1.1, 1], gap="large")

    with col_info:
        st.markdown("### Executive HR Platform")
        st.write(
            "Streamline your recruitment communication workflow from candidate data import to document issuance, "
            "email campaign dispatches, and real-time hiring analytics."
        )

        st.markdown("#### Automated Recruitment Pipeline")
        st.markdown("""
        - **1. Excel Data Ingestion**: Import candidates with validation & duplicate detection.
        - **2. Candidate Management**: Filter, search, and manage candidate directory.
        - **3. Document Generation**: Generate personalized Word (.docx) & PDF (.pdf) offer letters and certificates.
        - **4. Email Automation**: Compose personalized emails with attachments & preview.
        - **5. Tracking & Analytics**: Audit dispatch history with failure retry and Plotly charts.
        """)

        st.markdown("---")
        st.info("💡 **Demo System**: Supports both simulated Demo Mode and live Gmail SMTP transmission.")

    with col_login:
        st.markdown("### HR Admin Sign In")
        st.write("Enter administrative credentials to access your portal workspace.")

        with st.form("form_executive_login"):
            # Empty input boxes with helpful placeholder hints (NO auto-filled values)
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
                placeholder="Enter your password",
                key="login_pass_field"
            )

            chk_remember = st.checkbox("Remember me in this session", value=True, key="login_remember_chk")

            btn_submit_login = st.form_submit_button("Sign In to Portal 🚀", type="primary", use_container_width=True)

            if btn_submit_login:
                if not username_input or not password_input:
                    st.error("Please enter both username/email and password.")
                else:
                    with st.spinner("Authenticating credentials..."):
                        success, msg = login_user(username_input, password_input)
                        if success:
                            st.success("Authentication successful! Loading workspace...")
                            st.rerun()
                        else:
                            st.error(msg)

        # Clean Demo Credentials Display (No overlapping text)
        st.markdown("---")
        st.markdown("#### Demo Access Credentials")
        st.markdown("""
        * **Default Email**: `admin@abctechnologies.com`
        * **Default Password**: `admin123`
        """)
        st.caption("Enter the above default credentials into the Sign In fields to log in.")
