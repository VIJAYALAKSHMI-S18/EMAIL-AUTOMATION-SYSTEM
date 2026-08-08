import os
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "generated_documents"
OFFER_DIR = DOCS_DIR / "offer_letters"
CERT_DIR = DOCS_DIR / "certificates"

# Ensure output directories exist
OFFER_DIR.mkdir(parents=True, exist_ok=True)
CERT_DIR.mkdir(parents=True, exist_ok=True)

def set_cell_border(cell, **kwargs):
    """Set cell borders for python-docx tables."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)

    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["val", "color", "sz", "space"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))

def generate_offer_letter(candidate_data):
    """
    Generate professional Offer Letter .docx document for a candidate.
    Returns (file_name, file_path)
    """
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    c_id = str(candidate_data.get("candidate_id", "C000")).strip()
    name = str(candidate_data.get("name", "Candidate")).strip()
    email = str(candidate_data.get("email", "")).strip()
    phone = str(candidate_data.get("phone", "")).strip()
    position = str(candidate_data.get("position", "")).strip()
    department = str(candidate_data.get("department", "")).strip()
    company = str(candidate_data.get("company", "ABC Technologies")).strip()
    joining_date = str(candidate_data.get("joining_date", "")).strip()
    salary = f"${float(candidate_data.get('salary', 0)):,.2f}"
    current_date = datetime.now().strftime("%B %d, %Y")

    # Header / Company Banner
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_comp = p_header.add_run(f"{company.upper()}\n")
    run_comp.bold = True
    run_comp.font.size = Pt(16)
    run_comp.font.color.rgb = RGBColor(30, 41, 59)  # Slate dark

    run_sub = p_header.add_run("Human Resources Division | Corporate Headquarters\n")
    run_sub.font.size = Pt(9)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    run_date = p_header.add_run(f"Date: {current_date}\n")
    run_date.font.size = Pt(10)
    run_date.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()  # spacing

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("OFFER OF EMPLOYMENT")
    run_title.bold = True
    run_title.font.size = Pt(18)
    run_title.font.color.rgb = RGBColor(37, 99, 235)  # Electric Blue

    doc.add_paragraph()

    # Recipient Info
    p_to = doc.add_paragraph()
    p_to.add_run(f"To,\n").bold = True
    p_to.add_run(f"{name}\n").bold = True
    p_to.add_run(f"Candidate ID: {c_id}\n")
    p_to.add_run(f"Email: {email}\n")
    if phone:
        p_to.add_run(f"Phone: {phone}\n")

    doc.add_paragraph()

    # Salutation & Opening Body
    p_body = doc.add_paragraph()
    p_body.paragraph_format.line_spacing = 1.2
    run_salut = p_body.add_run(f"Dear {name},\n\n")
    run_salut.bold = True

    p_body.add_run(
        f"Congratulations! On behalf of {company}, we are thrilled to offer you the position of "
        f"{position} in our {department} department. We were thoroughly impressed with your experience "
        f"and believe your skills will be invaluable to our team.\n\n"
        f"Below are the primary terms and details of your employment offer:"
    )

    # Details Table
    table = doc.add_table(rows=5, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    details = [
        ("Position Title:", position),
        ("Department:", department),
        ("Company Name:", company),
        ("Proposed Joining Date:", joining_date),
        ("Annual Salary / Remuneration:", salary)
    ]

    for idx, (label, val) in enumerate(details):
        row = table.rows[idx]
        cell_lbl = row.cells[0]
        cell_val = row.cells[1]

        cell_lbl.text = label
        cell_lbl.paragraphs[0].runs[0].font.bold = True
        cell_lbl.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 41, 59)
        
        cell_val.text = str(val)
        cell_val.paragraphs[0].runs[0].font.color.rgb = RGBColor(37, 99, 235)
        cell_val.paragraphs[0].runs[0].font.bold = True

        # Padding / styling
        set_cell_border(cell_lbl, bottom={"val": "single", "sz": "4", "color": "CBD5E1"})
        set_cell_border(cell_val, bottom={"val": "single", "sz": "4", "color": "CBD5E1"})

    doc.add_paragraph()

    # Closing Remarks
    p_close = doc.add_paragraph()
    p_close.paragraph_format.line_spacing = 1.2
    p_close.add_run(
        f"Please indicate your acceptance of this offer by signing and returning a copy of this document.\n"
        f"We look forward to having you join our organization and building a successful future together.\n\n"
        f"Sincerely,\n\n"
    )

    # Signatory Section
    p_sign = doc.add_paragraph()
    run_sig_name = p_sign.add_run("Authorized Recruitment Team\n")
    run_sig_name.bold = True
    run_sig_name.font.color.rgb = RGBColor(30, 41, 59)
    run_sig_comp = p_sign.add_run(f"Human Resources Department\n{company}")
    run_sig_comp.font.color.rgb = RGBColor(100, 116, 139)

    file_name = f"{c_id}_Offer_Letter.docx"
    file_path = OFFER_DIR / file_name
    doc.save(file_path)

    return file_name, str(file_path)

def generate_certificate(candidate_data):
    """
    Generate professional Selection Certificate .docx document for a candidate.
    Returns (file_name, file_path)
    """
    doc = Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    c_id = str(candidate_data.get("candidate_id", "C000")).strip()
    name = str(candidate_data.get("name", "Candidate")).strip()
    position = str(candidate_data.get("position", "")).strip()
    department = str(candidate_data.get("department", "")).strip()
    company = str(candidate_data.get("company", "ABC Technologies")).strip()
    joining_date = str(candidate_data.get("joining_date", "")).strip()
    current_date = datetime.now().strftime("%B %d, %Y")

    # Header / Decorative Subtitle
    p_comp = doc.add_paragraph()
    p_comp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cname = p_comp.add_run(f"{company.upper()}\n")
    run_cname.bold = True
    run_cname.font.size = Pt(20)
    run_cname.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph()

    # Certificate Main Header
    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cert = p_cert.add_run("CERTIFICATE OF SELECTION")
    run_cert.bold = True
    run_cert.font.size = Pt(24)
    run_cert.font.color.rgb = RGBColor(37, 99, 235)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("THIS IS TO CERTIFY THAT")
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph()

    # Candidate Name Display
    p_name = doc.add_paragraph()
    p_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_name = p_name.add_run(name)
    run_name.bold = True
    run_name.font.size = Pt(26)
    run_name.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph()

    # Description Paragraph
    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc.paragraph_format.line_spacing = 1.3
    
    run_d1 = p_desc.add_run("has successfully completed the selection process and has been chosen for the position of\n")
    run_d1.font.size = Pt(13)
    
    run_pos = p_desc.add_run(f"{position}\n")
    run_pos.bold = True
    run_pos.font.size = Pt(16)
    run_pos.font.color.rgb = RGBColor(37, 99, 235)

    run_d2 = p_desc.add_run(f"in the {department} Department at {company}.\n\n")
    run_d2.font.size = Pt(13)

    run_jd = p_desc.add_run(f"Candidate ID: {c_id}   |   Scheduled Joining Date: {joining_date}\n")
    run_jd.font.size = Pt(11)
    run_jd.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph()
    doc.add_paragraph()

    # Signature Block
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    cell_left = table.rows[0].cells[0]
    cell_right = table.rows[0].cells[1]

    p_l = cell_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l.add_run(f"Date of Issuance: {current_date}\nVerification Code: CERT-{c_id}-2026").font.size = Pt(10)

    p_r = cell_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_s1 = p_r.add_run("_________________________\nAuthorized HR Signatory\n")
    run_s1.bold = True
    run_s1.font.size = Pt(11)
    run_s2 = p_r.add_run(f"{company}")
    run_s2.font.size = Pt(10)
    run_s2.font.color.rgb = RGBColor(100, 116, 139)

    file_name = f"{c_id}_Certificate.docx"
    file_path = CERT_DIR / file_name
    doc.save(file_path)

    return file_name, str(file_path)
