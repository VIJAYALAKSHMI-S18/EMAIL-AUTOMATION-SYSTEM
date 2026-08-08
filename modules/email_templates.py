def personalize_text(template_text, candidate_data):
    """
    Replace placeholders in subject or body with actual candidate data.
    Supported placeholders:
    {Name}, {Candidate_ID}, {Email}, {Phone}, {Position}, {Department}, {Company}, {Joining_Date}, {Salary}
    """
    if not template_text:
        return ""

    salary_str = f"${float(candidate_data.get('salary', 0)):,.2f}" if candidate_data.get("salary") is not None else ""

    replacements = {
        "{Name}": str(candidate_data.get("name", "")),
        "{Candidate_ID}": str(candidate_data.get("candidate_id", "")),
        "{Email}": str(candidate_data.get("email", "")),
        "{Phone}": str(candidate_data.get("phone", "")),
        "{Position}": str(candidate_data.get("position", "")),
        "{Department}": str(candidate_data.get("department", "")),
        "{Company}": str(candidate_data.get("company", "")),
        "{Joining_Date}": str(candidate_data.get("joining_date", "")),
        "{Salary}": salary_str,
    }

    result = str(template_text)
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result

def get_email_preview(template_subject, template_body, candidate_data, attachment_option="None"):
    """
    Generate rendered preview dict for UI display.
    """
    rendered_subject = personalize_text(template_subject, candidate_data)
    rendered_body = personalize_text(template_body, candidate_data)
    c_id = candidate_data.get("candidate_id", "")

    attachments = []
    if attachment_option in ["Offer Letter", "Both"]:
        attachments.append(f"{c_id}_Offer_Letter.docx")
    if attachment_option in ["Certificate", "Both"]:
        attachments.append(f"{c_id}_Certificate.docx")

    return {
        "candidate_id": c_id,
        "recipient_name": candidate_data.get("name", ""),
        "recipient_email": candidate_data.get("email", ""),
        "subject": rendered_subject,
        "body": rendered_body,
        "attachments": attachments
    }
