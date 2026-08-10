import streamlit as st

def get_current_theme():
    """Retrieve active theme ('dark' or 'light'). Default: 'dark'."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    return st.session_state["theme"]

def set_theme(theme_name):
    """Set active theme ('dark' or 'light')."""
    if theme_name in ["dark", "light"]:
        st.session_state["theme"] = theme_name

def toggle_theme():
    """Toggle theme state between dark and light."""
    current = get_current_theme()
    st.session_state["theme"] = "light" if current == "dark" else "dark"

def inject_custom_theme(theme="dark"):
    """
    Inject clean, non-breaking executive SaaS CSS styling.
    Ensures zero label overlaps, zero icon text collisions, and crisp readability.
    """
    if theme == "dark":
        bg_main = "#0F172A"       # Slate 900
        bg_sidebar = "#1E293B"    # Slate 800
        bg_card = "#1E293B"       # Slate 800
        border_card = "#334155"   # Slate 700
        text_primary = "#F8FAFC"  # Slate 50
        text_secondary = "#94A3B8"# Slate 400
        accent = "#3B82F6"        # Blue 500
        accent_hover = "#2563EB"  # Blue 600
        input_bg = "#0F172A"      # Slate 900
        input_text = "#F8FAFC"    # Slate 50
    else:
        bg_main = "#F8FAFC"       # Slate 50
        bg_sidebar = "#FFFFFF"    # White
        bg_card = "#FFFFFF"       # White
        border_card = "#E2E8F0"   # Slate 200
        text_primary = "#0F172A"  # Slate 900
        text_secondary = "#64748B"# Slate 500
        accent = "#2563EB"        # Blue 600
        accent_hover = "#1D4ED8"  # Blue 700
        input_bg = "#FFFFFF"      # White
        input_text = "#0F172A"    # Slate 900

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Global Typography & App Background */
        html, body, .stApp {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}

        /* Sidebar Container */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            border-right: 1px solid {border_card} !important;
        }}

        /* Main Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
            font-weight: 700 !important;
            letter-spacing: -0.3px !important;
        }}

        /* Metric Cards Styling - Clean & Non-truncated */
        [data-testid="stMetric"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05) !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 26px !important;
            font-weight: 800 !important;
            color: {accent} !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: {text_secondary} !important;
        }}

        /* Clean Form Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, {accent} 0%, {accent_hover} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 18px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
        }}

        /* Executive Card Class */
        .exec-card {{
            background-color: {bg_card};
            border: 1px solid {border_card};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        }}
        .exec-card-title {{
            font-size: 17px;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 4px;
        }}
        .exec-card-sub {{
            font-size: 13px;
            color: {text_secondary};
            margin-bottom: 12px;
        }}

        /* Badges */
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .badge-success {{ background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-failed  {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }}
        .badge-info    {{ background: rgba(59, 130, 246, 0.15); color: #3B82F6; border: 1px solid rgba(59, 130, 246, 0.3); }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_plotly_layout_params(theme="dark"):
    """Return clean Plotly layout parameters matching active theme."""
    if theme == "dark":
        return {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#F8FAFC", "family": "Inter"},
            "colorway": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        }
    else:
        return {
            "template": "plotly_white",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#0F172A", "family": "Inter"},
            "colorway": ["#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED"]
        }
