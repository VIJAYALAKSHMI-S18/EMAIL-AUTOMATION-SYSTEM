import os
import smtplib
import time
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

from database.database import get_setting, log_email_send, add_notification
from modules.email_templates import personalize_text
from modules.document_generator import generate_offer_letter, generate_certificate, OFFER_DIR, CERT_DIR

load_dotenv()

def get_smtp_credentials():
    """Retrieve SMTP email credentials."""
    email_address = os.getenv("EMAIL_ADDRESS") or get_setting("sender_email", "")
    email_password = os.getenv("EMAIL_PASSWORD") or get_setting("sender_password", "")

    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            if "EMAIL_ADDRESS" in st.secrets:
                email_address = st.secrets["EMAIL_ADDRESS"]
            if "EMAIL_PASSWORD" in st.secrets:
                email_password = st.secrets["EMAIL_PASSWORD"]
    except Exception:
        pass

    return email_address, email_password

def resolve_candidate_attachments(candidate_data, attachment_option):
    """
    Resolve attachment file paths (.docx and .pdf). Auto-generate if missing.
    """
    c_id = candidate_data.get("candidate_id", "")
    attachment_paths = []

    if attachment_option in ["Offer Letter", "Both"]:
        offer_docx = OFFER_DIR / f"{c_id}_Offer_Letter.docx"
        offer_pdf = OFFER_DIR / f"{c_id}_Offer_Letter.pdf"
        if not offer_docx.exists() or not offer_pdf.exists():
            generate_offer_letter(candidate_data)
        if offer_pdf.exists():
            attachment_paths.append(offer_pdf)
        elif offer_docx.exists():
            attachment_paths.append(offer_docx)

    if attachment_option in ["Certificate", "Both"]:
        cert_docx = CERT_DIR / f"{c_id}_Certificate.docx"
        cert_pdf = CERT_DIR / f"{c_id}_Certificate.pdf"
        if not cert_docx.exists() or not cert_pdf.exists():
            generate_certificate(candidate_data)
        if cert_pdf.exists():
            attachment_paths.append(cert_pdf)
        elif cert_docx.exists():
            attachment_paths.append(cert_docx)

    return attachment_paths

def send_single_email_smtp(sender_email, sender_password, recipient_email, subject, body, attachment_paths=None):
    """Send an individual email using Gmail SMTP server."""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_paths:
            for path in attachment_paths:
                if path.exists():
                    with open(path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{path.name}"')
                        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True, "Email sent successfully via Gmail SMTP"
    except Exception as e:
        return False, str(e)

def process_email_dispatch(candidate_list, subject_template, body_template, attachment_option="None", progress_callback=None):
    """Batch process email sending for a list of selected candidates."""
    email_mode = get_setting("email_mode", "Demo Mode")
    sender_email, sender_password = get_smtp_credentials()

    results = []
    total = len(candidate_list)

    for idx, candidate in enumerate(candidate_list):
        c_id = candidate.get("candidate_id", "")
        recipient_email = candidate.get("email", "")
        rendered_subject = personalize_text(subject_template, candidate)
        rendered_body = personalize_text(body_template, candidate)

        attachment_paths = resolve_candidate_attachments(candidate, attachment_option)
        attachment_names = ", ".join([p.name for p in attachment_paths]) if attachment_paths else "None"

        if email_mode == "Demo Mode":
            time.sleep(0.2)
            status = "SUCCESS"
            log_email_send(c_id, recipient_email, rendered_subject, status, "Simulated successfully (Demo Mode)", attachment_names)
            results.append({
                "candidate_id": c_id,
                "name": candidate.get("name"),
                "email": recipient_email,
                "status": "SUCCESS",
                "message": "Simulated successfully (Demo Mode)",
                "attachment": attachment_names
            })
        else:
            if not sender_email or not sender_password:
                status = "FAILED"
                error_msg = "Gmail credentials not configured."
                log_email_send(c_id, recipient_email, rendered_subject, status, error_msg, attachment_names)
                results.append({
                    "candidate_id": c_id,
                    "name": candidate.get("name"),
                    "email": recipient_email,
                    "status": "FAILED",
                    "message": error_msg,
                    "attachment": attachment_names
                })
            else:
                success, msg = send_single_email_smtp(sender_email, sender_password, recipient_email, rendered_subject, rendered_body, attachment_paths)
                status = "SUCCESS" if success else "FAILED"
                log_email_send(c_id, recipient_email, rendered_subject, status, "" if success else msg, attachment_names)
                results.append({
                    "candidate_id": c_id,
                    "name": candidate.get("name"),
                    "email": recipient_email,
                    "status": status,
                    "message": msg,
                    "attachment": attachment_names
                })

        if progress_callback:
            progress_callback(idx + 1, total)

    s_count = len([r for r in results if r["status"] == "SUCCESS"])
    f_count = len([r for r in results if r["status"] == "FAILED"])
    add_notification("Email Dispatch Completed", f"Sent/Logged {s_count} successful emails, {f_count} failed.", "Success" if f_count == 0 else "Warning")

    return results

def retry_single_email_log(log_id):
    """Retry sending a failed email by log_id."""
    from database.database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_logs WHERE id = ?", (log_id,))
    log_row = cursor.fetchone()

    if not log_row:
        conn.close()
        return False, "Log record not found"

    log_data = dict(log_row)
    c_id = log_data["candidate_id"]

    cursor.execute("SELECT * FROM candidates WHERE candidate_id = ?", (c_id,))
    cand_row = cursor.fetchone()
    conn.close()

    if not cand_row:
        return False, f"Candidate {c_id} not found"

    candidate = dict(cand_row)
    email_mode = get_setting("email_mode", "Demo Mode")
    sender_email, sender_password = get_smtp_credentials()

    if email_mode == "Demo Mode":
        time.sleep(0.2)
        log_email_send(c_id, candidate["email"], log_data["subject"], "SUCCESS", "Retried successfully (Demo Mode)", log_data.get("attachment", ""))
        add_notification("Email Retried", f"Retried email for {candidate['name']} ({c_id}).", "Success")
        return True, "Simulated retry successful"
    else:
        if not sender_email or not sender_password:
            return False, "Gmail credentials missing"
        
        attachment_paths = []
        if log_data.get("attachment") and log_data["attachment"] != "None":
            for fname in log_data["attachment"].split(", "):
                if "Offer_Letter" in fname:
                    attachment_paths.append(OFFER_DIR / fname)
                elif "Certificate" in fname:
                    attachment_paths.append(CERT_DIR / fname)

        success, msg = send_single_email_smtp(
            sender_email, sender_password, candidate["email"], log_data["subject"], "Retried Communication", attachment_paths
        )
        status = "SUCCESS" if success else "FAILED"
        log_email_send(c_id, candidate["email"], log_data["subject"], status, "" if success else msg, log_data.get("attachment", ""))
        add_notification("Email Retried", f"Retried email for {candidate['name']} ({c_id}). Status: {status}", "Success" if success else "Warning")
        return success, msg
