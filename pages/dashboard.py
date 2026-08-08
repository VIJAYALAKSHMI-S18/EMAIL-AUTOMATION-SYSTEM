import streamlit as st
import matplotlib.pyplot as plt
from database.database import (
    get_all_candidates,
    get_all_documents,
    get_all_email_logs,
    get_setting
)

def render_dashboard_page():
    st.markdown("## 🏠 Recruitment Executive Dashboard")
    st.markdown("Overview of candidate pipeline, generated documents, and email campaign analytics.")

    candidates = get_all_candidates()
    documents = get_all_documents()
    email_logs = get_all_email_logs()
    email_mode = get_setting("email_mode", "Demo Mode")

    # Mode Badge Notice
    if email_mode == "Demo Mode":
        st.info("ℹ️ **System Mode: Demo Mode** (Emails are simulated and logged to SQLite without sending real SMTP emails). You can switch to Gmail SMTP in Settings.")
    else:
        st.success("🟢 **System Mode: Gmail SMTP** (Live emails will be sent via Gmail SMTP).")

    # Key Metric Calculations
    total_candidates = len(candidates)
    selected_candidates = len([c for c in candidates if c.get("offer_status") == "Selected"])
    total_documents = len(documents)
    
    emails_sent = len([l for l in email_logs if l.get("status") == "SUCCESS"])
    emails_failed = len([l for l in email_logs if l.get("status") == "FAILED"])
    emails_pending = len([l for l in email_logs if l.get("status") == "PENDING"])

    # Metric Cards Layout
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Candidates", total_candidates)
    with col2:
        st.metric("Selected", selected_candidates)
    with col3:
        st.metric("Documents", total_documents)
    with col4:
        st.metric("Emails Sent", emails_sent)
    with col5:
        st.metric("Emails Failed", emails_failed)
    with col6:
        st.metric("Emails Pending", emails_pending)

    st.markdown("---")

    # Quick Summary & Action Banner
    st.markdown("### 📊 Live Recruitment Metrics")

    # Row 1: Charts
    chart_col1, chart_col2 = st.columns(2)

    # Chart 1: Candidate Status
    with chart_col1:
        st.markdown("#### Candidate Offer Status")
        if candidates:
            status_counts = {}
            for c in candidates:
                st_val = c.get("offer_status", "Pending")
                status_counts[st_val] = status_counts.get(st_val, 0) + 1

            fig1, ax1 = plt.subplots(figsize=(5, 3.5))
            colors = ['#2563EB', '#D97706', '#DC2626', '#059669']
            ax1.pie(
                status_counts.values(),
                labels=status_counts.keys(),
                autopct='%1.1f%%',
                startangle=140,
                colors=colors[:len(status_counts)],
                textprops={'fontsize': 9}
            )
            ax1.axis('equal')
            fig1.patch.set_alpha(0.0)
            st.pyplot(fig1)
        else:
            st.info("No candidate records available to plot.")

    # Chart 2: Email Logs Status
    with chart_col2:
        st.markdown("#### Email Dispatch Status")
        if email_logs:
            email_counts = {"SUCCESS": 0, "FAILED": 0, "PENDING": 0}
            for l in email_logs:
                st_val = l.get("status", "PENDING")
                email_counts[st_val] = email_counts.get(st_val, 0) + 1

            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            bars = ax2.bar(
                email_counts.keys(),
                email_counts.values(),
                color=['#059669', '#DC2626', '#D97706']
            )
            ax2.set_ylabel("Count")
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            fig2.patch.set_alpha(0.0)
            st.pyplot(fig2)
        else:
            st.info("No email campaign logs available yet.")

    st.markdown("---")

    # Row 2: Department & Position Breakdown Charts
    chart_col3, chart_col4 = st.columns(2)

    # Chart 3: Department Breakdown
    with chart_col3:
        st.markdown("#### Candidates by Department")
        if candidates:
            dept_counts = {}
            for c in candidates:
                d = c.get("department", "Other")
                dept_counts[d] = dept_counts.get(d, 0) + 1

            fig3, ax3 = plt.subplots(figsize=(5, 3.5))
            ax3.barh(list(dept_counts.keys()), list(dept_counts.values()), color='#1E293B')
            ax3.set_xlabel("Candidates")
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            fig3.patch.set_alpha(0.0)
            st.pyplot(fig3)
        else:
            st.info("No candidate data.")

    # Chart 4: Position Breakdown
    with chart_col4:
        st.markdown("#### Top Candidate Positions")
        if candidates:
            pos_counts = {}
            for c in candidates:
                p = c.get("position", "Other")
                pos_counts[p] = pos_counts.get(p, 0) + 1

            fig4, ax4 = plt.subplots(figsize=(5, 3.5))
            ax4.bar(list(pos_counts.keys()), list(pos_counts.values()), color='#2563EB')
            plt.xticks(rotation=45, ha='right', fontsize=8)
            ax4.set_ylabel("Candidates")
            ax4.spines['top'].set_visible(False)
            ax4.spines['right'].set_visible(False)
            fig4.patch.set_alpha(0.0)
            st.pyplot(fig4)
        else:
            st.info("No candidate data.")
