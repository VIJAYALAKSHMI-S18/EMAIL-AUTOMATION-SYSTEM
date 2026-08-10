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
    Inject high-contrast CSS styling ensuring 100% legibility in both Dark and Light modes.
    """
    if theme == "dark":
        bg_main = "#0F172A"       # Deep Slate 900
        bg_sidebar = "#1E293B"    # Slate 800
        bg_card = "#1E293B"       # Slate 800
        border_card = "#334155"   # Slate 700
        text_primary = "#FFFFFF"  # Pure Crisp White
        text_secondary = "#CBD5E1"# High Contrast Light Slate 300
        accent = "#3B82F6"        # Bright Royal Blue 500
        accent_hover = "#60A5FA"  # Light Blue 400
        input_bg = "#0F172A"      # Slate 900
        input_text = "#FFFFFF"    # Pure White
    else:
        bg_main = "#F8FAFC"       # Light Slate 50
        bg_sidebar = "#FFFFFF"    # Pure White
        bg_card = "#FFFFFF"       # Pure White
        border_card = "#E2E8F0"   # Slate 200
        text_primary = "#0F172A"  # Dark Slate 900
        text_secondary = "#475569"# Slate 600
        accent = "#2563EB"        # Blue 600
        accent_hover = "#1D4ED8"  # Blue 700
        input_bg = "#FFFFFF"      # White
        input_text = "#0F172A"    # Dark Slate

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* Main Application Background & Header Removal of White Bar */
        html, body, .stApp, header[data-testid="stHeader"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: {bg_main} !important;
            color: {text_primary} !important;
        }}
        
        header[data-testid="stHeader"] {{
            background: {bg_main} !important;
        }}

        /* Sidebar Styling & High-Contrast Text */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            border-right: 1px solid {border_card} !important;
        }}
        section[data-testid="stSidebar"] *,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {text_primary} !important;
        }}

        /* Navigation Radio Buttons - High Contrast White Text */
        div[class*="stRadio"] label,
        div[class*="stRadio"] label *,
        div[class*="stRadio"] p,
        div[class*="stRadio"] span {{
            color: {text_primary} !important;
            font-weight: 500 !important;
            font-size: 14px !important;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}

        /* Paragraphs, Labels & Captions */
        p, span, label, div {{
            color: {text_primary};
        }}

        .stCaption, caption {{
            color: {text_secondary} !important;
        }}

        /* Form Labels */
        label, .stSelectbox label, .stTextInput label, .stTextArea label, .stNumberInput label {{
            color: {text_primary} !important;
            font-weight: 600 !important;
        }}

        /* Inputs & Textareas */
        input[type="text"], input[type="password"], textarea {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1px solid {border_card} !important;
            border-radius: 8px !important;
        }}

        /* Selectbox Widget Popup Styling */
        div[data-baseweb="select"] > div {{
            background-color: {input_bg} !important;
            border-color: {border_card} !important;
            color: {input_text} !important;
        }}
        div[data-baseweb="popover"] * {{
            background-color: {bg_card} !important;
            color: {text_primary} !important;
        }}

        /* Buttons Styling */
        .stButton > button {{
            background: linear-gradient(135deg, {accent} 0%, {accent_hover} 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 18px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
        }}

        /* Metric Cards Styling */
        [data-testid="stMetric"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_card} !important;
            border-radius: 10px !important;
            padding: 14px 16px !important;
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

        /* Alert Boxes (Info, Success, Warning, Error) */
        div[data-testid="stNotification"],
        div[class*="stAlert"] {{
            background-color: {bg_card} !important;
            border: 1px solid {border_card} !important;
            color: {text_primary} !important;
        }}
        div[class*="stAlert"] * {{
            color: {text_primary} !important;
        }}

        /* Executive Card Class */
        .exec-card {{
            background-color: {bg_card};
            border: 1px solid {border_card};
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        .exec-card-title {{
            font-size: 17px;
            font-weight: 700;
            color: {text_primary};
        }}
        .exec-card-sub {{
            font-size: 13px;
            color: {text_secondary};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def get_plotly_layout_params(theme="dark"):
    """Return crisp high-contrast Plotly layout parameters."""
    if theme == "dark":
        return {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#FFFFFF", "family": "Inter", "size": 12},
            "colorway": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        }
    else:
        return {
            "template": "plotly_white",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#0F172A", "family": "Inter", "size": 12},
            "colorway": ["#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED"]
        }
