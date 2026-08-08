# RecruitFlow - Recruitment Email Automation System

> **Automate. Personalize. Communicate.**

RecruitFlow is a centralized, end-to-end recruitment email automation system built using **Python, Streamlit, Pandas, openpyxl, SQLite, python-docx, and SMTP**. 

It eliminates repetitive HR tasks such as candidate data management, manual Word offer letter creation, personalized certificate generation, individual email sending, document attachment, and tracking.

---

## Problem Statement

In traditional recruitment workflows, HR teams manually handle candidate data across fragmented tools:
- Maintaining candidate information in Microsoft Excel.
- Manually drafting and formatting Offer Letters and Certificates in Microsoft Word.
- Manually writing and sending emails to each candidate via email clients.
- Attaching individual candidate files manually.
- Manually tracking sent/failed emails in spreadsheets.

When candidate volume increases, this process becomes time-consuming, error-prone, repetitive, inconsistent, and administratively expensive.

---

## System Objectives

RecruitFlow unifies the entire recruitment communication lifecycle into one centralized web application:
1. **Manage Candidate Data**: Upload/Download Excel spreadsheets with automated validation.
2. **SQLite Data Store**: Store persistent candidate records, document logs, email communication logs, and settings.
3. **Automated Document Generation**: Generate personalized `.docx` Offer Letters and Certificates using `python-docx`.
4. **Personalized Email Campaigns**: Dynamic template substitution with placeholder support (`{Name}`, `{Position}`, `{Company}`, `{Joining_Date}`, `{Salary}`).
5. **Dual Email Dispatch Engines**: 
   - **Demo Mode**: Full simulation & SQLite logging without requiring real email credentials (ideal for demonstrations).
   - **Gmail SMTP Mode**: Live individual email dispatch using TLS via Gmail App Passwords.
6. **Audit & Analytics**: Executive dashboard and Matplotlib analytics detailing pipeline status, department distributions, and email dispatch audit logs with retry capabilities.

---

## Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend / UI** | Streamlit |
| **Backend Logic** | Python 3.10+ |
| **Data Processing** | Pandas, openpyxl |
| **Database** | SQLite (`sqlite3`) |
| **Document Generation** | `python-docx` |
| **Email Protocol** | Python SMTP (`smtplib`, `email.mime`) |
| **Visualization** | Matplotlib |
| **Configuration** | `python-dotenv` & Streamlit Secrets |

---

## System Architecture & Workflow

```text
                    RECRUITFLOW
                         │
                         ▼
                  HR Dashboard
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Download Excel            Upload Excel
          Template                   │
             │                       ▼
             │                Validate Excel
             │                       │
             └──────────────► SQLite Database
                                     │
                                     ▼
                             Candidate Management
                                     │
                             Select Candidates
                                     │
                      ┌──────────────┴──────────────┐
                      ▼                             ▼
               Generate Offer              Generate Certificate
                  Letter
                      │                             │
                      └──────────────┬──────────────┘
                                     ▼
                              Email Automation
                                     │
                                     ▼
                              Email Preview
                                     │
                                     ▼
                            Confirm Before Sending
                                     │
                         ┌───────────┴───────────┐
                         ▼                       ▼
                    Demo Mode               Gmail SMTP
                         │                       │
                         └───────────┬───────────┘
                                     ▼
                                Email Logs
                                     │
                                     ▼
                                  Analytics
```

---

## Project Directory Structure

```text
recruitment-email-automation/
│
├── app.py                      # Main Streamlit application entry point & routing
│
├── database/
│   ├── __init__.py
│   └── database.py             # SQLite connection, schema creation, & CRUD functions
│
├── modules/
│   ├── __init__.py
│   ├── excel_handler.py        # Excel upload, column validation, sample generation, export
│   ├── candidate_manager.py    # Candidate filtering, search, and summary stats
│   ├── document_generator.py   # python-docx Offer Letter & Certificate generator
│   ├── email_sender.py         # SMTP email dispatcher & Demo Mode simulator
│   └── email_templates.py      # Email templates & dynamic placeholder engine
│
├── pages/
│   ├── dashboard.py            # HR Executive Dashboard & key metrics
│   ├── candidates.py           # Candidate management table, Excel upload/download, filters
│   ├── documents.py            # Offer letter & Certificate batch generator UI
│   ├── analytics.py            # Matplotlib visual reporting & department analytics
│   ├── email_automation.py     # Email composer, live preview, attachment binder, batch sender
│   ├── email_logs.py           # Audit log table with failure retry mechanism
│   └── settings.py             # Demo/Gmail SMTP toggle, credentials setup, company details
│
├── generated_documents/
│   ├── offer_letters/          # Output directory for generated offer letters (.docx)
│   └── certificates/           # Output directory for generated certificates (.docx)
│
├── sample_candidates.xlsx      # Pre-built sample Excel dataset (10 fictional candidates)
├── .streamlit/
│   ├── config.toml             # Custom UI theme configuration
│   └── secrets.toml.example    # Credentials configuration template
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
└── README.md                   # Complete documentation
```

---

## Quick Start & Installation Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your computer.

### 2. Clone Repository & Navigate
```bash
git clone https://github.com/your-username/recruitment-email-automation.git
cd recruitment-email-automation
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

---

## Gmail SMTP Setup (App Password)

To send live emails via **Gmail SMTP**, Google requires a 16-character **App Password**:

1. Go to your **Google Account** settings (`https://myaccount.google.com`).
2. Select **Security** from the left navigation panel.
3. Ensure **2-Step Verification** is enabled.
4. Search for **App Passwords**.
5. Select **Mail** as the app and **Other (RecruitFlow)** as the device name.
6. Click **Generate** and copy the 16-character password.
7. Create a `.env` file or update `.streamlit/secrets.toml`:
```text
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
```
8. Go to **Settings** in RecruitFlow and switch Transmission Mode to **Gmail SMTP**.

---

## Demo Mode (For Project Presentations & Testing)

RecruitFlow features a built-in **Demo Mode** enabled by default:
- **No SMTP Credentials Required**: Runs 100% locally without external email server connections.
- **Full Automation Simulation**: Generates actual `.docx` files, renders dynamic emails with live previews, simulates batch dispatch progress, records success entries in `email_logs`, and updates analytical charts in real time.
- **Ideal for College / Client Demonstrations**: Demonstrators can showcase the entire system without exposing email credentials or sending real emails to dummy addresses.

---

## License
This project is released under the **MIT License**.