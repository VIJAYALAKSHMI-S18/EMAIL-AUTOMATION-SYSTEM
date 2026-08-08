import pandas as pd
from database.database import (
    get_all_candidates,
    get_candidate_by_id,
    insert_candidate,
    update_candidate,
    delete_candidate,
    upsert_candidates_bulk
)
from modules.excel_handler import SAMPLE_FILE_PATH, validate_excel_dataframe

def seed_sample_candidates_if_empty():
    """Load sample Excel data into database if database is currently empty."""
    candidates = get_all_candidates()
    if not candidates:
        if SAMPLE_FILE_PATH.exists():
            df = pd.read_excel(SAMPLE_FILE_PATH, engine="openpyxl")
            validation = validate_excel_dataframe(df)
            if validation["is_valid"] or validation["valid_candidates"]:
                upsert_candidates_bulk(validation["valid_candidates"])
                return len(validation["valid_candidates"])
    return len(candidates)

def filter_candidates(candidates, search_term="", department="All", position="All", offer_status="All", cert_status="All"):
    """Filter and search candidate list in-memory."""
    filtered = candidates

    if search_term:
        term = search_term.lower().strip()
        filtered = [
            c for c in filtered if (
                term in c.get("candidate_id", "").lower() or
                term in c.get("name", "").lower() or
                term in c.get("email", "").lower() or
                term in c.get("position", "").lower() or
                term in c.get("department", "").lower() or
                term in c.get("company", "").lower()
            )
        ]

    if department != "All":
        filtered = [c for c in filtered if c.get("department") == department]

    if position != "All":
        filtered = [c for c in filtered if c.get("position") == position]

    if offer_status != "All":
        filtered = [c for c in filtered if c.get("offer_status") == offer_status]

    if cert_status != "All":
        filtered = [c for c in filtered if c.get("certificate_status") == cert_status]

    return filtered

def get_candidate_summary():
    """Fetch statistical metrics for dashboard."""
    candidates = get_all_candidates()
    total = len(candidates)
    selected = len([c for c in candidates if c.get("offer_status") == "Selected"])
    pending_offer = len([c for c in candidates if c.get("offer_status") == "Pending"])
    rejected = len([c for c in candidates if c.get("offer_status") == "Rejected"])
    
    # Departments count
    departments = {}
    for c in candidates:
        dept = c.get("department", "Other")
        departments[dept] = departments.get(dept, 0) + 1

    # Positions count
    positions = {}
    for c in candidates:
        pos = c.get("position", "Other")
        positions[pos] = positions.get(pos, 0) + 1

    return {
        "total": total,
        "selected": selected,
        "pending_offer": pending_offer,
        "rejected": rejected,
        "departments": departments,
        "positions": positions
    }
