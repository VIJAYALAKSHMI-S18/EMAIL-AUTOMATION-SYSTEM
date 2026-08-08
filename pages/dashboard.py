import streamlit as st
import datetime
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from database.database import (
    get_all_candidates,
    get_all_documents,
    get_all_email_logs,
    get_setting
)
from utils.auth import get_current_user

def get_greeting():
    """Return dynamic greeting based on current time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 17:
        return "Good Afternoon"
    else:
        return "Good Evening"

def render_dashboard_page():
    user = get_current_user()
    greeting = get_greeting()

    st.markdown(f"## {greeting}, {user['name']} 👋")
    st.markdown("Here's your recruitment communication overview.")

    candidates = get_all_candidates()
    documents = get_all_documents()
    email_logs = get_all_email_logs()
    email_mode = get_setting("email_mode", "Demo Mode")

    # Mode Notice
    if email_mode == "Demo Mode":
        st.info("System Mode: Demo Mode (Emails are simulated and logged to SQLite). Switch to Gmail SMTP in Settings for live emails.")
    else:
        st.success("System Mode: Gmail SMTP (Live emails are active via Gmail SMTP).")

    # Metric Calculations
    total_candidates = len(candidates)
    selected_candidates = len([c for c in candidates if c.get("offer_status") == "Selected"])
    emails_sent = len([l for l in email_logs if l.get("status") == "SUCCESS"])
    emails_failed = len([l for l in email_logs if l.get("status") == "FAILED"])
    emails_pending = len([l for l in email_logs if l.get("status") == "PENDING"])
    selection_rate = (selected_candidates / total_candidates * 100) if total_candidates > 0 else 0.0

    # Top Metric Cards Layout
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Candidates", total_candidates)
    with col2:
        st.metric("Selected Candidates", selected_candidates, delta=f"{selection_rate:.1f}% Rate")
    with col3:
        st.metric("Emails Sent", emails_sent)
    with col4:
        st.metric("Pending Emails", emails_pending)
    with col5:
        st.metric("Failed Emails", emails_failed)

    st.markdown("---")

    # Row 1: Interactive Plotly Charts
    st.markdown("### Recruitment Analytics & Distribution")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Candidate Offer Status")
        if candidates:
            status_df = pd.DataFrame(candidates)
            offer_counts = status_df['offer_status'].value_counts().reset_index()
            offer_counts.columns = ['Status', 'Count']
            
            fig1 = px.pie(
                offer_counts,
                values='Count',
                names='Status',
                hole=0.4,
                color_discrete_sequence=['#2563EB', '#059669', '#D97706', '#DC2626']
            )
            fig1.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No candidates available for plotting.")

    with c2:
        st.markdown("#### Email Dispatch Status")
        if email_logs:
            logs_df = pd.DataFrame(email_logs)
            log_counts = logs_df['status'].value_counts().reset_index()
            log_counts.columns = ['Status', 'Count']

            fig2 = px.bar(
                log_counts,
                x='Status',
                y='Count',
                color='Status',
                color_discrete_map={'SUCCESS': '#059669', 'FAILED': '#DC2626', 'PENDING': '#D97706'}
            )
            fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No email campaign logs available yet.")

    # Row 2: Department & Activity Charts
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Candidates by Department")
        if candidates:
            cand_df = pd.DataFrame(candidates)
            dept_counts = cand_df['department'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Candidates']

            fig3 = px.bar(
                dept_counts,
                x='Candidates',
                y='Department',
                orientation='h',
                color_discrete_sequence=['#1E293B']
            )
            fig3.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=280)
            st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("#### Selection Rate Gauge")
        fig4 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = selection_rate,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Selection Rate (%)"},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#2563EB"},
                'steps': [
                    {'range': [0, 50], 'color': "#F1F5F9"},
                    {'range': [50, 100], 'color': "#E2E8F0"}
                ]
            }
        ))
        fig4.update_layout(margin=dict(t=30, b=20, l=20, r=20), height=280)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Recent Activities Feed
    st.markdown("### Recent Activities")

    if email_logs:
        activity_rows = []
        for l in email_logs[:8]:
            c_name = l.get("candidate_name") or l.get("candidate_id")
            action = f"Email: {l.get('subject')}"
            status = l.get("status")
            sent_time = l.get("sent_at")
            activity_rows.append({
                "Candidate": c_name,
                "Action": action,
                "Status": status,
                "Timestamp": sent_time
            })
        st.dataframe(pd.DataFrame(activity_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No activity records registered yet.")
