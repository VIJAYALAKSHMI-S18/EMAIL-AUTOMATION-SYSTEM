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

    # Header Row with Mode Badge
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown(f"## {greeting}, {user['name']} 👋")
        st.caption(f"Recruitment Communication Overview • {today_str}")

    with head_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if email_mode == "Demo Mode":
            st.markdown("<span class='badge badge-warning'>🟡 Demo Mode Active</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span class='badge badge-success'>🟢 Gmail SMTP Active</span>", unsafe_allow_html=True)

    st.markdown("---")

    # Metric Calculations
    total_candidates = len(candidates)
    selected_candidates = len([c for c in candidates if c.get("offer_status") == "Selected"])
    emails_sent = len([l for l in email_logs if l.get("status") == "SUCCESS"])
    emails_failed = len([l for l in email_logs if l.get("status") == "FAILED"])

    # 4 Spacious Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Candidates", total_candidates)
    with m2:
        st.metric("Selected Candidates", selected_candidates)
    with m3:
        st.metric("Emails Dispatched", emails_sent)
    with m4:
        st.metric("Failed Dispatches", emails_failed)

    st.markdown("---")

    # 2 Essential Side-by-Side Visual Charts
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Candidate Status Distribution")
        if candidates:
            cand_df = pd.DataFrame(candidates)
            status_counts = cand_df['offer_status'].value_counts().reset_index()
            status_counts.columns = ['Status', 'Count']

            fig1 = px.pie(
                status_counts,
                values='Count',
                names='Status',
                hole=0.45,
                color_discrete_sequence=['#3B82F6', '#10B981', '#F59E0B', '#EF4444']
            )
            fig1.update_layout(
                template=plotly_layout["template"],
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=plotly_layout["font"],
                margin=dict(t=20, b=20, l=20, r=20),
                height=290
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No candidate data available yet.")

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
                font=plotly_layout["font"],
                margin=dict(t=20, b=20, l=20, r=20),
                height=290
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No department data available yet.")

    st.markdown("---")

    # Clean Recent Activity Log Stream
    st.markdown("### Recent Activity Stream")
    if email_logs:
        for log in email_logs[:5]:
            c_name = log.get("candidate_name") or log.get("candidate_id")
            subject = log.get("subject")
            sent_at = log.get("sent_at")
            status = log.get("status")

            badge_html = "<span class='badge badge-success'>SUCCESS</span>" if status == "SUCCESS" else "<span class='badge badge-failed'>FAILED</span>"

            st.markdown(f"""
            <div class="exec-card" style="padding: 12px 16px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>{c_name}</strong> &nbsp;—&nbsp; <span style="font-size: 13px; opacity: 0.85;">{subject}</span>
                    </div>
                    <div>
                        {badge_html} &nbsp; <span style="font-size: 12px; opacity: 0.7;">{sent_at}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent email activity recorded yet.")
