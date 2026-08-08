import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from database.database import (
    get_all_candidates,
    get_all_email_logs,
    get_all_documents
)

def render_analytics_page():
    st.markdown("## 📊 Recruitment Analytics & Insights")
    st.markdown("In-depth statistical reporting on candidate acquisition, departmental hiring, and email communication metrics.")

    candidates = get_all_candidates()
    email_logs = get_all_email_logs()
    documents = get_all_documents()

    if not candidates:
        st.warning("No candidate data available for analytics. Upload or add candidates first.")
        return

    # Filter Bar
    st.markdown("### 🛠 Filter Visualizations")
    af_col1, af_col2 = st.columns(2)

    companies = ["All"] + sorted(list(set([c.get("company") for c in candidates if c.get("company")])))
    departments = ["All"] + sorted(list(set([c.get("department") for c in candidates if c.get("department")])))

    with af_col1:
        sel_comp = st.selectbox("Company Filter", companies, key="analytics_comp")
    with af_col2:
        sel_dept = st.selectbox("Department Filter", departments, key="analytics_dept")

    filtered_cands = candidates
    if sel_comp != "All":
        filtered_cands = [c for c in filtered_cands if c.get("company") == sel_comp]
    if sel_dept != "All":
        filtered_cands = [c for c in filtered_cands if c.get("department") == sel_dept]

    st.markdown("---")

    # Metrics Summary Row
    st.markdown("### 📈 Pipeline Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Candidates", len(filtered_cands))
    with m2:
        sel_count = len([c for c in filtered_cands if c.get("offer_status") == "Selected"])
        st.metric("Selected Candidates", sel_count)
    with m3:
        avg_sal = (sum([float(c.get("salary", 0)) for c in filtered_cands]) / len(filtered_cands)) if filtered_cands else 0
        st.metric("Average Salary", f"${avg_sal:,.2f}")
    with m4:
        st.metric("Total Documents Issued", len(documents))

    st.markdown("---")

    # Row 1 Charts: Offer Status & Email Dispatch Status
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Candidate Status Breakdown")
        offer_counts = {}
        for c in filtered_cands:
            st_val = c.get("offer_status", "Pending")
            offer_counts[st_val] = offer_counts.get(st_val, 0) + 1

        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        colors = ['#2563EB', '#059669', '#D97706', '#DC2626']
        ax1.pie(
            offer_counts.values(),
            labels=offer_counts.keys(),
            autopct='%1.1f%%',
            colors=colors[:len(offer_counts)],
            startangle=90
        )
        ax1.axis('equal')
        st.pyplot(fig1)

    with c2:
        st.markdown("#### Email Communication Dispatch Logs")
        if email_logs:
            email_counts = {"SUCCESS": 0, "FAILED": 0, "PENDING": 0}
            for l in email_logs:
                st_val = l.get("status", "PENDING")
                email_counts[st_val] = email_counts.get(st_val, 0) + 1

            fig2, ax2 = plt.subplots(figsize=(5, 3.5))
            ax2.bar(email_counts.keys(), email_counts.values(), color=['#059669', '#DC2626', '#D97706'])
            ax2.set_ylabel("Email Count")
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            st.pyplot(fig2)
        else:
            st.info("No email campaign logs recorded yet.")

    st.markdown("---")

    # Row 2 Charts: Department Distribution & Salary by Department
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### Candidates per Department")
        dept_counts = {}
        for c in filtered_cands:
            d = c.get("department", "Other")
            dept_counts[d] = dept_counts.get(d, 0) + 1

        fig3, ax3 = plt.subplots(figsize=(5, 3.5))
        ax3.barh(list(dept_counts.keys()), list(dept_counts.values()), color='#1E293B')
        ax3.set_xlabel("Count")
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        st.pyplot(fig3)

    with c4:
        st.markdown("#### Average Salary by Department")
        dept_salaries = {}
        for c in filtered_cands:
            d = c.get("department", "Other")
            sal = float(c.get("salary", 0))
            if d not in dept_salaries:
                dept_salaries[d] = []
            dept_salaries[d].append(sal)

        dept_avg_sal = {d: sum(sals)/len(sals) for d, sals in dept_salaries.items()}

        fig4, ax4 = plt.subplots(figsize=(5, 3.5))
        ax4.bar(list(dept_avg_sal.keys()), list(dept_avg_sal.values()), color='#2563EB')
        plt.xticks(rotation=45, ha='right', fontsize=8)
        ax4.set_ylabel("Average Salary ($)")
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)
        st.pyplot(fig4)
