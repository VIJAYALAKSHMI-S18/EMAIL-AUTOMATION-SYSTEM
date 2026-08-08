import pandas as pd
import re
import io
from pathlib import Path
from datetime import datetime

REQUIRED_COLUMNS = [
    "Candidate_ID",
    "Name",
    "Email",
    "Phone",
    "Position",
    "Department",
    "Company",
    "Joining_Date",
    "Salary",
    "Offer_Status",
    "Certificate_Status"
]

SAMPLE_FILE_PATH = Path(__file__).parent.parent / "sample_candidates.xlsx"

def generate_sample_excel():
    """Generate sample_candidates.xlsx with at least 10 realistic fictional records."""
    sample_data = [
        {
            "Candidate_ID": "C001",
            "Name": "Vijay Kumar",
            "Email": "candidate1@example.com",
            "Phone": "9000000001",
            "Position": "Python Developer",
            "Department": "IT",
            "Company": "ABC Technologies",
            "Joining_Date": "2026-09-01",
            "Salary": 45000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C002",
            "Name": "Priya Sharma",
            "Email": "candidate2@example.com",
            "Phone": "9000000002",
            "Position": "Data Analyst",
            "Department": "Analytics",
            "Company": "ABC Technologies",
            "Joining_Date": "2026-09-05",
            "Salary": 52000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C003",
            "Name": "Rahul Kumar",
            "Email": "candidate3@example.com",
            "Phone": "9000000003",
            "Position": "Software Engineer",
            "Department": "Engineering",
            "Company": "Apex Solutions",
            "Joining_Date": "2026-09-10",
            "Salary": 60000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C004",
            "Name": "Ananya Roy",
            "Email": "candidate4@example.com",
            "Phone": "9000000004",
            "Position": "UI/UX Designer",
            "Department": "Design",
            "Company": "Nexus Labs",
            "Joining_Date": "2026-09-12",
            "Salary": 48000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C005",
            "Name": "Karthik Raja",
            "Email": "candidate5@example.com",
            "Phone": "9000000005",
            "Position": "DevOps Engineer",
            "Department": "Infrastructure",
            "Company": "ABC Technologies",
            "Joining_Date": "2026-09-15",
            "Salary": 65000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C006",
            "Name": "Sneha Patel",
            "Email": "candidate6@example.com",
            "Phone": "9000000006",
            "Position": "HR Specialist",
            "Department": "Human Resources",
            "Company": "GlobalTech",
            "Joining_Date": "2026-09-18",
            "Salary": 42000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C007",
            "Name": "Amit Singh",
            "Email": "candidate7@example.com",
            "Phone": "9000000007",
            "Position": "QA Automation Engineer",
            "Department": "Quality Assurance",
            "Company": "Apex Solutions",
            "Joining_Date": "2026-09-20",
            "Salary": 47000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C008",
            "Name": "Deepika Das",
            "Email": "candidate8@example.com",
            "Phone": "9000000008",
            "Position": "Backend Engineer",
            "Department": "Engineering",
            "Company": "Nexus Labs",
            "Joining_Date": "2026-09-22",
            "Salary": 58000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C009",
            "Name": "Rohan Gupta",
            "Email": "candidate9@example.com",
            "Phone": "9000000009",
            "Position": "Frontend Developer",
            "Department": "Engineering",
            "Company": "Innovate Corp",
            "Joining_Date": "2026-09-25",
            "Salary": 50000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        },
        {
            "Candidate_ID": "C010",
            "Name": "Meera Nair",
            "Email": "candidate10@example.com",
            "Phone": "9000000010",
            "Position": "System Administrator",
            "Department": "IT",
            "Company": "ABC Technologies",
            "Joining_Date": "2026-09-28",
            "Salary": 46000,
            "Offer_Status": "Selected",
            "Certificate_Status": "Pending"
        }
    ]

    df = pd.DataFrame(sample_data)
    df.to_excel(SAMPLE_FILE_PATH, index=False, engine="openpyxl")
    return SAMPLE_FILE_PATH

def get_sample_excel_bytes():
    """Return bytes of sample excel file for downloading."""
    if not SAMPLE_FILE_PATH.exists():
        generate_sample_excel()
    with open(SAMPLE_FILE_PATH, "rb") as f:
        return f.read()

def validate_email_format(email):
    """Validate email address format using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, str(email).strip()))

def validate_excel_dataframe(df):
    """
    Validate uploaded Excel DataFrame.
    Returns dictionary with:
    - is_valid: bool
    - errors: list of error strings
    - missing_columns: list of missing column names
    - valid_candidates: list of candidate dicts ready for insertion
    - summary: stats dict
    """
    errors = []
    missing_columns = []
    valid_candidates = []

    # 1. Column presence check
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            missing_columns.append(col)

    if missing_columns:
        errors.append(f"Missing required column(s): {', '.join(missing_columns)}")
        return {
            "is_valid": False,
            "errors": errors,
            "missing_columns": missing_columns,
            "valid_candidates": [],
            "summary": {"total": len(df), "valid": 0, "invalid": len(df)}
        }

    # 2. Row by row validation
    seen_candidate_ids = set()

    for idx, row in df.iterrows():
        row_num = idx + 2  # Excel 1-indexed plus header row
        c_id = str(row.get("Candidate_ID", "")).strip()
        name = str(row.get("Name", "")).strip()
        email = str(row.get("Email", "")).strip()
        phone = str(row.get("Phone", "")).strip()
        position = str(row.get("Position", "")).strip()
        department = str(row.get("Department", "")).strip()
        company = str(row.get("Company", "")).strip()
        joining_date = str(row.get("Joining_Date", "")).strip()
        salary = row.get("Salary", 0)
        offer_status = str(row.get("Offer_Status", "Selected")).strip()
        certificate_status = str(row.get("Certificate_Status", "Pending")).strip()

        row_errors = []

        if not c_id or c_id == "nan":
            row_errors.append(f"Row {row_num}: Candidate_ID is empty")
        elif c_id in seen_candidate_ids:
            row_errors.append(f"Row {row_num}: Duplicate Candidate_ID '{c_id}' in Excel file")
        else:
            seen_candidate_ids.add(c_id)

        if not name or name == "nan":
            row_errors.append(f"Row {row_num}: Candidate Name is empty")

        if not email or email == "nan":
            row_errors.append(f"Row {row_num}: Email is empty")
        elif not validate_email_format(email):
            row_errors.append(f"Row {row_num}: Invalid email format '{email}'")

        if not position or position == "nan":
            row_errors.append(f"Row {row_num}: Position is empty")

        if not department or department == "nan":
            row_errors.append(f"Row {row_num}: Department is empty")

        if not company or company == "nan":
            row_errors.append(f"Row {row_num}: Company is empty")

        # Salary check
        try:
            val_salary = float(salary)
            if val_salary < 0:
                row_errors.append(f"Row {row_num}: Salary cannot be negative")
        except (ValueError, TypeError):
            row_errors.append(f"Row {row_num}: Invalid numerical salary '{salary}'")
            val_salary = 0.0

        # Joining Date check
        if not joining_date or joining_date == "nan":
            row_errors.append(f"Row {row_num}: Joining Date is empty")

        if row_errors:
            errors.extend(row_errors)
        else:
            valid_candidates.append({
                "Candidate_ID": c_id,
                "Name": name,
                "Email": email,
                "Phone": phone if phone != "nan" else "",
                "Position": position,
                "Department": department,
                "Company": company,
                "Joining_Date": joining_date,
                "Salary": val_salary,
                "Offer_Status": offer_status if offer_status != "nan" else "Selected",
                "Certificate_Status": certificate_status if certificate_status != "nan" else "Pending"
            })

    is_valid = len(errors) == 0 and len(valid_candidates) > 0

    return {
        "is_valid": is_valid,
        "errors": errors,
        "missing_columns": missing_columns,
        "valid_candidates": valid_candidates,
        "summary": {
            "total": len(df),
            "valid": len(valid_candidates),
            "invalid": len(df) - len(valid_candidates)
        }
    }

def export_candidates_to_excel(candidates):
    """
    Convert list of candidate dicts/rows into downloadable Excel byte buffer (.xlsx).
    """
    if not candidates:
        df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    else:
        # Standardize keys to match Excel output columns
        export_data = []
        for c in candidates:
            export_data.append({
                "Candidate_ID": c.get("candidate_id", ""),
                "Name": c.get("name", ""),
                "Email": c.get("email", ""),
                "Phone": c.get("phone", ""),
                "Position": c.get("position", ""),
                "Department": c.get("department", ""),
                "Company": c.get("company", ""),
                "Joining_Date": c.get("joining_date", ""),
                "Salary": c.get("salary", 0),
                "Offer_Status": c.get("offer_status", "Selected"),
                "Certificate_Status": c.get("certificate_status", "Pending")
            })
        df = pd.DataFrame(export_data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidates")
    output.seek(0)
    return output.getvalue()
