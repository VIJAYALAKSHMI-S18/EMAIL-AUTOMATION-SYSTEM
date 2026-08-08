import streamlit as st
from utils.auth import login_user

def render_login_page():
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #2563EB; font-weight: 800; font-size: 38px; margin-bottom: 5px;">Email Automation Portal</h1>
        <p style="color: #64748B; font-size: 16px; font-weight: 500; margin-top: 0;">Smart Recruitment Communication Management</p>
        <p style="color: #475569; max-width: 650px; margin: 15px auto 25px auto; line-height: 1.5; font-size: 14px;">
            An intelligent recruitment communication platform that automates candidate data processing, 
            personalized document generation, individual email communication, and campaign tracking.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow Visual Diagram
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 15px; margin-bottom: 30px; text-align: center;">
        <span style="font-weight: 600; color: #1E293B; font-size: 13px;">AUTOMATION WORKFLOW:</span><br/>
        <div style="display: flex; justify-content: space-around; align-items: center; margin-top: 10px; flex-wrap: wrap; gap: 8px; font-size: 13px; font-weight: 600; color: #2563EB;">
            <span>Excel Data</span> ➔ 
            <span>Candidate Processing</span> ➔ 
            <span>Document Generation</span> ➔ 
            <span>Email Automation</span> ➔ 
            <span>Tracking & Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered Login Card Container
    l_col1, l_col2, l_col3 = st.columns([1, 2, 1])

    with l_col2:
        with st.form("form_login_card"):
            st.markdown("<h3 style='text-align: center; color: #1E293B; margin-top:0;'>HR Admin Sign In</h3>", unsafe_allow_html=True)
            
            username_input = st.text_input("Username or Email", value="admin@abctechnologies.com", key="login_user_field")
            password_input = st.text_input("Password", type="password", value="admin123", key="login_pass_field")
            
            chk_remember = st.checkbox("Remember me", value=True, key="login_remember_chk")
            
            btn_submit_login = st.form_submit_button("Sign In to Portal", type="primary", use_container_width=True)

            if btn_submit_login:
                success, msg = login_user(username_input, password_input)
                if success:
                    st.success("Authentication successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(msg)

        # Demo Credentials & Help Hint
        with st.expander("🔑 Demo Access Credentials & Quick Guide", expanded=True):
            st.markdown("""
            - **Default Email**: `admin@abctechnologies.com`
            - **Default Password**: `admin123`
            
            *You can customize administrative passwords in System Settings or via Streamlit Secrets.*
            """)

        with st.popover("Forgot Password?"):
            st.info("To reset administrative credentials, update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in your `.env` file or Streamlit Secrets configuration.")
