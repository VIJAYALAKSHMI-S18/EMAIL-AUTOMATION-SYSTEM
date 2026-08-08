import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from database.database import (
    get_all_candidates,
    get_all_email_logs,
    get_all_documents,
    get_all_campaigns
)

def render_analytics_page():
    st.markdown("## Recruitment Analytics & Reporting")
    st.markdown("In-depth statistical insights on candidate acquisition, departmental hiring, email communication success rates, and selection trends.")

    candidates = get_all_candidates()
    email_logs = get_all_email_logs()
    documents = get_all_documents()
    campaigns = get_all_campaigns()

    if not candidates:
        st.warning("No candidate data available for analytics. Upload or add candidates first.")
        return

    cand_df = pd.DataFrame(candidates)
    logs_df = pd.DataFrame(email_logs) if email_logs else pd.DataFrame()

    # Filter Bar
    st.markdown("### Filter Visualizations")
    af_col1, af_col2 = st.columns(2)

    companies = ["All"] + sorted(list(set(cand_df['company'].dropna())))
    departments = ["All"] + sorted(list(set(cand_df['department'].dropna())))

    with af_col1:
        sel_comp = st.selectbox("Company Filter", companies, key="analytics_comp")
    with af_col2:
        sel_dept = st.selectbox("Department Filter", departments, key="analytics_dept")

    filtered_df = cand_df
    if sel_comp != "All":
        filtered_df = filtered_df[filtered_df['company'] == sel_comp]
    if sel_dept != "All":
        filtered_df = filtered_df[filtered_df['department'] == sel_dept]

    st.markdown("---")

    # Metrics Summary Row
    st.markdown("### Pipeline Summary")
    m1, m2, m3, m4, m5 = st.columns(5)
    
    total_cands = len(filtered_df)
    selected_cands = len(filtered_df[filtered_df['offer_status'] == 'Selected'])
    rejected_cands = len(filtered_df[filtered_df['offer_status'] == 'Rejected'])
    pending_cands = len(filtered_df[filtered_df['offer_status'] == 'Pending'])
    
    avg_sal = filtered_df['salary'].mean() if total_cands > 0 else 0
    sel_rate = (selected_cands / total_cands * 100) if total_cands > 0 else 0

    with m1:
        st.metric("Total Candidates", total_cands)
    with m2:
        st.metric("Selected Candidates", selected_cands)
    with m3:
        st.metric("Selection Rate", f"{sel_rate:.1f}%")
    with m4:
        st.metric("Average Salary", f"${avg_sal:,.2f}")
    with m5:
        st.metric("Total Documents", len(documents))

    st.markdown("---")

    # Row 1 Plotly Charts
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Candidate Status Breakdown")
        offer_counts = filtered_df['offer_status'].value_counts().reset_index()
        offer_counts.columns = ['Status', 'Count']

        fig1 = px.pie(
            offer_counts,
            values='Count',
            names='Status',
            hole=0.4,
            color_discrete_sequence=['#2563EB', '#059669', '#D97706', '#DC2626']
        )
        fig1.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.markdown("#### Email Communication Dispatch Logs")
        if not logs_df.empty:
            email_counts = logs_df['status'].value_counts().reset_index()
            email_counts.columns = ['Status', 'Count']

            fig2 = px.bar(
                email_counts,
                x='Status',
                y='Count',
                color='Status',
                color_discrete_map={'SUCCESS': '#059669', 'FAILED': '#DC2626', 'PENDING': '#D97706'}
            )
            fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No email campaign logs recorded yet.")

    st.markdown("---")

    # Row 2 Plotly Charts
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Candidates by Department")
        dept_counts = filtered_df['department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Candidates']

        fig3 = px.bar(
            dept_counts,
            x='Candidates',
            y='Department',
            orientation='h',
            color='Candidates',
            color_continuous_scale='Blues'
        )
        fig3.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300, showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.markdown("#### Position-wise Distribution")
        pos_counts = filtered_df['position'].value_counts().reset_index()
        pos_counts.columns = ['Position', 'Count']

        fig4 = px.bar(
            pos_counts,
            x='Position',
            y='Count',
            color_discrete_sequence=['#2563EB']
        )
        fig4.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=300)
        st.plotly_chart(fig4, use_container_width=True)
