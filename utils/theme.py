import streamlit as st

def get_current_theme():
    """Retrieve active theme ('dark' or 'light'). Default: 'dark'."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"
    return st.session_state["theme"]

def toggle_theme():
    """Toggle theme state."""
    current = get_current_theme()
    st.session_state["theme"] = "light" if current == "dark" else "dark"

def get_theme_css(theme="dark"):
    """
    Generate comprehensive CSS for Glassmorphic HR SaaS UI & Custom Cursor.
    """
    if theme == "dark":
        bg_primary = "#0B0F19"
        sidebar_bg = "#0F172A"
        card_bg = "rgba(30, 41, 59, 0.7)"
        card_border = "rgba(255, 255, 255, 0.1)"
        card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
        text_primary = "#F8FAFC"
        text_secondary = "#94A3B8"
        accent_color = "#3B82F6"
        accent_glow = "rgba(59, 130, 246, 0.4)"
        input_bg = "rgba(15, 23, 42, 0.6)"
        input_border = "rgba(255, 255, 255, 0.15)"
        hover_bg = "rgba(59, 130, 246, 0.15)"
    else: # Light Mode
        bg_primary = "#F8FAFC"
        sidebar_bg = "#FFFFFF"
        card_bg = "rgba(255, 255, 255, 0.85)"
        card_border = "rgba(226, 232, 240, 0.8)"
        card_shadow = "0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)"
        text_primary = "#0F172A"
        text_secondary = "#64748B"
        accent_color = "#2563EB"
        accent_glow = "rgba(37, 99, 235, 0.25)"
        input_bg = "#FFFFFF"
        input_border = "#CBD5E1"
        hover_bg = "rgba(37, 99, 235, 0.08)"

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
        
        :root {{
            --bg-primary: {bg_primary};
            --sidebar-bg: {sidebar_bg};
            --card-bg: {card_bg};
            --card-border: {card_border};
            --card-shadow: {card_shadow};
            --text-primary: {text_primary};
            --text-secondary: {text_secondary};
            --accent-color: {accent_color};
            --accent-glow: {accent_glow};
            --input-bg: {input_bg};
            --input-border: {input_border};
            --hover-bg: {hover_bg};
        }}

        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }}

        .stApp {{
            background-color: var(--bg-primary) !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background-color: var(--sidebar-bg) !important;
            border-right: 1px solid var(--card-border) !important;
        }}

        /* Custom Glassmorphic Cards */
        .saas-card {{
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            box-shadow: var(--card-shadow);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .saas-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 30px -5px var(--accent-glow);
            border-color: var(--accent-color);
        }}

        /* Metric Cards Styling */
        [data-testid="stMetric"] {{
            background: var(--card-bg) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 14px !important;
            padding: 18px !important;
            box-shadow: var(--card-shadow) !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 20px var(--accent-glow) !important;
            border-color: var(--accent-color) !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 30px !important;
            font-weight: 800 !important;
            color: var(--accent-color) !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 13px !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
        }}

        /* Buttons Styling */
        .stButton > button {{
            background: linear-gradient(135deg, var(--accent-color) 0%, #1D4ED8 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            box-shadow: 0 4px 14px var(--accent-glow) !important;
            transition: all 0.25s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 6px 20px var(--accent-glow) !important;
            filter: brightness(1.1) !important;
        }}

        /* Inputs & Textareas */
        input[type="text"], input[type="password"], textarea, select, [data-baseweb="select"] {{
            background-color: var(--input-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--input-border) !important;
            border-radius: 10px !important;
        }}
        input:focus, textarea:focus {{
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 2px var(--accent-glow) !important;
        }}

        /* Badges & Status Pills */
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .badge-success {{ background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-warning {{ background: rgba(245, 158, 11, 0.15); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-failed  {{ background: rgba(239, 68, 68, 0.15); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.3); }}
        .badge-info    {{ background: rgba(59, 130, 246, 0.15); color: #3B82F6; border: 1px solid rgba(59, 130, 246, 0.3); }}

        /* CUSTOM CURSOR OVERLAY */
        .cursor-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--accent-color);
            position: fixed;
            top: 0;
            left: 0;
            border-radius: 50%;
            pointer-events: none;
            z-index: 99999;
            transition: transform 0.1s ease;
            box-shadow: 0 0 10px var(--accent-color);
        }}
        .cursor-ring {{
            width: 28px;
            height: 28px;
            border: 2px solid var(--accent-color);
            position: fixed;
            top: 0;
            left: 0;
            border-radius: 50%;
            pointer-events: none;
            z-index: 99998;
            opacity: 0.6;
            transition: transform 0.15s ease-out, width 0.2s ease, height 0.2s ease, opacity 0.2s ease;
        }}
        body:hover .cursor-ring {{
            opacity: 0.8;
        }}
    </style>

    <div class="cursor-dot" id="cursorDot"></div>
    <div class="cursor-ring" id="cursorRing"></div>

    <script>
        (function() {{
            const dot = document.getElementById('cursorDot');
            const ring = document.getElementById('cursorRing');
            if(!dot || !ring) return;

            let mouseX = -100, mouseY = -100;
            let ringX = -100, ringY = -100;

            document.addEventListener('mousemove', (e) => {{
                mouseX = e.clientX;
                mouseY = e.clientY;
                dot.style.transform = `translate3d(${{mouseX - 4}}px, ${{mouseY - 4}}px, 0)`;
            }});

            function render() {{
                ringX += (mouseX - ringX) * 0.2;
                ringY += (mouseY - ringY) * 0.2;
                ring.style.transform = `translate3d(${{ringX - 14}}px, ${{ringY - 14}}px, 0)`;
                requestAnimationFrame(render);
            }}
            render();

            // Hover expansion over interactive elements
            document.querySelectorAll('button, .saas-card, a, input, select, [role="button"]').forEach(el => {{
                el.addEventListener('mouseenter', () => {{
                    ring.style.width = '42px';
                    ring.style.height = '42px';
                    ring.style.backgroundColor = 'rgba(59, 130, 246, 0.15)';
                }});
                el.addEventListener('mouseleave', () => {{
                    ring.style.width = '28px';
                    ring.style.height = '28px';
                    ring.style.backgroundColor = 'transparent';
                }});
            }});
        }})();
    </script>
    """
    return css

def get_plotly_layout_params(theme="dark"):
    """
    Return layout dictionary for Plotly charts matching active theme.
    """
    if theme == "dark":
        return {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#F8FAFC", "family": "Plus Jakarta Sans"},
            "colorway": ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
        }
    else:
        return {
            "template": "plotly_white",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"color": "#0F172A", "family": "Plus Jakarta Sans"},
            "colorway": ["#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED"]
        }
