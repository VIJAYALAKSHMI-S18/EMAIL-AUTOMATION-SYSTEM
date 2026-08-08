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

    # Campaigns table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_name TEXT NOT NULL,
        template_name TEXT NOT NULL,
        recipient_count INTEGER NOT NULL,
        status TEXT DEFAULT 'Draft',
        scheduled_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notifications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        category TEXT NOT NULL,
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
    """Seed initial settings, templates, and notifications if empty."""
    cursor = conn.cursor()

    # Default Settings
    default_settings = [
        ("email_mode", "Demo Mode"),
        ("sender_email", "hr@abctechnologies.com"),
        ("company_name", "ABC Technologies"),
        ("hr_name", "Recruitment Team"),
        ("hr_email", "hr@abctechnologies.com"),
        ("company_address", "Tech Park, Innovation Way, Suite 500"),
        ("admin_email", "admin@abctechnologies.com"),
        ("admin_password", "admin123"),
        ("confirm_before_send", "True"),
        ("save_email_history", "True"),
        ("auto_gen_docs", "False"),
        ("show_notifications", "True")
    ]
    for key, val in default_settings:
        cursor.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (key, val))

    # Extended Default Email Templates (supporting both {{placeholder}} and {Placeholder})
    default_templates = [
        (
            "Selection / Offer Email",
            "Congratulations! Your Selection for {{position}} at {{company}}",
            "Dear {{name}},\n\nCongratulations!\n\nWe are pleased to inform you that you have been selected for the position of {{position}} in the {{department}} department at {{company}}.\n\nJoining Date: {{joining_date}}\n\nPlease review your attached Offer Letter and confirm your acceptance.\n\nRegards,\nHR Team\n{{company}}"
        ),
        (
            "Interview Invitation",
            "Interview Invitation for {{position}} Position at {{company}}",
            "Dear {{name}},\n\nThank you for applying for the {{position}} role in our {{department}} department at {{company}}.\n\nWe would like to invite you for a formal interview session.\n\nPlease reply with your availability for the coming week.\n\nBest regards,\nHR Team\n{{company}}"
        ),
        (
            "Rejection Email",
            "Update regarding your application for {{position}} at {{company}}",
            "Dear {{name}},\n\nThank you for taking the time to interview for the {{position}} role at {{company}}.\n\nAfter careful consideration, we regret to inform you that we have decided to move forward with another candidate whose background more closely aligns with our current needs.\n\nWe wish you all the best in your job search.\n\nRegards,\nRecruitment Team\n{{company}}"
        ),
        (
            "Internship Email",
            "Internship Offer - {{position}} at {{company}}",
            "Dear {{name}},\n\nWe are excited to offer you an internship position as {{position}} in the {{department}} team at {{company}}.\n\nStart Date: {{joining_date}}\n\nWelcome aboard!\n\nRegards,\nHR Team\n{{company}}"
        ),
        (
            "Certificate Email",
            "Selection Certificate - {{company}}",
            "Dear {{name}},\n\nPlease find attached your official Selection Certificate for the {{position}} role at {{company}}.\n\nCongratulations once again on your selection.\n\nRegards,\nHR Team\n{{company}}"
        ),
        (
            "Joining Instructions",
            "Joining Instructions & Onboarding Guide - {{company}}",
            "Dear {{name}},\n\nWelcome to {{company}}! As your joining date of {{joining_date}} approaches, please find below important onboarding instructions for your role as {{position}}.\n\nPlease bring your ID proof and educational certificates on your first day.\n\nBest regards,\nHR Department\n{{company}}"
        )
    ]
    for t_name, t_sub, t_body in default_templates:
        cursor.execute(
            "INSERT OR IGNORE INTO email_templates (template_name, subject, body) VALUES (?, ?, ?)",
            (t_name, t_sub, t_body)
        )

    # Default Notifications if empty
    cursor.execute("SELECT COUNT(*) FROM notifications")
    if cursor.fetchone()[0] == 0:
        notifications_data = [
            ("System Ready", "Recruitment Email Automation Portal initialized successfully.", "Success"),
            ("Sample Candidates Loaded", "10 initial sample candidate records imported.", "Info"),
            ("Demo Mode Active", "Emails are currently running in simulated Demo Mode.", "Warning")
        ]
        for title, msg, cat in notifications_data:
            cursor.execute("INSERT INTO notifications (title, message, category) VALUES (?, ?, ?)", (title, msg, cat))

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
    add_notification("New Candidate Added", f"Added candidate {data['Name']} ({data['Candidate_ID']}).", "Success")

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
    add_notification("Excel Upload Completed", f"Imported {inserted_count + updated_count} candidates from Excel.", "Success")
    return inserted_count, updated_count

def save_document_record(candidate_id, doc_type, file_name, file_path):
    """Record document generation event."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO documents (candidate_id, document_type, file_name, file_path, status)
        VALUES (?, ?, ?, ?, 'Generated')
    """, (candidate_id, doc_type, file_name, file_path))
    
    if doc_type == "Offer Letter":
        cursor.execute("UPDATE candidates SET offer_status = 'Generated' WHERE candidate_id = ?", (candidate_id,))
    elif doc_type == "Certificate":
        cursor.execute("UPDATE candidates SET certificate_status = 'Generated' WHERE candidate_id = ?", (candidate_id,))
        
    conn.commit()
    conn.close()

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

def add_notification(title, message, category="Info"):
    """Record a system notification alert."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (title, message, category) VALUES (?, ?, ?)", (title, message, category))
    conn.commit()
    conn.close()

def get_all_notifications():
    """Fetch all notification records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT 50")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def save_campaign(campaign_name, template_name, recipient_count, status="Completed", scheduled_at=None):
    """Record email campaign."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO campaigns (campaign_name, template_name, recipient_count, status, scheduled_at)
        VALUES (?, ?, ?, ?, ?)
    """, (campaign_name, template_name, recipient_count, status, scheduled_at))
    conn.commit()
    conn.close()
    add_notification("Campaign Triggered", f"Campaign '{campaign_name}' ({recipient_count} recipients) marked as {status}.", "Success" if status == "Completed" else "Info")

def get_all_campaigns():
    """Fetch all recorded campaigns."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
