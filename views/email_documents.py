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
    save_email_template,
    save_document_record
)
from modules.email_templates import get_email_preview
from modules.email_sender import process_email_dispatch
from modules.document_generator import generate_offer_letter, generate_certificate, OFFER_DIR, CERT_DIR

def render_email_documents_page():
    st.markdown("## Email & Document Studio")
    st.markdown("Generate candidate documents and dispatch personalized email campaigns in one seamless workflow.")

    all_candidates = get_all_candidates()
    if not all_candidates:
        st.warning("No candidates found. Please add or import candidates first.")
        return

    # Selected candidate summary
    selected_ids = list(st.session_state.get("selected_candidate_ids", set()))
    selected_candidates = [c for c in all_candidates if c["candidate_id"] in selected_ids]

    tab_send, tab_docs = st.tabs(["📧 Email Campaign Dispatch", "📄 Generated Document Archives"])

    # Tab 1: Email Campaign Dispatch
    with tab_send:
        # Step 1: Target Candidates
        st.markdown("### 1. Select Target Recipients")
        sc_col1, sc_col2 = st.columns([3, 1])
        with sc_col1:
            st.info(f"Targeting **{len(selected_candidates)} candidate(s)** (from Candidates Directory)")
        with sc_col2:
            if st.button("Select All Candidates", key="studio_sel_all"):
                st.session_state.selected_candidate_ids = set([c["candidate_id"] for c in all_candidates])
                st.rerun()

        st.markdown("---")

        # Step 2: Email Composer & Template Binder
        st.markdown("### 2. Compose Email & Choose Attachments")
        templates = get_all_templates()
        template_names = [t["template_name"] for t in templates]

        c_col1, c_col2 = st.columns(2)
        with c_col1:
            selected_t_name = st.selectbox("Email Template", template_names, key="studio_template_name")
            active_template = next((t for t in templates if t["template_name"] == selected_t_name), templates[0])
            subject_input = st.text_input("Subject Line", value=active_template["subject"], key="studio_subject")

        with c_col2:
            attachment_choice = st.selectbox(
                "Document Package to Attach",
                ["Both", "Offer Letter", "Certificate", "None"],
                help="Automatically generates Word & PDF files if not generated yet."
            )

        body_input = st.text_area("Email Content", value=active_template["body"], height=160, key="studio_body")

        if st.button("Save Template Changes", key="studio_save_t"):
            save_email_template(selected_t_name, subject_input, body_input)
            st.toast(f"Template '{selected_t_name}' saved.", icon="✅")

        st.markdown("---")

        # Step 3: Live Preview & Dispatch
        st.markdown("### 3. Live Preview & Dispatch")
        if not selected_candidates:
            st.warning("Please select at least one candidate above to preview and send.")
        else:
            prev_cand_id = st.selectbox(
                "Preview Candidate",
                options=[c["candidate_id"] for c in selected_candidates],
                format_func=lambda cid: f"{cid} - {next((c['name'] for c in selected_candidates if c['candidate_id'] == cid), '')}"
            )
            cand_preview = next((c for c in selected_candidates if c["candidate_id"] == prev_cand_id), selected_candidates[0])
            preview_data = get_email_preview(subject_input, body_input, cand_preview, attachment_choice)

            with st.container():
                st.markdown(f"**To:** {preview_data['recipient_name']} &lt;{preview_data['recipient_email']}&gt;")
                st.markdown(f"**Subject:** {preview_data['subject']}")
                st.text_area("Preview Body", value=preview_data['body'], height=120, disabled=True)
                st.caption(f"Attachments: {', '.join(preview_data['attachments']) if preview_data['attachments'] else 'None'}")

            st.markdown("<br>", unsafe_allow_html=True)
            email_mode = get_setting("email_mode", "Demo Mode")
            confirm_send = st.checkbox(f"Confirm sending emails to {len(selected_candidates)} candidates in {email_mode}.", key="chk_studio_send")

            if st.button("Send Email Campaign 🚀", type="primary", disabled=not confirm_send, key="btn_studio_send"):
                p_bar = st.progress(0)
                status_txt = st.empty()

                def update_p(curr, tot):
                    p_bar.progress(curr / tot)
                    status_txt.text(f"Sending email {curr} of {tot}...")

                results = process_email_dispatch(
                    selected_candidates,
                    subject_input,
                    body_input,
                    attachment_option=attachment_choice,
                    progress_callback=update_p
                )

                status_txt.text("Campaign execution completed!")
                successes = [r for r in results if r["status"] == "SUCCESS"]
                if successes:
                    st.toast(f"Dispatched {len(successes)} email(s) successfully!", icon="✅")
                    st.success(f"Dispatched {len(successes)} email(s).")
                st.rerun()

    # Tab 2: Document Generator Archives
    with tab_docs:
        st.markdown("### Document Generator & Download Archives")
        doc_col1, doc_col2 = st.columns([2, 1])
        with doc_col1:
            doc_package = st.radio("Generate Documents For Selected Candidates", ["Both", "Offer Letter", "Certificate"], horizontal=True)
        with doc_col2:
            if st.button("Generate Files Now", type="primary", key="btn_doc_gen"):
                if not selected_candidates:
                    st.error("Select candidates first.")
                else:
                    for cand in selected_candidates:
                        c_id = cand["candidate_id"]
                        if doc_package in ["Offer Letter", "Both"]:
                            fn, fp = generate_offer_letter(cand)
                            save_document_record(c_id, "Offer Letter", fn, fp)
                        if doc_package in ["Certificate", "Both"]:
                            fn, fp = generate_certificate(cand)
                            save_document_record(c_id, "Certificate", fn, fp)
                    st.toast("Documents generated!", icon="✅")
                    st.rerun()

        st.markdown("---")

        from database.database import get_all_documents
        docs = get_all_documents()
        if not docs:
            st.info("No documents generated yet.")
        else:
            st.markdown(f"**Archived Document Files ({len(docs)})**")
            for d in docs:
                c1, c2, c3, c4 = st.columns([3, 2, 2, 2])
                c_name = d["candidate_name"]
                c_id = d["candidate_id"]
                d_type = d["document_type"]
                f_name = d["file_name"]
                pdf_name = f_name.replace(".docx", ".pdf")
                target_dir = OFFER_DIR if d_type == "Offer Letter" else CERT_DIR

                with c1:
                    st.markdown(f"**{d_type}** — {c_name} (`{c_id}`)")
                with c2:
                    st.caption(d["generated_at"])
                with c3:
                    docx_p = target_dir / f_name
                    if docx_p.exists():
                        with open(docx_p, "rb") as f:
                            st.download_button("Download .docx", data=f.read(), file_name=f_name, key=f"dl_docx_{d['id']}")
                with c4:
                    pdf_p = target_dir / pdf_name
                    if pdf_p.exists():
                        with open(pdf_p, "rb") as f:
                            st.download_button("Download .pdf", data=f.read(), file_name=pdf_name, key=f"dl_pdf_{d['id']}")
                st.divider()
