import streamlit as st
import pandas as pd
from database.database import get_all_notifications

def render_notifications_page():
    st.markdown("## Notification Center & Activity Alerts")
    st.markdown("Real-time audit log of system events, email campaign dispatches, document creations, and Excel data imports.")

    notifications = get_all_notifications()

    if not notifications:
        st.info("No system notifications recorded yet.")
        return

    n_col1, n_col2 = st.columns(2)
    with n_col1:
        cat_filter = st.selectbox("Filter Category", ["All", "Success", "Warning", "Info"])
    with n_col2:
        search_filter = st.text_input("Search Notifications", value="")

    filtered = notifications
    if cat_filter != "All":
        filtered = [n for n in filtered if n["category"] == cat_filter]
    if search_filter:
        term = search_filter.lower()
        filtered = [n for n in filtered if term in n["title"].lower() or term in n["message"].lower()]

    st.markdown(f"**Showing {len(filtered)} Notifications**")

    for n in filtered:
        title = n["title"]
        msg = n["message"]
        cat = n["category"]
        created_at = n["created_at"]

        with st.container():
            col_info, col_cat = st.columns([5, 1])

            with col_info:
                st.markdown(f"**{title}**")
                st.write(msg)
                st.caption(f"Time: {created_at}")

            with col_cat:
                if cat == "Success":
                    st.success("Success")
                elif cat == "Warning":
                    st.warning("Warning")
                else:
                    st.info("Info")

            st.divider()
