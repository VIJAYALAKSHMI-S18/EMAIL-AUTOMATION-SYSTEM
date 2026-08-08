import streamlit as st
import pandas as pd
from database.database import get_all_email_logs
from modules.email_sender import retry_single_email_log

def render_email_logs_page():
    st.markdown("## 📜 Email Audit Logs")
    st.markdown("Historical records of all email dispatch events, tracking success status, attachments, error stack traces, and resend attempts.")

    logs = get_all_email_logs()

    if not logs:
        st.info("No email dispatch logs recorded yet. Launch an email campaign in Email Automation to populate logs.")
        return

    # Filter Section
    l_col1, l_col2 = st.columns(2)
    with l_col1:
        status_filter = st.selectbox("Filter Status", ["All", "SUCCESS", "FAILED", "PENDING"], key="logs_status_filter")
    with l_col2:
        search_filter = st.text_input("Search Candidate ID / Email / Subject", value="", key="logs_search_filter")

    filtered_logs = logs
    if status_filter != "All":
        filtered_logs = [l for l in filtered_logs if l["status"] == status_filter]
    if search_filter:
        term = search_filter.lower()
        filtered_logs = [
            l for l in filtered_logs if (
                term in l.get("candidate_id", "").lower() or
                term in l.get("recipient_email", "").lower() or
                term in l.get("subject", "").lower() or
                term in str(l.get("candidate_name", "")).lower()
            )
        ]

    st.markdown(f"**Displaying {len(filtered_logs)} Log Records**")

    # Table view summary metrics
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Total Logged", len(logs))
    with col_s2:
        st.metric("Successful", len([l for l in logs if l["status"] == "SUCCESS"]))
    with col_s3:
        st.metric("Failed", len([l for l in logs if l["status"] == "FAILED"]))

    st.markdown("---")

    # Detailed Logs List with Retry Actions
    for log_item in filtered_logs:
        log_id = log_item["id"]
        c_id = log_item["candidate_id"]
        c_name = log_item.get("candidate_name", "Unknown")
        email = log_item["recipient_email"]
        subject = log_item["subject"]
        sent_at = log_item["sent_at"]
        status = log_item["status"]
        err_msg = log_item.get("error_message", "")
        attachment = log_item.get("attachment", "None")

        with st.container():
            lc_icon, lc_info, lc_status, lc_action = st.columns([1, 4, 2, 2])

            with lc_icon:
                if status == "SUCCESS":
                    st.markdown("✅")
                elif status == "FAILED":
                    st.markdown("❌")
                else:
                    st.markdown("⏳")

            with lc_info:
                st.markdown(f"**{c_name}** (`{c_id}`) &lt;`{email}`&gt;")
                st.caption(f"Subject: {subject}")
                st.caption(f"Sent: {sent_at} | Attachments: {attachment}")
                if err_msg:
                    st.error(f"Error: {err_msg}")

            with lc_status:
                if status == "SUCCESS":
                    st.success("SUCCESS")
                elif status == "FAILED":
                    st.error("FAILED")
                else:
                    st.warning("PENDING")

            with lc_action:
                if status == "FAILED":
                    if st.button(f"🔄 Retry Send", key=f"retry_btn_{log_id}"):
                        success, msg = retry_single_email_log(log_id)
                        if success:
                            st.success(f"Retry successful! {msg}")
                        else:
                            st.error(f"Retry failed: {msg}")
                        st.rerun()

            st.divider()
