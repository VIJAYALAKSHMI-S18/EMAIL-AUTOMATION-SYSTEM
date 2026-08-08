import streamlit as st
import pandas as pd
from database.database import (
    get_all_candidates,
    insert_candidate,
    update_candidate,
    delete_candidate,
    upsert_candidates_bulk
)
from modules.excel_handler import (
    get_sample_excel_bytes,
    validate_excel_dataframe,
    export_candidates_to_excel
)
from modules.candidate_manager import filter_candidates, seed_sample_candidates_if_empty

def render_candidates_page():
    st.markdown("## Candidate Management")
    st.markdown("Manage candidate records, import/export via Excel, search, filter, and select candidates for automation.")

    # Ensure sample candidates exist in DB if empty
    seed_sample_candidates_if_empty()

    # Expandable Excel Section: Upload & Download
    with st.expander("Excel Management (Upload / Download Template / Export)", expanded=False):
        ex_col1, ex_col2, ex_col3 = st.columns(3)

        with ex_col1:
            st.markdown("#### 1. Download Template")
            st.markdown("Get pre-formatted `.xlsx` template with sample records.")
            sample_bytes = get_sample_excel_bytes()
            st.download_button(
                label="Download Sample Excel Template",
                data=sample_bytes,
                file_name="sample_candidates.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_download_sample"
            )

        with ex_col2:
            st.markdown("#### 2. Upload Candidate Excel")
            uploaded_file = st.file_uploader("Upload Excel file (.xlsx)", type=["xlsx"], key="uploader_excel")
            if uploaded_file is not None:
                try:
                    df_upload = pd.read_excel(uploaded_file, engine="openpyxl")
                    val_result = validate_excel_dataframe(df_upload)

                    if val_result["is_valid"]:
                        st.success("Excel uploaded and validated successfully.")
                        st.info(f"Total: {val_result['summary']['total']} | Valid: {val_result['summary']['valid']} | Invalid: {val_result['summary']['invalid']}")
                        
                        if st.button("Import Candidates to Database", key="btn_import_valid"):
                            ins, upd = upsert_candidates_bulk(val_result["valid_candidates"])
                            st.success(f"Successfully processed candidates. New inserted: {ins}, Updated: {upd}")
                            st.rerun()
                    else:
                        st.error("Excel Validation Errors Found:")
                        for err in val_result["errors"]:
                            st.write(f"- {err}")
                        if val_result["valid_candidates"]:
                            st.warning(f"Found {len(val_result['valid_candidates'])} valid candidates despite errors.")
                            if st.button("Import Only Valid Candidates", key="btn_import_partial"):
                                ins, upd = upsert_candidates_bulk(val_result["valid_candidates"])
                                st.success(f"Partial import completed. Inserted: {ins}, Updated: {upd}")
                                st.rerun()
                except Exception as e:
                    st.error(f"Failed to parse Excel file: {str(e)}")

        with ex_col3:
            st.markdown("#### 3. Export Candidates")
            st.markdown("Export current candidate database records into `.xlsx`.")
            current_cands = get_all_candidates()
            export_bytes = export_candidates_to_excel(current_cands)
            st.download_button(
                label="Export Candidates to Excel",
                data=export_bytes,
                file_name="recruitment_candidates.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="btn_export_all"
            )

    st.markdown("---")

    # Fetch fresh candidate list from database
    all_candidates = get_all_candidates()

    if not all_candidates:
        st.warning("No candidate records found in SQLite database. Upload an Excel file or click 'Download Sample Excel Template' above.")
        return

    # Search & Filter Controls
    st.markdown("### Search & Filter Candidates")
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns(5)

    with f_col1:
        search_query = st.text_input("Search (ID, Name, Email, Position)", value="", key="search_query")

    # Dynamic unique values for dropdowns
    departments = ["All"] + sorted(list(set([c.get("department") for c in all_candidates if c.get("department")])))
    positions = ["All"] + sorted(list(set([c.get("position") for c in all_candidates if c.get("position")])))
    offer_statuses = ["All", "Selected", "Pending", "Generated", "Rejected"]
    cert_statuses = ["All", "Pending", "Generated", "Issued"]

    with f_col2:
        dept_filter = st.selectbox("Department", departments, key="dept_filter")
    with f_col3:
        pos_filter = st.selectbox("Position", positions, key="pos_filter")
    with f_col4:
        offer_filter = st.selectbox("Offer Status", offer_statuses, key="offer_filter")
    with f_col5:
        cert_filter = st.selectbox("Certificate Status", cert_statuses, key="cert_filter")

    filtered_cands = filter_candidates(
        all_candidates,
        search_term=search_query,
        department=dept_filter,
        position=pos_filter,
        offer_status=offer_filter,
        cert_status=cert_filter
    )

    st.markdown(f"**Showing {len(filtered_cands)} of {len(all_candidates)} Candidates**")

    # Selection State Management
    if "selected_candidate_ids" not in st.session_state:
        st.session_state.selected_candidate_ids = set()

    # Selection Action Buttons
    sel_col1, sel_col2, sel_col3, sel_col4 = st.columns([1.5, 1.5, 2, 3])
    with sel_col1:
        if st.button("Select All Filtered", key="btn_sel_all"):
            for c in filtered_cands:
                st.session_state.selected_candidate_ids.add(c["candidate_id"])
            st.rerun()

    with sel_col2:
        if st.button("Deselect All", key="btn_desel_all"):
            st.session_state.selected_candidate_ids.clear()
            st.rerun()

    with sel_col3:
        num_selected = len(st.session_state.selected_candidate_ids)
        st.markdown(f"Selected: **{num_selected} candidates**")

    # Candidate Data Table with Selection Checkboxes
    st.markdown("### Candidate Directory")

    # Display Data Table with interactive checkboxes
    table_data = []
    for c in filtered_cands:
        is_sel = c["candidate_id"] in st.session_state.selected_candidate_ids
        table_data.append({
            "Select": is_sel,
            "Candidate ID": c["candidate_id"],
            "Name": c["name"],
            "Email": c["email"],
            "Phone": c["phone"],
            "Position": c["position"],
            "Department": c["department"],
            "Company": c["company"],
            "Joining Date": c["joining_date"],
            "Salary": f"${float(c['salary']):,.2f}",
            "Offer Status": c["offer_status"],
            "Cert Status": c["certificate_status"]
        })

    df_display = pd.DataFrame(table_data)

    # Interactive Data Editor with checkbox toggle
    edited_df = st.data_editor(
        df_display,
        column_config={
            "Select": st.column_config.CheckboxColumn("Select", default=False),
            "Salary": st.column_config.TextColumn("Salary"),
        },
        disabled=["Candidate ID", "Name", "Email", "Phone", "Position", "Department", "Company", "Joining Date", "Salary", "Offer Status", "Cert Status"],
        hide_index=True,
        key="cand_table_editor"
    )

    # Update selection set based on user toggle in data editor
    new_selected = set()
    for idx, row in edited_df.iterrows():
        if row["Select"]:
            new_selected.add(row["Candidate ID"])

    # Update session state if modified
    current_ids_in_view = set([c["candidate_id"] for c in filtered_cands])
    st.session_state.selected_candidate_ids = (st.session_state.selected_candidate_ids - current_ids_in_view) | new_selected

    st.markdown("---")

    # Add & Edit Single Candidate Section
    with st.expander("Add / Edit / Delete Candidate Record", expanded=False):
        tab_add, tab_edit, tab_del = st.tabs(["Add New Candidate", "Edit Candidate", "Delete Candidate"])

        with tab_add:
            with st.form("form_add_candidate"):
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    new_cid = st.text_input("Candidate ID *", value=f"C0{len(all_candidates)+1:02d}")
                    new_name = st.text_input("Full Name *")
                    new_email = st.text_input("Email Address *")
                with ac2:
                    new_phone = st.text_input("Phone Number")
                    new_pos = st.text_input("Position *")
                    new_dept = st.text_input("Department *")
                with ac3:
                    new_comp = st.text_input("Company *", value="ABC Technologies")
                    new_jdate = st.text_input("Joining Date (YYYY-MM-DD) *", value="2026-09-01")
                    new_sal = st.number_input("Salary *", value=50000.0, step=1000.0)

                submit_add = st.form_submit_button("Save Candidate")
                if submit_add:
                    if not new_cid or not new_name or not new_email or not new_pos or not new_dept:
                        st.error("Please fill in all required fields (*)")
                    else:
                        try:
                            insert_candidate({
                                "Candidate_ID": new_cid,
                                "Name": new_name,
                                "Email": new_email,
                                "Phone": new_phone,
                                "Position": new_pos,
                                "Department": new_dept,
                                "Company": new_comp,
                                "Joining_Date": new_jdate,
                                "Salary": new_sal,
                                "Offer_Status": "Selected",
                                "Certificate_Status": "Pending"
                            })
                            st.success(f"Candidate '{new_name}' ({new_cid}) added successfully.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to add candidate: {str(e)}")

        with tab_edit:
            selected_edit_cid = st.selectbox(
                "Select Candidate to Edit",
                options=[c["candidate_id"] for c in all_candidates],
                key="select_edit_cid"
            )
            cand_to_edit = next((c for c in all_candidates if c["candidate_id"] == selected_edit_cid), None)
            if cand_to_edit:
                with st.form("form_edit_candidate"):
                    ec1, ec2, ec3 = st.columns(3)
                    with ec1:
                        e_name = st.text_input("Name", value=cand_to_edit["name"])
                        e_email = st.text_input("Email", value=cand_to_edit["email"])
                        e_phone = st.text_input("Phone", value=cand_to_edit["phone"])
                    with ec2:
                        e_pos = st.text_input("Position", value=cand_to_edit["position"])
                        e_dept = st.text_input("Department", value=cand_to_edit["department"])
                        e_comp = st.text_input("Company", value=cand_to_edit["company"])
                    with ec3:
                        e_jdate = st.text_input("Joining Date", value=cand_to_edit["joining_date"])
                        e_sal = st.number_input("Salary", value=float(cand_to_edit["salary"]))
                        e_offer = st.selectbox("Offer Status", ["Selected", "Pending", "Generated", "Rejected"], index=["Selected", "Pending", "Generated", "Rejected"].index(cand_to_edit["offer_status"]) if cand_to_edit["offer_status"] in ["Selected", "Pending", "Generated", "Rejected"] else 0)

                    submit_edit = st.form_submit_button("Update Candidate")
                    if submit_edit:
                        update_candidate(selected_edit_cid, {
                            "name": e_name,
                            "email": e_email,
                            "phone": e_phone,
                            "position": e_pos,
                            "department": e_dept,
                            "company": e_comp,
                            "joining_date": e_jdate,
                            "salary": e_sal,
                            "offer_status": e_offer
                        })
                        st.success(f"Candidate {selected_edit_cid} updated successfully.")
                        st.rerun()

        with tab_del:
            selected_del_cid = st.selectbox(
                "Select Candidate to Delete",
                options=[c["candidate_id"] for c in all_candidates],
                key="select_del_cid"
            )
            if st.button("Delete Candidate", key="btn_del_candidate"):
                delete_candidate(selected_del_cid)
                st.success(f"Candidate {selected_del_cid} deleted.")
                st.rerun()
