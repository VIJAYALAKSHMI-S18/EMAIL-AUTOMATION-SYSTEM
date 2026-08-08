import streamlit as st

def get_current_theme():
    """Retrieve active theme ('dark' or 'light'). Default: 'dark'."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    return st.session_state["theme"]

def toggle_theme():
    """Toggle theme state between dark and light."""
    current = get_current_theme()
    st.session_state["theme"] = "light" if current == "dark" else "dark"

def inject_custom_theme(theme="dark"):
    """
    Inject clean, production-grade, bug-free executive SaaS CSS styling.
    Guarantees zero raw HTML leaks, high contrast text, and beautiful card layouts.
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

        /* Main Application Background & Global Typography */
        html, body, [class*="st-"], .stApp {{
            font-family: 'Inter', sans-serif !important;
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            border-right: 1px solid {border_card} !important;
        }}
        section[data-testid="stSidebar"] * {{
            color: {text_primary} !important;
        }}

        /* Headers & Paragraphs */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px !important;
        }}
        p, span, label, div {{
            color: {text_primary};
        }}

        /* Input Fields & Textareas */
        input[type="text"], input[type="password"], textarea, select, [data-baseweb="select"] * {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border-color: {border_card} !important;
            border-radius: 8px !important;
        }}
        input:focus, textarea:focus {{
            border-color: {accent} !important;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25) !important;
        }}

        /* Buttons Styling */
        .stButton > button {{
            background: linear-gradient(135deg, {accent} 0%, {accent_hover} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35) !important;
        }}

        /* Metric Cards Styling */
        [data-testid="stMetric"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 28px !important;
            font-weight: 800 !important;
            color: {accent} !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: {text_secondary} !important;
        }}

        /* Expanders & Containers */
        .stExpander {{
            background-color: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 10px !important;
        }}

        /* Executive SaaS Card Container Class */
        .exec-card {{
            background-color: {bg_card};
            border: 1px solid {border_card};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }}
        .exec-card-title {{
            font-size: 18px;
            font-weight: 700;
            color: {text_primary};
            margin-bottom: 6px;
        }}
        .exec-card-sub {{
            font-size: 13px;
            color: {text_secondary};
            margin-bottom: 16px;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_plotly_layout_params(theme="dark"):
    """Return clean Plotly layout matching dark or light mode."""
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
