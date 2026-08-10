import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import plotly.express as px
import pandas as pd
from database.database import (
    get_all_candidates,
    get_all_email_logs
)
from utils.theme import get_current_theme, get_plotly_layout_params
from modules.email_sender import retry_single_email_log

def render_analytics_logs_page():
    st.markdown("## Analytics & Email Logs")
    st.markdown("Visual reports on candidate status, department breakdowns, and complete email dispatch history.")

    tab_charts, tab_logs = st.tabs(["📊 Hiring Visual Reports", "📜 Email Audit History"])

    # Tab 1: Charts
    with tab_charts:
        candidates = get_all_candidates()
        if not candidates:
            st.info("No candidates available for visual reporting.")
        else:
            cand_df = pd.DataFrame(candidates)
            theme = get_current_theme()
            layout_p = get_plotly_layout_params(theme)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Candidate Status Breakdown")
                status_counts = cand_df['offer_status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig1 = px.pie(status_counts, values='Count', names='Status', hole=0.4)
                fig1.update_layout(template=layout_p["template"], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=layout_p["font"], height=280)
                st.plotly_chart(fig1, use_container_width=True)

            with c2:
                st.markdown("#### Candidates by Department")
                dept_counts = cand_df['department'].value_counts().reset_index()
                dept_counts.columns = ['Department', 'Count']
                fig2 = px.bar(dept_counts, x='Count', y='Department', orientation='h')
                fig2.update_layout(template=layout_p["template"], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=layout_p["font"], height=280)
                st.plotly_chart(fig2, use_container_width=True)

    # Tab 2: Logs & Retry
    with tab_logs:
        logs = get_all_email_logs()
        if not logs:
            st.info("No email history logs recorded yet.")
        else:
            status_filter = st.selectbox("Filter Status", ["All", "SUCCESS", "FAILED", "PENDING"], key="al_status_filter")
            filtered_logs = logs if status_filter == "All" else [l for l in logs if l["status"] == status_filter]

            st.markdown(f"**Total Logs: {len(filtered_logs)}**")

            for item in filtered_logs:
                lc1, lc2, lc3 = st.columns([5, 3, 2])
                with lc1:
                    st.markdown(f"**{item.get('candidate_name', 'Unknown')}** (`{item['candidate_id']}`)")
                    st.caption(f"To: {item['recipient_email']} | Subject: {item['subject']}")
                    if item.get("error_message"):
                        st.error(item["error_message"])
                with lc2:
                    if item["status"] == "SUCCESS":
                        st.success("SUCCESS")
                    elif item["status"] == "FAILED":
                        st.error("FAILED")
                    else:
                        st.warning("PENDING")
                    st.caption(item["sent_at"])
                with lc3:
                    if item["status"] == "FAILED":
                        if st.button("Retry Send", key=f"retry_al_{item['id']}"):
                            succ, msg = retry_single_email_log(item['id'])
                            if succ:
                                st.toast("Email resent successfully!", icon="✅")
                            else:
                                st.error(msg)
                            st.rerun()
                st.divider()
