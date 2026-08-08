def personalize_text(template_text, candidate_data):
    """
    Replace placeholders in subject or body with actual candidate data.
    Supports both {{name}} / {{position}} and {Name} / {Position} formats.
    """
    if not template_text:
        return ""

    salary_str = f"${float(candidate_data.get('salary', 0)):,.2f}" if candidate_data.get("salary") is not None else ""

    # Map all variations
    replacements = {
        "{{name}}": str(candidate_data.get("name", "")),
        "{{Name}}": str(candidate_data.get("name", "")),
        "{Name}": str(candidate_data.get("name", "")),
        "{name}": str(candidate_data.get("name", "")),

        "{{candidate_id}}": str(candidate_data.get("candidate_id", "")),
        "{{Candidate_ID}}": str(candidate_data.get("candidate_id", "")),
        "{Candidate_ID}": str(candidate_data.get("candidate_id", "")),
        "{candidate_id}": str(candidate_data.get("candidate_id", "")),

        "{{email}}": str(candidate_data.get("email", "")),
        "{{Email}}": str(candidate_data.get("email", "")),
        "{Email}": str(candidate_data.get("email", "")),
        "{email}": str(candidate_data.get("email", "")),

        "{{phone}}": str(candidate_data.get("phone", "")),
        "{{Phone}}": str(candidate_data.get("phone", "")),
        "{Phone}": str(candidate_data.get("phone", "")),
        "{phone}": str(candidate_data.get("phone", "")),

        "{{position}}": str(candidate_data.get("position", "")),
        "{{Position}}": str(candidate_data.get("position", "")),
        "{Position}": str(candidate_data.get("position", "")),
        "{position}": str(candidate_data.get("position", "")),

        "{{department}}": str(candidate_data.get("department", "")),
        "{{Department}}": str(candidate_data.get("department", "")),
        "{Department}": str(candidate_data.get("department", "")),
        "{department}": str(candidate_data.get("department", "")),

        "{{company}}": str(candidate_data.get("company", "")),
        "{{Company}}": str(candidate_data.get("company", "")),
        "{Company}": str(candidate_data.get("company", "")),
        "{company}": str(candidate_data.get("company", "")),

        "{{joining_date}}": str(candidate_data.get("joining_date", "")),
        "{{Joining_Date}}": str(candidate_data.get("joining_date", "")),
        "{Joining_Date}": str(candidate_data.get("joining_date", "")),
        "{joining_date}": str(candidate_data.get("joining_date", "")),

        "{{salary}}": salary_str,
        "{{Salary}}": salary_str,
        "{Salary}": salary_str,
        "{salary}": salary_str,
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
        attachments.append(f"{c_id}_Offer_Letter.pdf")
    if attachment_option in ["Certificate", "Both"]:
        attachments.append(f"{c_id}_Certificate.docx")
        attachments.append(f"{c_id}_Certificate.pdf")

    return {
        "candidate_id": c_id,
        "recipient_name": candidate_data.get("name", ""),
        "recipient_email": candidate_data.get("email", ""),
        "subject": rendered_subject,
        "body": rendered_body,
        "attachments": attachments
    }
