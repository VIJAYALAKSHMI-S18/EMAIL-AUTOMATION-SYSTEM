# Email Automation Portal – Smart Recruitment Communication Management

> **Automate. Personalize. Communicate.**

Live Application Demo: [email-automation-system-27.streamlit.app](https://email-automation-system-27.streamlit.app/)

The **Email Automation Portal** is a production-ready, SaaS-grade **Recruitment Email Automation System** built with **Python, Streamlit, Pandas, openpyxl, SQLite, python-docx, ReportLab, Plotly, and SMTP**.

It transforms repetitive HR workflows (candidate management, Word/PDF document creation, personalized email campaigns, individual file attachments, and audit tracking) into a centralized enterprise portal.

---

## 📌 Problem Statement

In traditional recruitment workflows, HR teams manually handle candidate data across fragmented tools:
- Maintaining candidate information in Microsoft Excel.
- Manually drafting and formatting Offer Letters and Certificates in Word and PDF.
- Manually writing and sending emails to each candidate via email clients.
- Attaching individual candidate files manually.
- Manually tracking sent/failed emails in spreadsheets.

When candidate volume increases, this process becomes time-consuming, error-prone, repetitive, inconsistent, and administratively expensive.

---

## 🎯 System Objectives & Key Features

1. **Authentication & Session Security**: Secure landing page with username/password authentication, session state protection, and logout capabilities.
2. **Interactive Executive Dashboard**: Dynamic time-based greeting (*Good Morning / Afternoon / Evening, HR Admin*), top metric cards (Total Candidates, Selected Candidates, Emails Sent, Pending, Failed), Plotly interactive graphs, and a real-time Recent Activities audit feed.
3. **Candidate Directory & Excel Engine**: Excel upload with validation (missing columns, email syntax, duplicates, salary checks), search, department/position filters, selection checkboxes, and Excel export (`recruitment_candidates.xlsx`).
4. **Dual Document Generation (Word .docx & PDF .pdf)**: Generates personalized **Offer Letters** and **Certificates** in both Word `.docx` and PDF `.pdf` formats using `python-docx` and `ReportLab`.
5. **Dynamic Email Personalization**: Dynamic placeholder engine supporting both `{{name}}`, `{{position}}`, `{{company}}`, `{{joining_date}}`, `{{salary}}` and `{Name}`, `{Position}` syntax.
6. **Campaign Management & Scheduling**: Group candidate outreach into named campaigns, select document attachment packages, execute immediately, or schedule campaigns.
7. **Email History & Failure Retry**: Filterable email log table tracking recipient, subject, sent timestamp, status, and error stack traces with a `Retry` action button.
8. **Notification Center**: Real-time activity feeds and alerts for imports, document generations, campaign launches, and errors.
9. **Settings & Configuration**: Profile manager, Gmail SMTP setup guide (16-character App Password), application options, and transmission toggles.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend / Web UI** | Streamlit |
| **Backend & Logic** | Python 3.10+ |
| **Data Processing** | Pandas, openpyxl |
| **Database** | SQLite (`sqlite3`) |
| **Document Generation** | `python-docx` (Word) & `ReportLab` (PDF) |
| **Visual Analytics** | Plotly Express & Plotly Graph Objects |
| **Email Protocol** | Python SMTP (`smtplib`, `email.mime`) |
| **Configuration** | `python-dotenv` & Streamlit Secrets |

---

## 🏗️ System Architecture & Workflow

```text
               EMAIL AUTOMATION PORTAL
                          │
                          ▼
                     Login Page
                          │
                          ▼
                 HR Executive Dashboard
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       Download Excel             Upload Excel
          Template                    │
             │                        ▼
             │                 Validate Excel
             │                        │
             └───────────────► SQLite Database
                                      │
                                      ▼
                              Candidate Management
                                      │
                              Select Candidates
                                      │
                      ┌───────────────┴───────────────┐
                      ▼                               ▼
               Generate Offer               Generate Certificate
             Letter (.docx/.pdf)             (.docx/.pdf)
                      │                               │
                      └───────────────┬───────────────┘
                                      ▼
                              Email Automation
                                      │
                                      ▼
                               Live Email Preview
                                      │
                                      ▼
                             Campaign Scheduling
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
                    Demo Mode                 Gmail SMTP
                         │                         │
                         └────────────┬────────────┘
                                      ▼
                             Email Audit Logs
                                      │
                                      ▼
                            Plotly Analytics Page
```

---

## 📂 Directory Structure

```text
email-automation-system/
│
├── app.py                      # Main router handling auth state, global SaaS CSS, sidebar navigation
├── database/
│   ├── __init__.py
│   └── database.py             # SQLite schemas & CRUD functions
├── modules/
│   ├── __init__.py
│   ├── excel_handler.py        # Excel upload, column validation, sample generation, export
│   ├── candidate_manager.py    # Candidate filtering, search, and summary stats
│   ├── document_generator.py   # python-docx (.docx) & ReportLab (.pdf) generator
│   ├── email_sender.py         # SMTP dispatcher, Demo Mode, campaign processor
│   └── email_templates.py      # Dynamic template placeholder engine
├── utils/
│   ├── __init__.py
│   └── auth.py                 # Session state authentication & login validator
├── pages/
│   ├── login.py                # Landing banner & Login Card UI
│   ├── dashboard.py            # Greeting, metric cards, Plotly charts, Recent Activities feed
│   ├── candidates.py           # Candidate directory table, Excel upload/export, filters
│   ├── email_automation.py     # Email composer, live preview, attachment binder, batch sender
│   ├── campaigns.py            # Email Campaign creator, scheduler & campaign metrics
│   ├── documents.py            # Document Center (.docx and .pdf previews/downloads)
│   ├── analytics.py            # Plotly interactive reporting
│   ├── notifications.py        # Activity Feed & System Alerts
│   └── settings.py             # Profile, SMTP config, App options, theme toggle
├── generated_documents/
│   ├── offer_letters/          # Output directory for generated offer letters (.docx and .pdf)
│   └── certificates/           # Output directory for generated certificates (.docx and .pdf)
├── sample_candidates.xlsx      # Sample Excel file
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git exclusions
└── README.md                   # Complete documentation
```

---

## ⚡ Quick Start & Installation Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your machine.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Application
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your web browser.

---

## 🔑 Demo Login Credentials

- **Default Username/Email**: `admin@abctechnologies.com`
- **Default Password**: `admin123`

*You can update administrative passwords in System Settings or via Streamlit Secrets.*

---

## ☁️ Streamlit Cloud Deployment Setup

When deploying to **Streamlit Community Cloud**:
1. Push project to your GitHub repository.
2. Connect repository on Streamlit Cloud.
3. In App Settings -> Secrets, add your SMTP credentials (optional for Gmail SMTP mode):
```toml
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_16_digit_app_password"
```

---

## 📄 License
This project is released under the **MIT License**.