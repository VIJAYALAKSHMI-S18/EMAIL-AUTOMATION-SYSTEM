import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import datetime
import plotly.express as px
import pandas as pd

from database.database import (
    get_all_candidates,
    get_all_email_logs,
    get_setting
)
from utils.auth import get_current_user
from utils.theme import get_current_theme, get_plotly_layout_params

def get_greeting():
    """Return dynamic time-based greeting."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def render_dashboard_page():
    theme = get_current_theme()
    plotly_layout = get_plotly_layout_params(theme)
    user = get_current_user()
    greeting = get_greeting()
    today_str = datetime.date.today().strftime("%A, %d %B %Y")

    candidates = get_all_candidates()
    email_logs = get_all_email_logs()
    email_mode = get_setting("email_mode", "Demo Mode")

    # Header Row
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown(f"## {greeting}, {user['name']} 👋")
        st.caption(f"HR Overview • {today_str}")

    with head_col2:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if email_mode == "Demo Mode":
            st.markdown("<span class='badge badge-warning'>🟡 Demo Mode Active</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge badge-success'>🟢 Gmail SMTP Active</span>", unsafe_allow_html=True)

    st.markdown("---")

    # Metric Calculations
    total_cands = len(candidates)
    selected_cands = len([c for c in candidates if c.get("offer_status") == "Selected"])
    emails_sent = len([l for l in email_logs if l.get("status") == "SUCCESS"])
    emails_failed = len([l for l in email_logs if l.get("status") == "FAILED"])

    # 4 Executive Metric Cards with Icons & High Contrast
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="exec-card" style="padding: 16px; border-left: 4px solid #3B82F6;">
            <div style="font-size: 12px; font-weight: 700; opacity: 0.8; text-transform: uppercase;">👥 Total Candidates</div>
            <div style="font-size: 32px; font-weight: 800; color: #3B82F6; margin-top: 4px;">{total_cands}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="exec-card" style="padding: 16px; border-left: 4px solid #10B981;">
            <div style="font-size: 12px; font-weight: 700; opacity: 0.8; text-transform: uppercase;">🎯 Selected</div>
            <div style="font-size: 32px; font-weight: 800; color: #10B981; margin-top: 4px;">{selected_cands}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="exec-card" style="padding: 16px; border-left: 4px solid #6366F1;">
            <div style="font-size: 12px; font-weight: 700; opacity: 0.8; text-transform: uppercase;">📧 Emails Dispatched</div>
            <div style="font-size: 32px; font-weight: 800; color: #6366F1; margin-top: 4px;">{emails_sent}</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="exec-card" style="padding: 16px; border-left: 4px solid #EF4444;">
            <div style="font-size: 12px; font-weight: 700; opacity: 0.8; text-transform: uppercase;">⚠️ Failed Dispatches</div>
            <div style="font-size: 32px; font-weight: 800; color: #EF4444; margin-top: 4px;">{emails_failed}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2 Side-by-Side Plotly Charts with Crisp White Text & Fixed Height
    c1, c2 = st.columns(2)

    font_color = "#FFFFFF" if theme == "dark" else "#0F172A"

    with c1:
        st.markdown("### Candidate Status")
        if candidates:
            cand_df = pd.DataFrame(candidates)
            status_counts = cand_df['offer_status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            fig1 = px.pie(
                status_counts,
                values='Count',
                names='Status',
                hole=0.5,
                color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
            )
            fig1.update_layout(
                template=plotly_layout["template"],
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=font_color, family="Inter", size=13),
                legend=dict(font=dict(color=font_color, size=12), orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                margin=dict(t=10, b=30, l=10, r=10),
                height=250
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No candidates data available yet.")

    with c2:
        st.markdown("### Candidates by Department")
        if candidates:
            cand_df = pd.DataFrame(candidates)
            dept_counts = cand_df['department'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Candidates']

            fig2 = px.bar(
                dept_counts,
                x='Candidates',
                y='Department',
                orientation='h',
                color_discrete_sequence=['#3B82F6']
            )
            fig2.update_layout(
                template=plotly_layout["template"],
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color=font_color, family="Inter", size=13),
                xaxis=dict(tickfont=dict(color=font_color), title=dict(font=dict(color=font_color))),
                yaxis=dict(tickfont=dict(color=font_color), title=dict(font=dict(color=font_color))),
                margin=dict(t=10, b=20, l=10, r=10),
                height=250
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No department data available yet.")

    st.markdown("---")

    # Recent Activity Feed
    st.markdown("### Recent Activity Stream")
    if email_logs:
        for log in email_logs[:4]:
            c_name = log.get("candidate_name") or log.get("candidate_id")
            subject = log.get("subject")
            sent_at = log.get("sent_at")
            status = log.get("status")

            badge_html = "<span class='badge badge-success'>SUCCESS</span>" if status == "SUCCESS" else "<span class='badge badge-failed'>FAILED</span>"

            st.markdown(f"""
            <div class="exec-card" style="padding: 10px 16px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: {font_color};">{c_name}</strong> &nbsp;—&nbsp; <span style="font-size: 13px; color: {font_color}; opacity: 0.85;">{subject}</span>
                    </div>
                    <div>
                        {badge_html} &nbsp; <span style="font-size: 12px; color: {font_color}; opacity: 0.7;">{sent_at}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent email activity recorded yet.")
