import sys
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from database.database import (
    get_all_candidates,
    get_all_templates,
    get_setting,
    save_email_template
)
from modules.email_templates import get_email_preview
from modules.email_sender import process_email_dispatch

def render_email_automation_page():
    st.markdown("## Email Campaign Automation")
    st.markdown("Compose personalized recruitment emails, preview rendered content per candidate, attach documents, and launch bulk campaigns.")

    all_candidates = get_all_candidates()

    if not all_candidates:
        st.warning("No candidates available. Please add or import candidates first.")
        return

    # Fetch selected candidates
    selected_ids = list(st.session_state.get("selected_candidate_ids", set()))
    selected_candidates = [c for c in all_candidates if c["candidate_id"] in selected_ids]

    # Email Mode Notice
    email_mode = get_setting("email_mode", "Demo Mode")
    if email_mode == "Demo Mode":
        st.info("Active Mode: Demo Mode (Emails will be simulated and logged into SQLite. No actual SMTP connection will be opened). You can switch to Gmail SMTP in Settings.")
    else:
        st.warning("Active Mode: Gmail SMTP (Live emails will be dispatched to candidate email addresses via Gmail SMTP).")

    # Step 1: Candidate Selection Summary
    st.markdown("### 1. Select Campaign Recipients")
    rec_col1, rec_col2 = st.columns([3, 1])

    with rec_col1:
        st.write(f"Target Recipients: **{len(selected_candidates)} candidate(s) selected**")
        if selected_candidates:
            c_summary = [f"{c['name']} ({c['email']})" for c in selected_candidates]
            st.caption("Selected: " + ", ".join(c_summary))

    with rec_col2:
        if st.button("Select All Candidates", key="em_btn_sel_all"):
            st.session_state.selected_candidate_ids = set([c["candidate_id"] for c in all_candidates])
            st.rerun()

    st.markdown("---")

    # Step 2: Email Template Selection & Composer
    st.markdown("### 2. Compose Email")

    templates = get_all_templates()
    template_names = [t["template_name"] for t in templates]

    selected_t_name = st.selectbox("Predefined Email Template", template_names, key="sel_template_name")
    active_template = next((t for t in templates if t["template_name"] == selected_t_name), templates[0])

    # SaaS Composer Container
    with st.container():
        subject_input = st.text_input("Subject Line", value=active_template["subject"], key="em_subject_input")
        body_input = st.text_area("Email Body Content", value=active_template["body"], height=200, key="em_body_input")

    # Placeholder Reference Guide
    with st.expander("Available Personalization Placeholders", expanded=False):
        st.markdown("""
        Use dynamic placeholders in your subject line and email body (substituted per candidate):
        - `{{name}}` or `{Name}` : Candidate's Full Name
        - `{{candidate_id}}` or `{Candidate_ID}` : Candidate ID
        - `{{email}}` or `{Email}` : Recipient Email Address
        - `{{position}}` or `{Position}` : Position Title
        - `{{department}}` or `{Department}` : Department
        - `{{company}}` or `{Company}` : Company Name
        - `{{joining_date}}` or `{Joining_Date}` : Proposed Joining Date
        - `{{salary}}` or `{Salary}` : Formatted Salary
        """)

    if st.button("Save Template Changes", key="btn_save_template"):
        save_email_template(selected_t_name, subject_input, body_input)
        st.toast(f"Template '{selected_t_name}' updated successfully.", icon="✅")

    st.markdown("---")

    # Step 3: Attachments Selector
    st.markdown("### 3. Document Attachments")
    attachment_choice = st.radio(
        "Attach Personalized Candidate Document(s)",
        ["None", "Offer Letter", "Certificate", "Both"],
        index=3,
        help="Each candidate receives ONLY their own personalized document(s). Files auto-generate if missing."
    )

    st.markdown("---")

    # Step 4: Candidate Live Email Preview Modal / Panel
    st.markdown("### 4. Email Preview Panel")
    
    if not selected_candidates:
        st.warning("Select candidates above to preview personalized email output.")
    else:
        preview_cand_id = st.selectbox(
            "Select Candidate to Preview",
            options=[c["candidate_id"] for c in selected_candidates],
            format_func=lambda cid: f"{cid} - {next((c['name'] for c in selected_candidates if c['candidate_id'] == cid), '')}"
        )
        cand_for_preview = next((c for c in selected_candidates if c["candidate_id"] == preview_cand_id), selected_candidates[0])

        preview_data = get_email_preview(subject_input, body_input, cand_for_preview, attachment_choice)

        st.markdown(f"""
        <div class="exec-card">
            <div style="border-bottom: 1px solid var(--card-border); padding-bottom: 10px; margin-bottom: 12px;">
                <span class="badge badge-info">EMAIL PREVIEW</span>
            </div>
            <p><strong>To:</strong> {preview_data['recipient_name']} &lt;{preview_data['recipient_email']}&gt;</p>
            <p><strong>Subject:</strong> {preview_data['subject']}</p>
            <hr style="border: 0.5px solid var(--card-border);" />
            <pre style="white-space: pre-wrap; font-family: inherit; margin: 0; color: var(--text-primary);">{preview_data['body']}</pre>
            <hr style="border: 0.5px solid var(--card-border);" />
            <p><strong>Attachments:</strong> {', '.join([f'📎 {a}' for a in preview_data['attachments']]) if preview_data['attachments'] else 'None'}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Step 5: Send Campaign Section with Confirmation Modal
    st.markdown("### 5. Launch Email Campaign")

    if not selected_candidates:
        st.error("Please select target candidates before launching campaign.")
        return

    st.warning(f"Confirmation: You are about to send personalized emails to **{len(selected_candidates)} candidates**.")

    confirm_check = st.checkbox(f"I confirm that I want to send emails to {len(selected_candidates)} candidates in {email_mode}.", key="chk_confirm_send")

    if st.button("Confirm & Send Email 🚀", type="primary", disabled=not confirm_check, key="btn_send_campaign"):
        progress_bar = st.progress(0)
        status_box = st.empty()

        def update_progress(current, total):
            progress_bar.progress(current / total)
            status_box.text(f"Processing email {current} of {total}...")

        results = process_email_dispatch(
            selected_candidates,
            subject_input,
            body_input,
            attachment_option=attachment_choice,
            progress_callback=update_progress
        )

        status_box.text("Campaign execution completed!")

        successes = [r for r in results if r["status"] == "SUCCESS"]
        failures = [r for r in results if r["status"] == "FAILED"]

        if successes:
            st.toast(f"Dispatched {len(successes)} email(s) successfully!", icon="✅")
            st.success(f"Successfully dispatched/logged {len(successes)} email(s).")
        if failures:
            st.error(f"Failed to dispatch {len(failures)} email(s). Check Email Logs for failure details.")

        st.rerun()
