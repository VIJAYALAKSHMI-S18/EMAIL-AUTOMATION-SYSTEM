import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import datetime
import pandas as pd
from database.database import (
    get_all_candidates,
    get_all_templates,
    save_campaign,
    get_all_campaigns
)
from modules.email_sender import process_email_dispatch

def render_campaigns_page():
    st.markdown("## Email Campaigns & Scheduling")
    st.markdown("Group candidate email outreach into named campaigns, attach document packages, and execute or schedule bulk sending.")

    candidates = get_all_candidates()
    templates = get_all_templates()

    if not candidates:
        st.warning("No candidate records available. Please import candidates first.")
        return

    tab_create, tab_history = st.tabs(["Create & Launch Campaign", "Campaign History & Stats"])

    with tab_create:
        with st.form("form_create_campaign"):
            st.markdown("### Campaign Configuration")
            camp_name = st.text_input("Campaign Name *", value=f"Recruitment Outreach - {datetime.date.today().strftime('%B %Y')}")
            
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                t_names = [t["template_name"] for t in templates]
                sel_template = st.selectbox("Select Email Template *", t_names)
                sel_t_obj = next((t for t in templates if t["template_name"] == sel_template), templates[0])

            with c_col2:
                attachment_option = st.selectbox(
                    "Attach Candidate Documents",
                    ["Both", "Offer Letter", "Certificate", "None"]
                )

            st.markdown("### Select Target Candidates")
            selected_ids = list(st.session_state.get("selected_candidate_ids", set()))
            st.info(f"Targeting **{len(selected_ids) if selected_ids else len(candidates)} candidates**")

            target_cands = [c for c in candidates if c["candidate_id"] in selected_ids] if selected_ids else candidates

            dispatch_mode = st.radio("Execution Option", ["Send Now", "Schedule Campaign"], horizontal=True)

            sched_time = None
            if dispatch_mode == "Schedule Campaign":
                sched_date = st.date_input("Schedule Date", value=datetime.date.today() + datetime.timedelta(days=1))
                sched_hour = st.time_input("Schedule Time", value=datetime.time(9, 0))
                sched_time = f"{sched_date} {sched_hour}"

            submit_camp = st.form_submit_button("Execute Campaign", type="primary")

            if submit_camp:
                if not camp_name:
                    st.error("Please enter a campaign name.")
                else:
                    if dispatch_mode == "Send Now":
                        progress_bar = st.progress(0)
                        status_box = st.empty()

                        def update_p(curr, tot):
                            progress_bar.progress(curr/tot)
                            status_box.text(f"Processing email {curr} of {tot}...")

                        results = process_email_dispatch(
                            target_cands,
                            sel_t_obj["subject"],
                            sel_t_obj["body"],
                            attachment_option=attachment_option,
                            progress_callback=update_p
                        )

                        save_campaign(camp_name, sel_template, len(target_cands), "Completed")
                        st.success(f"Campaign '{camp_name}' completed successfully!")
                        st.rerun()
                    else:
                        save_campaign(camp_name, sel_template, len(target_cands), "Scheduled", sched_time)
                        st.success(f"Campaign '{camp_name}' scheduled for {sched_time}!")
                        st.rerun()

    with tab_history:
        st.markdown("### Campaign History")
        campaigns = get_all_campaigns()

        if not campaigns:
            st.info("No recorded campaigns yet.")
        else:
            df_camp = pd.DataFrame(campaigns)
            st.dataframe(df_camp, use_container_width=True, hide_index=True)
