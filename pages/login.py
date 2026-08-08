import streamlit as st
from utils.auth import login_user
from utils.theme import get_current_theme

def render_login_page():
    theme = get_current_theme()

    # Split Screen Layout (Left: Branding & Animated Workflow, Right: Login Card)
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("""
        <div style="padding: 30px 20px;">
            <div style="display: inline-block; padding: 6px 16px; border-radius: 9999px; background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.3); color: #3B82F6; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 20px;">
                HR Enterprise Platform
            </div>
            <h1 style="font-size: 42px; font-weight: 800; line-height: 1.1; margin-bottom: 12px; background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Email Automation Portal
            </h1>
            <p style="font-size: 18px; font-weight: 600; color: var(--text-secondary); margin-bottom: 20px;">
                Automate. Personalize. Communicate.
            </p>
            <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.6; max-width: 480px; margin-bottom: 35px;">
                Smart recruitment communication powered by automation. Streamline candidate processing, generate personalized Word & PDF offer letters, dispatch individual email campaigns, and track real-time hiring analytics.
            </p>
            
            <div style="background: var(--card-bg); backdrop-filter: blur(12px); border: 1px solid var(--card-border); border-radius: 16px; padding: 20px; box-shadow: var(--card-shadow);">
                <div style="font-size: 12px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px;">
                    Automated Recruitment Workflow
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; text-align: center; gap: 8px;">
                    <div style="flex: 1; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 18px;">📊</div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-primary); margin-top: 4px;">Excel</div>
                    </div>
                    <div style="color: var(--accent-color); font-weight: 700;">➔</div>
                    <div style="flex: 1; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 18px;">👥</div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-primary); margin-top: 4px;">Candidates</div>
                    </div>
                    <div style="color: var(--accent-color); font-weight: 700;">➔</div>
                    <div style="flex: 1; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 18px;">📄</div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-primary); margin-top: 4px;">Documents</div>
                    </div>
                    <div style="color: var(--accent-color); font-weight: 700;">➔</div>
                    <div style="flex: 1; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 18px;">📧</div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-primary); margin-top: 4px;">Emails</div>
                    </div>
                    <div style="color: var(--accent-color); font-weight: 700;">➔</div>
                    <div style="flex: 1; padding: 10px; background: rgba(59, 130, 246, 0.1); border-radius: 10px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 18px;">📈</div>
                        <div style="font-size: 11px; font-weight: 700; color: var(--text-primary); margin-top: 4px;">Analytics</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
        with st.form("form_glass_login"):
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="font-size: 24px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px;">HR Admin Sign In</h2>
                <p style="font-size: 13px; color: var(--text-secondary);">Enter credentials to access your workspace</p>
            </div>
            """, unsafe_allow_html=True)
            
            username_input = st.text_input("Username or Email", value="admin@abctechnologies.com", key="login_user_field")
            password_input = st.text_input("Password", type="password", value="admin123", key="login_pass_field")
            
            chk_remember = st.checkbox("Remember me", value=True, key="login_remember_chk")
            
            btn_submit_login = st.form_submit_button("Sign In to Portal 🚀", type="primary", use_container_width=True)

            if btn_submit_login:
                with st.spinner("Authenticating credentials..."):
                    success, msg = login_user(username_input, password_input)
                    if success:
                        st.toast("🎉 Sign in successful! Loading portal...", icon="✅")
                        st.rerun()
                    else:
                        st.error(msg)

        # Demo Credentials Popover
        with st.expander("🔑 Demo Credentials & Quick Access", expanded=True):
            st.markdown("""
            - **Default Username**: `admin@abctechnologies.com`
            - **Default Password**: `admin123`
            """)

        with st.popover("Forgot Password?"):
            st.info("To modify administrative passwords, update `ADMIN_EMAIL` and `ADMIN_PASSWORD` in your `.env` file or Streamlit Secrets configuration.")
