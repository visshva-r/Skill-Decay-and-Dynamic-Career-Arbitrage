"""Batch analysis, mentor exports, and placement cell UI."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

from skillpulse.charts import build_batch_decay_chart, build_batch_heatmap
from skillpulse.config import (
    SAMPLE_BATCH_STUDENT_3_PATH,
    SAMPLE_RESUME_ALT_PATH,
    SAMPLE_RESUME_PATH,
)
from skillpulse.market import analyze_market, compute_resume_compatibility, score_label
from skillpulse.reports import generate_batch_pdf, generate_readiness_report_pdf
from skillpulse.skills import extract_skills


def load_demo_batch_profiles() -> list[tuple[str, str]]:
    return [
        ("Riya Sharma (Strong)", SAMPLE_RESUME_PATH.read_text(encoding="utf-8")),
        ("Arjun Kumar (Weak)", SAMPLE_RESUME_ALT_PATH.read_text(encoding="utf-8")),
        ("Priya Nair (Moderate)", SAMPLE_BATCH_STUDENT_3_PATH.read_text(encoding="utf-8")),
    ]


def parse_batch_from_text(text: str) -> list[tuple[str, str]]:
    blocks = [block.strip() for block in text.split("---") if block.strip()]
    profiles: list[tuple[str, str]] = []
    for index, block in enumerate(blocks, start=1):
        first_line = block.splitlines()[0].strip() if block.splitlines() else f"Student {index}"
        label = first_line[:48] if first_line else f"Student {index}"
        profiles.append((label, block))
    return profiles


def parse_batch_from_files(uploaded_files: list) -> list[tuple[str, str]]:
    profiles: list[tuple[str, str]] = []
    for uploaded in uploaded_files:
        label = Path(uploaded.name).stem.replace("_", " ").title()
        profiles.append((label, uploaded.read().decode("utf-8", errors="replace")))
    return profiles


def analyze_single_profile(profile_text: str, label: str, filtered_jobs: pd.DataFrame, role: str) -> dict[str, object]:
    student_skills = extract_skills(profile_text)
    analysis = analyze_market(filtered_jobs, student_skills)
    compatibility = compute_resume_compatibility(student_skills, analysis["required_skills"], profile_text, role)
    rising_skills = analysis["rising"]["skill"].tolist() if not analysis["rising"].empty else []
    missing_top = (analysis["missing"] + ["", "", ""])[:3]
    return {
        "student_label": label,
        "decay_score": analysis["score"],
        "fit_score": compatibility["overall"],
        "missing_skill_1": missing_top[0],
        "missing_skill_2": missing_top[1],
        "missing_skill_3": missing_top[2],
        "risk_level": score_label(analysis["score"]),
        "skills": student_skills,
        "analysis": analysis,
        "compatibility": compatibility,
        "rising_skills": rising_skills,
    }


def run_batch_analysis(profiles: list[tuple[str, str]], role: str, filtered_jobs: pd.DataFrame) -> pd.DataFrame:
    rows = [analyze_single_profile(text, label, filtered_jobs, role) for label, text in profiles]
    return prioritize_batch_risk(pd.DataFrame(rows))


def prioritize_batch_risk(batch_df: pd.DataFrame) -> pd.DataFrame:
    return batch_df.sort_values(by=["decay_score", "fit_score"], ascending=[False, True]).reset_index(drop=True)


def aggregate_batch_summary(batch_df: pd.DataFrame) -> dict[str, object]:
    all_missing: list[str] = []
    for column in ["missing_skill_1", "missing_skill_2", "missing_skill_3"]:
        all_missing.extend([skill for skill in batch_df[column].tolist() if skill])
    top_missing = Counter(all_missing).most_common(5)
    return {
        "total": len(batch_df),
        "high_risk": int((batch_df["decay_score"] >= 70).sum()),
        "medium_risk": int(((batch_df["decay_score"] >= 40) & (batch_df["decay_score"] < 70)).sum()),
        "low_risk": int((batch_df["decay_score"] < 40).sum()),
        "avg_fit": round(float(batch_df["fit_score"].mean()), 1) if len(batch_df) else 0.0,
        "top_missing": top_missing,
        "training_focus": [skill for skill, _ in top_missing[:5]],
    }


def export_batch_csv(batch_df: pd.DataFrame, role: str, city: str) -> str:
    export_df = batch_df[
        ["student_label", "decay_score", "fit_score", "missing_skill_1", "missing_skill_2", "missing_skill_3", "risk_level"]
    ].copy()
    export_df.insert(0, "city", city)
    export_df.insert(0, "role", role)
    return export_df.to_csv(index=False)


def export_mentor_action_plan_csv(batch_df: pd.DataFrame, role: str, city: str) -> str:
    rows: list[dict[str, str]] = []
    for _, student in batch_df.iterrows():
        rising = student.get("rising_skills") or []
        if isinstance(rising, str):
            rising = [rising]
        train_skills = [skill for skill in rising if skill][:3]
        if not train_skills:
            train_skills = [student.get("missing_skill_1", ""), student.get("missing_skill_2", ""), student.get("missing_skill_3", "")]
            train_skills = [skill for skill in train_skills if skill][:3]
        rows.append({
            "role": role,
            "city": city,
            "student_label": student["student_label"],
            "decay_score": str(student["decay_score"]),
            "risk_level": student["risk_level"],
            "train_on_skill_1": train_skills[0] if len(train_skills) > 0 else "",
            "train_on_skill_2": train_skills[1] if len(train_skills) > 1 else "",
            "train_on_skill_3": train_skills[2] if len(train_skills) > 2 else "",
            "mentor_action": (
                f"Prioritize coaching on {', '.join(train_skills)} for this high-risk profile."
                if student["decay_score"] >= 40 and train_skills
                else "Maintain current momentum; review monthly market signals."
            ),
        })
    return pd.DataFrame(rows).to_csv(index=False)


def render_placement_cell_mode(
    jobs_df: pd.DataFrame,
    role: str,
    city: str,
    batch_name: str,
    batch_profiles: list[tuple[str, str]],
) -> None:
    st.markdown("### Placement Cell Mode")
    st.caption(
        "Rank a student batch by skill decay risk for one role and city, "
        "then export mentor actions for the highest-risk profiles first."
    )
    filtered_jobs = jobs_df[(jobs_df["role"] == role) & (jobs_df["city"] == city)].copy()
    if filtered_jobs.empty:
        st.error("No job postings available for this role/city combination in the current dataset.")
        st.stop()
    if len(batch_profiles) < 1:
        st.info("Add at least one student profile in the sidebar using upload, paste, or **Load demo batch (3 students)**.")
        st.stop()

    batch_df = run_batch_analysis(batch_profiles, role, filtered_jobs)
    summary = aggregate_batch_summary(batch_df)

    metric_cols = st.columns(4)
    metric_cols[0].metric("Students Analyzed", summary["total"])
    metric_cols[1].metric("High-Risk Students", summary["high_risk"])
    metric_cols[2].metric("Average Fit Score", f"{summary['avg_fit']}%")
    metric_cols[3].metric("Job Postings", len(filtered_jobs))

    focus_text = ", ".join(summary["training_focus"]) if summary["training_focus"] else "No major batch-wide gaps detected"
    st.success(f"Recommended 2-week training focus: **{focus_text}**")

    st.markdown('<p class="section-header">Mentor Export Pack</p>', unsafe_allow_html=True)
    export_cols = st.columns(4)
    csv_data = export_batch_csv(batch_df, role, city)
    action_plan_csv = export_mentor_action_plan_csv(batch_df, role, city)
    with export_cols[0]:
        st.download_button(
            "Export Batch CSV",
            data=csv_data.encode("utf-8"),
            file_name=f"skillpulse_batch_{role.replace(' ', '_')}_{city}.csv",
            mime="text/csv",
        )
    with export_cols[1]:
        st.download_button(
            "Mentor Action Plan (CSV)",
            data=action_plan_csv.encode("utf-8"),
            file_name=f"skillpulse_mentor_action_{role.replace(' ', '_')}_{city}.csv",
            mime="text/csv",
        )
    batch_pdf = generate_batch_pdf(batch_df, summary, role, city, batch_name)
    with export_cols[2]:
        if batch_pdf:
            st.download_button(
                "Export Batch PDF",
                data=batch_pdf,
                file_name=f"skillpulse_batch_{role.replace(' ', '_')}_{city}.pdf",
                mime="application/pdf",
            )
        else:
            st.caption("Install `fpdf2` for PDF export.")
    readiness_pdf = generate_readiness_report_pdf(batch_df, summary, role, city, batch_name)
    with export_cols[3]:
        if readiness_pdf:
            st.download_button(
                "College Readiness Report (PDF)",
                data=readiness_pdf,
                file_name=f"skillpulse_readiness_{role.replace(' ', '_')}_{city}.pdf",
                mime="application/pdf",
            )
        else:
            st.caption("Install `fpdf2` for readiness PDF.")

    st.markdown('<p class="section-header">College Placement Readiness Report</p>', unsafe_allow_html=True)
    display_batch = batch_name.strip() or "Unnamed batch"
    st.markdown(f"**Batch:** {display_batch}")
    readiness_cols = st.columns(3)
    readiness_cols[0].metric("High Risk", summary["high_risk"])
    readiness_cols[1].metric("Medium Risk", summary["medium_risk"])
    readiness_cols[2].metric("Low Risk", summary["low_risk"])
    st.caption(f"Role: **{role}** | City: **{city}** | Profiles: **{summary['total']}** | Date: **{pd.Timestamp.today().date()}**")

    table_df = batch_df[
        ["student_label", "decay_score", "fit_score", "missing_skill_1", "missing_skill_2", "missing_skill_3", "risk_level"]
    ].rename(columns={
        "student_label": "Student",
        "decay_score": "Decay Risk",
        "fit_score": "Fit Score",
        "missing_skill_1": "Missing Skill 1",
        "missing_skill_2": "Missing Skill 2",
        "missing_skill_3": "Missing Skill 3",
        "risk_level": "Risk Level",
    })
    st.markdown('<p class="section-header">Batch Results (High-Risk First)</p>', unsafe_allow_html=True)
    st.dataframe(table_df, width="stretch", hide_index=True)

    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(build_batch_decay_chart(batch_df), width="stretch")
    with chart_right:
        st.plotly_chart(build_batch_heatmap(batch_df), width="stretch")

    if summary["top_missing"]:
        st.markdown('<p class="section-header">Top Batch-Wide Missing Skills</p>', unsafe_allow_html=True)
        for skill, count in summary["top_missing"]:
            st.markdown(f"- **{skill}**: missing in **{count}** student profile(s)")
