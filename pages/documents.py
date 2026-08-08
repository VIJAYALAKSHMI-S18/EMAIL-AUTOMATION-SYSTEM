import streamlit as st
from pathlib import Path
from database.database import (
    get_all_candidates,
    get_all_documents,
    save_document_record
)
from modules.document_generator import generate_offer_letter, generate_certificate

def render_documents_page():
    st.markdown("## Document Generation")
    st.markdown("Generate personalized `.docx` Offer Letters and Certificates for selected candidates.")

    all_candidates = get_all_candidates()

    if not all_candidates:
        st.warning("No candidates available. Please add candidates in Candidate Management first.")
        return

    # Check candidate selection in session state
    selected_ids = list(st.session_state.get("selected_candidate_ids", set()))
    selected_candidates = [c for c in all_candidates if c["candidate_id"] in selected_ids]

    st.markdown("### 1. Select Target Candidates")
    doc_sel_col1, doc_sel_col2 = st.columns([3, 1])

    with doc_sel_col1:
        st.info(f"Currently selected: **{len(selected_candidates)} candidates** (from Candidates page)")
        if selected_candidates:
            cand_names = [f"{c['candidate_id']} - {c['name']} ({c['position']})" for c in selected_candidates]
            st.write("Target Candidates: " + ", ".join(cand_names))

    with doc_sel_col2:
        if st.button("Select All Candidates", key="doc_btn_sel_all"):
            st.session_state.selected_candidate_ids = set([c["candidate_id"] for c in all_candidates])
            st.rerun()

    st.markdown("---")

    # Document Generation Controls
    st.markdown("### 2. Choose Document Type & Generate")
    g_col1, g_col2 = st.columns(2)

    with g_col1:
        doc_type_choice = st.radio(
            "Document Type",
            ["Offer Letter", "Certificate", "Both"],
            help="Choose document(s) to generate for target candidate(s)"
        )

    with g_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Generate Documents Now", type="primary", key="btn_gen_docs"):
            if not selected_candidates:
                st.error("Please select at least one candidate first.")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                total = len(selected_candidates)
                success_count = 0

                for idx, cand in enumerate(selected_candidates):
                    c_id = cand["candidate_id"]
                    status_text.text(f"Generating documents for {cand['name']} ({c_id})...")

                    try:
                        if doc_type_choice in ["Offer Letter", "Both"]:
                            fname, fpath = generate_offer_letter(cand)
                            save_document_record(c_id, "Offer Letter", fname, fpath)

                        if doc_type_choice in ["Certificate", "Both"]:
                            fname, fpath = generate_certificate(cand)
                            save_document_record(c_id, "Certificate", fname, fpath)

                        success_count += 1
                    except Exception as e:
                        st.error(f"Failed to generate for {c_id}: {str(e)}")

                    progress_bar.progress((idx + 1) / total)

                status_text.text("Generation complete!")
                st.success(f"Generated documents for {success_count} candidate(s) successfully.")
                st.rerun()

    st.markdown("---")

    # Generated Documents Directory Table
    st.markdown("### Generated Document Archives")
    all_docs = get_all_documents()

    if not all_docs:
        st.info("No documents generated yet. Select candidates and click 'Generate Documents Now' above.")
        return

    # Filter Document Logs
    d_fcol1, d_fcol2 = st.columns(2)
    with d_fcol1:
        doc_filter_type = st.selectbox("Filter Document Type", ["All", "Offer Letter", "Certificate"])
    with d_fcol2:
        doc_search_cand = st.text_input("Filter Candidate Name / ID", value="")

    filtered_docs = all_docs
    if doc_filter_type != "All":
        filtered_docs = [d for d in filtered_docs if d["document_type"] == doc_filter_type]
    if doc_search_cand:
        term = doc_search_cand.lower()
        filtered_docs = [d for d in filtered_docs if term in d["candidate_id"].lower() or term in d["candidate_name"].lower()]

    st.markdown(f"**Total Archived Files: {len(filtered_docs)}**")

    # Document File Download Rows
    for doc_item in filtered_docs:
        doc_id = doc_item["id"]
        c_id = doc_item["candidate_id"]
        c_name = doc_item["candidate_name"]
        doc_type = doc_item["document_type"]
        f_name = doc_item["file_name"]
        f_path = Path(doc_item["file_path"])
        gen_at = doc_item["generated_at"]
        status = doc_item["status"]

        with st.container():
            col_info, col_status, col_dl = st.columns([5, 3, 2])

            with col_info:
                st.markdown(f"**{doc_type}** | **{c_name}** (`{c_id}`)")
                st.caption(f"Filename: `{f_name}` | Generated: {gen_at}")

            with col_status:
                st.markdown(f"Status: **{status}**")

            with col_dl:
                if f_path.exists():
                    with open(f_path, "rb") as f:
                        st.download_button(
                            label="Download .docx",
                            data=f.read(),
                            file_name=f_name,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"dl_btn_{doc_id}"
                        )
                else:
                    st.warning("File missing")

            st.divider()
