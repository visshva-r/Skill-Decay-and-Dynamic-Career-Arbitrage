"""PDF report generation for student and batch exports."""
from __future__ import annotations

import re

import pandas as pd

from skillpulse.market import score_label

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None


def _pdf_safe(text: str) -> str:
    text = re.sub(r"[`*]", "", text)
    text = text.replace("\u0394", "delta").replace("\u2014", "-").replace("\u2013", "-")
    text = text.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_pdf_report(role: str, city: str, filtered_jobs: pd.DataFrame, analysis: dict, roadmap: list[dict[str, str]], proof_pack: dict[str, str], compatibility_data: dict[str, int], student_skills: list[str], salary_summary: dict) -> bytes | None:
    if FPDF is None:
        return None
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def write_block(text: str, size: int = 10) -> None:
        pdf.set_font("Helvetica", "", size)
        pdf.multi_cell(w=0, h=6, text=_pdf_safe(text), new_x="LMARGIN", new_y="NEXT")

    def heading(text: str) -> None:
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(w=0, h=10, text=text, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(w=0, h=15, text="SkillPulse Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(w=0, h=8, text=_pdf_safe(f"Role: {role}  |  City: {city}  |  Postings Analyzed: {len(filtered_jobs)}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    heading("Scores")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(w=0, h=7, text=f"Skill Decay Risk: {analysis['score']}/100 ({score_label(analysis['score'])})", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(w=0, h=7, text=f"Resume Compatibility: {compatibility_data['overall']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    heading("Salary Insights")
    write_block(f"Average Range: {salary_summary['avg_min']} - {salary_summary['avg_max']}")
    write_block(f"Total Positions: {salary_summary['total_positions']}")
    heading("Matched Skills")
    write_block(", ".join(analysis["matched"]) if analysis["matched"] else "None")
    heading("Missing High-Demand Skills")
    write_block(", ".join(analysis["missing"]) if analysis["missing"] else "None")
    heading("Market Trend Insights")
    for explanation in analysis["explanations"]:
        write_block(f"- {explanation}")
    if analysis.get("evidence_cards"):
        heading("Evidence Cards")
        for card in analysis["evidence_cards"][:5]:
            write_block(f"- {card}")
    heading("7-Day Micro Roadmap")
    for item in roadmap:
        write_block(f"{item['day']} - {item['focus']}: {item['task']}")
    heading("Proof Pack")
    write_block(f"Project: {proof_pack['title']}")
    write_block(f"Idea: {proof_pack['idea']}")
    write_block(f"Resume Bullet: {proof_pack['resume_bullet']}")
    heading("Your Skills")
    write_block(", ".join(student_skills) if student_skills else "None detected")
    heading("Resume Compatibility Breakdown")
    for label, key in [("Skill Match", "skill_match"), ("Keyword Density", "keyword_density"), ("Completeness", "completeness"), ("Role Alignment", "role_alignment")]:
        pdf.cell(w=0, h=6, text=f"{label}: {compatibility_data[key]}%", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())


def generate_batch_pdf(batch_df: pd.DataFrame, summary: dict[str, object], role: str, city: str, batch_name: str) -> bytes | None:
    if FPDF is None:
        return None
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(w=0, h=12, text="SkillPulse Mentor Export Pack", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(w=0, h=7, text=_pdf_safe(f"Batch: {batch_name or 'Unnamed batch'}  |  Role: {role}  |  City: {city}"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(w=0, h=8, text="Batch Summary", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for line in [
        f"Total students: {summary['total']}",
        f"High risk: {summary['high_risk']}  |  Medium risk: {summary['medium_risk']}  |  Low risk: {summary['low_risk']}",
        f"Average fit score: {summary['avg_fit']}%",
        f"Top batch-wide missing skills: {', '.join(summary['training_focus']) or 'None'}",
    ]:
        pdf.cell(w=0, h=6, text=_pdf_safe(line), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(w=0, h=8, text="Student Results", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    for _, row in batch_df.iterrows():
        pdf.multi_cell(
            w=0,
            h=5,
            text=_pdf_safe(
                f"{row['student_label']} | Decay {row['decay_score']} | Fit {row['fit_score']}% | "
                f"Missing: {row['missing_skill_1']}, {row['missing_skill_2']}, {row['missing_skill_3']} | {row['risk_level']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )
        pdf.ln(1)
    return bytes(pdf.output())


def generate_readiness_report_pdf(batch_df: pd.DataFrame, summary: dict[str, object], role: str, city: str, batch_name: str) -> bytes | None:
    if FPDF is None:
        return None
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(w=0, h=12, text="College Placement Readiness Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(w=0, h=7, text=_pdf_safe("SkillPulse - Placement Intelligence Platform"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(w=0, h=8, text="Batch Overview", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    overview_lines = [
        f"Batch name: {batch_name or 'Unnamed batch'}",
        f"Target role: {role}",
        f"Target city: {city}",
        f"Report date: {pd.Timestamp.today().date()}",
        f"Total profiles analyzed: {summary['total']}",
        f"High decay risk: {summary['high_risk']}",
        f"Medium decay risk: {summary['medium_risk']}",
        f"Low decay risk: {summary['low_risk']}",
        f"Average resume fit score: {summary['avg_fit']}%",
    ]
    for line in overview_lines:
        pdf.cell(w=0, h=6, text=_pdf_safe(line), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(w=0, h=8, text="Recommended 2-week training focus", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    focus_skills = summary["training_focus"] or ["No major batch-wide gaps detected"]
    for index, skill in enumerate(focus_skills, start=1):
        pdf.cell(w=0, h=6, text=_pdf_safe(f"{index}. {skill}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(w=0, h=8, text="Student Risk Snapshot", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    for _, row in batch_df.iterrows():
        pdf.multi_cell(
            w=0,
            h=5,
            text=_pdf_safe(
                f"{row['student_label']}: decay {row['decay_score']}/100 ({row['risk_level']}), "
                f"fit {row['fit_score']}%, missing {row['missing_skill_1']}, {row['missing_skill_2']}, {row['missing_skill_3']}"
            ),
            new_x="LMARGIN",
            new_y="NEXT",
        )
    return bytes(pdf.output())
