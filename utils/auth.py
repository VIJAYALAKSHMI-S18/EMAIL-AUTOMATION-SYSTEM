import streamlit as st
import os
from database.database import get_setting, set_setting

def is_authenticated():
    """Check if current session is authenticated."""
    return st.session_state.get("authenticated", False)

def login_user(username_or_email, password):
    """
    Authenticate user against stored settings or environment / defaults.
    Default Admin: admin@abctechnologies.com / admin123
    """
    admin_user = os.getenv("ADMIN_EMAIL") or get_setting("admin_email", "admin@abctechnologies.com")
    admin_pass = os.getenv("ADMIN_PASSWORD") or get_setting("admin_password", "admin123")

    clean_input_user = str(username_or_email).strip().lower()
    clean_input_pass = str(password).strip()

    if clean_input_user in [admin_user.lower(), "admin", "hradmin"] and clean_input_pass == admin_pass:
        st.session_state["authenticated"] = True
        st.session_state["user_email"] = admin_user
        st.session_state["user_name"] = get_setting("hr_name", "HR Lead Admin")
        st.session_state["user_role"] = "Senior Recruitment Manager"
        return True, "Login successful!"
    
    return False, "Invalid username/email or password."

def logout_user():
    """Clear authentication session state."""
    st.session_state["authenticated"] = False
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None
    st.session_state["user_role"] = None

def get_current_user():
    """Return dict of current logged in user details."""
    return {
        "name": st.session_state.get("user_name", "HR Admin"),
        "email": st.session_state.get("user_email", "admin@abctechnologies.com"),
        "role": st.session_state.get("user_role", "Recruitment Administrator")
    }
