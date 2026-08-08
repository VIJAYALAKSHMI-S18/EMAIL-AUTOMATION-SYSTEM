import sqlite3
import os
from pathlib import Path
from datetime import datetime

# Database file path
DB_PATH = Path(__file__).parent / "recruitment.db"

def get_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Candidates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        position TEXT NOT NULL,
        department TEXT NOT NULL,
        company TEXT NOT NULL,
        joining_date TEXT NOT NULL,
        salary REAL NOT NULL,
        offer_status TEXT DEFAULT 'Pending',
        certificate_status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT NOT NULL,
        document_type TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        status TEXT DEFAULT 'Generated',
        generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
    )
    """)

    # Email logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT NOT NULL,
        recipient_email TEXT NOT NULL,
        subject TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL,
        error_message TEXT,
        attachment TEXT,
        FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE
    )
    """)

    # Email templates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_name TEXT UNIQUE NOT NULL,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    seed_default_data(conn)
    conn.close()

def seed_default_data(conn):
    """Seed initial settings and templates if empty."""
    cursor = conn.cursor()

    # Default Settings
    default_settings = [
        ("email_mode", "Demo Mode"),
        ("sender_email", "hr@abctechnologies.com"),
        ("company_name", "ABC Technologies"),
        ("hr_name", "Recruitment Team"),
        ("hr_email", "hr@abctechnologies.com"),
        ("company_address", "Tech Park, Innovation Way, Suite 500")
    ]
    for key, val in default_settings:
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, val))

    # Default Email Templates
    default_templates = [
        (
            "Selection Email",
            "Congratulations! Your Selection for {Position} at {Company}",
            "Dear {Name},\n\nCongratulations!\n\nWe are pleased to inform you that you have been selected for the position of {Position} at {Company}.\n\nYour joining date is {Joining_Date}.\n\nWe look forward to welcoming you to our organization.\n\nRegards,\nHR Team\n{Company}"
        ),
        (
            "Offer Letter",
            "Offer Letter – {Position} at {Company}",
            "Dear {Name},\n\nPlease find attached your official Offer Letter for the position of {Position} in the {Department} department at {Company}.\n\nJoining Date: {Joining_Date}\nSalary: {Salary}\n\nPlease review the attached document and return a signed copy at your earliest convenience.\n\nRegards,\nHR Team\n{Company}"
        ),
        (
            "Certificate",
            "Selection Certificate – {Company}",
            "Dear {Name},\n\nWe are pleased to present your Selection Certificate for the position of {Position} at {Company}.\n\nPlease find your official certificate attached to this email.\n\nRegards,\nHR Team\n{Company}"
        ),
        (
            "Custom Email",
            "Update regarding your application at {Company}",
            "Dear {Name},\n\nThank you for taking the time to interview with us for the {Position} position at {Company}.\n\nIf you have any questions, feel free to reply directly to this email.\n\nBest regards,\nHR Team\n{Company}"
        )
    ]
    for t_name, t_sub, t_body in default_templates:
        cursor.execute(
            "INSERT OR IGNORE INTO email_templates (template_name, subject, body) VALUES (?, ?, ?)",
            (t_name, t_sub, t_body)
        )

    conn.commit()

# --- Helper Query Functions ---

def get_setting(key, default_value=""):
    """Retrieve setting value by key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row["value"] if row else default_value

def set_setting(key, value):
    """Set or update a setting key-value pair."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def get_all_candidates():
    """Fetch all candidate records as list of dicts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_candidate_by_id(candidate_id):
    """Fetch single candidate record by candidate_id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def insert_candidate(data):
    """Insert a single candidate dict into SQLite."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates (
            candidate_id, name, email, phone, position, department, company, joining_date, salary, offer_status, certificate_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["Candidate_ID"], data["Name"], data["Email"], str(data.get("Phone", "")),
        data["Position"], data["Department"], data["Company"], str(data["Joining_Date"]),
        float(data["Salary"]), data.get("Offer_Status", "Selected"), data.get("Certificate_Status", "Pending")
    ))
    conn.commit()
    conn.close()

def update_candidate(candidate_id, updates):
    """Update candidate details."""
    conn = get_connection()
    cursor = conn.cursor()
    fields = ", ".join([f"{k} = ?" for k in updates.keys()])
    values = list(updates.values()) + [candidate_id]
    cursor.execute(f"UPDATE candidates SET {fields} WHERE candidate_id = ?", values)
    conn.commit()
    conn.close()

def delete_candidate(candidate_id):
    """Delete candidate and associated records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM candidates WHERE candidate_id = ?", (candidate_id,))
    cursor.execute("DELETE FROM documents WHERE candidate_id = ?", (candidate_id,))
    cursor.execute("DELETE FROM email_logs WHERE candidate_id = ?", (candidate_id,))
    conn.commit()
    conn.close()

def upsert_candidates_bulk(candidates_list):
    """Insert or replace candidates from Excel upload."""
    conn = get_connection()
    cursor = conn.cursor()
    inserted_count = 0
    updated_count = 0

    for data in candidates_list:
        cursor.execute("SELECT id FROM candidates WHERE candidate_id = ?", (data["Candidate_ID"],))
        exists = cursor.fetchone()
        
        cursor.execute("""
            INSERT OR REPLACE INTO candidates (
                candidate_id, name, email, phone, position, department, company, joining_date, salary, offer_status, certificate_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(data["Candidate_ID"]).strip(),
            str(data["Name"]).strip(),
            str(data["Email"]).strip(),
            str(data.get("Phone", "")).strip(),
            str(data["Position"]).strip(),
            str(data["Department"]).strip(),
            str(data["Company"]).strip(),
            str(data["Joining_Date"]).strip(),
            float(data["Salary"]),
            str(data.get("Offer_Status", "Selected")).strip(),
            str(data.get("Certificate_Status", "Pending")).strip()
        ))
        if exists:
            updated_count += 1
        else:
            inserted_count += 1

    conn.commit()
    conn.close()
    return inserted_count, updated_count

def save_document_record(candidate_id, doc_type, file_name, file_path):
    """Record document generation event."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (candidate_id, document_type, file_name, file_path, status)
        VALUES (?, ?, ?, ?, 'Generated')
    """, (candidate_id, doc_type, file_name, file_path))
    
    # Update candidate status if applicable
    if doc_type == "Offer Letter":
        cursor.execute("UPDATE candidates SET offer_status = 'Generated' WHERE candidate_id = ?", (candidate_id,))
    elif doc_type == "Certificate":
        cursor.execute("UPDATE candidates SET certificate_status = 'Generated' WHERE candidate_id = ?", (candidate_id,))
        
    conn.commit()
    conn.close()

def get_documents_by_candidate(candidate_id):
    """Fetch generated documents for a candidate."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE candidate_id = ? ORDER BY generated_at DESC", (candidate_id,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_documents():
    """Fetch all generated documents with candidate names."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT d.*, c.name as candidate_name, c.email as candidate_email
        FROM documents d
        JOIN candidates c ON d.candidate_id = c.candidate_id
        ORDER BY d.generated_at DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def log_email_send(candidate_id, recipient_email, subject, status, error_message="", attachment=""):
    """Log an email sending attempt."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO email_logs (candidate_id, recipient_email, subject, status, error_message, attachment)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (candidate_id, recipient_email, subject, status, error_message, attachment))
    conn.commit()
    conn.close()

def get_all_email_logs():
    """Fetch all email log entries."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT l.*, c.name as candidate_name
        FROM email_logs l
        LEFT JOIN candidates c ON l.candidate_id = c.candidate_id
        ORDER BY l.sent_at DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_all_templates():
    """Fetch all email templates."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_templates ORDER BY id ASC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def save_email_template(name, subject, body):
    """Save or update custom email template."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO email_templates (template_name, subject, body)
        VALUES (?, ?, ?)
    """, (name, subject, body))
    conn.commit()
    conn.close()
