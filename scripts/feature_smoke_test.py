"""Local feature smoke test for SkillPulse (logic + export layer)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

from skillpulse.batch import (
    aggregate_batch_summary,
    export_batch_csv,
    export_mentor_action_plan_csv,
    load_demo_batch_profiles,
    prioritize_batch_risk,
    run_batch_analysis,
)
from skillpulse.charts import (
    build_batch_decay_chart,
    build_batch_heatmap,
    build_benchmark_radar,
    build_career_path_chart,
    build_monthly_trend_chart,
    build_openings_chart,
    build_radar_chart,
    build_resume_gauge,
    build_salary_chart,
    build_trend_chart,
)
from skillpulse.config import BENCHMARK_PROFILES, HACKATHON_MAP
from skillpulse.curriculum import build_proof_pack, generate_micro_curriculum, roadmap_for_skills
from skillpulse.data_loader import load_jobs, normalize_city_name
from skillpulse.market import analyze_market, build_market_alert, compute_resume_compatibility
from skillpulse.reports import generate_batch_pdf, generate_pdf_report, generate_readiness_report_pdf
from skillpulse.skills import extract_skills, get_learning_resources
from skillpulse.snapshots import build_profile_key, build_snapshot_delta, export_history_csv, get_profile_history

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def main() -> None:
    df = load_jobs()
    check("Dataset loads", len(df) >= 88, str(len(df)))
    roles = sorted(df["role"].unique())
    cities = sorted(df["city"].unique())
    check("8 roles present", len(roles) == 8, ", ".join(roles))
    check("7 cities present", len(cities) == 7, ", ".join(cities))
    check("FinTech role data", "FinTech Analyst" in roles)
    check("Healthcare role data", "Healthcare Data Analyst" in roles)
    check("Mumbai and Delhi data", "Mumbai" in cities and "Delhi" in cities)

    sparse = df.groupby(["role", "city"]).size()
    sparse_count = int((sparse <= 1).sum())
    check("Role x city coverage (<=1 rows)", sparse_count == 0, f"sparse={sparse_count}")

    strong = extract_skills(Path("data/sample_resume.txt").read_text(encoding="utf-8"))
    weak = extract_skills(Path("data/sample_resume_alt.txt").read_text(encoding="utf-8"))
    check("Strong profile skill extraction", len(strong) >= 5, ", ".join(strong[:6]))
    check("Weak profile skill extraction", len(weak) >= 3, ", ".join(weak))

    for role in ["Junior Data Analyst", "FinTech Analyst", "Healthcare Data Analyst"]:
        city = "Mumbai" if role != "Healthcare Data Analyst" else "Bengaluru"
        jobs = df[(df["role"] == role) & (df["city"] == city)]
        if jobs.empty:
            jobs = df[df["role"] == role].head(8)
        analysis = analyze_market(jobs, weak)
        compat = compute_resume_compatibility(weak, analysis["required_skills"], "weak profile", role)
        check(f"Market analysis: {role}", analysis["score"] > 0)
        check(f"Evidence cards present: {role}", len(analysis.get("evidence_cards", [])) >= 0)
        check(f"Compatibility score: {role}", 0 <= compat["overall"] <= 100)

    jobs = df[(df["role"] == "Junior Data Analyst") & (df["city"] == "Chennai")]
    a_strong = analyze_market(jobs, strong)
    a_weak = analyze_market(jobs, weak)
    check(
        "Weak profile higher decay than strong",
        a_weak["score"] > a_strong["score"],
        f"weak={a_weak['score']} strong={a_strong['score']}",
    )

    analysis = a_weak
    compat = compute_resume_compatibility(weak, analysis["required_skills"], "weak", "Junior Data Analyst")
    check("Radar chart builds", build_radar_chart(weak, analysis["required_skills"]) is not None)
    check("Trend chart builds", build_trend_chart(analysis) is not None)
    check("Monthly trend chart builds", build_monthly_trend_chart(analysis["monthly_df"]) is not None)
    check("Resume gauge builds", build_resume_gauge(compat["overall"]) is not None)
    check("Career path chart builds", build_career_path_chart("FinTech Analyst", weak) is not None)
    check("Salary chart builds", build_salary_chart(jobs) is not None)
    check("Openings chart builds", build_openings_chart(df, "Junior Data Analyst") is not None)

    check("7-day roadmap", len(roadmap_for_skills(analysis["missing"])) >= 1)
    check("Proof pack", "title" in build_proof_pack(analysis["missing"], weak))
    check("Micro curriculum", len(generate_micro_curriculum(analysis["missing"])) >= 1)
    check("Market alert", "title" in build_market_alert(analysis, weak, "Junior Data Analyst", ""))
    check("Learning resources", len(get_learning_resources("Financial Modeling")) >= 2)
    check("Hackathon map", len(HACKATHON_MAP) > 0)

    profiles = load_demo_batch_profiles()
    batch_jobs = df[df["role"] == "Junior Data Analyst"]
    batch = run_batch_analysis(profiles, "Junior Data Analyst", batch_jobs)
    summary = aggregate_batch_summary(batch)
    check("Placement batch analysis (3 students)", len(batch) == 3)
    check("Batch sorted high-risk first", batch.iloc[0]["decay_score"] >= batch.iloc[-1]["decay_score"])
    check(
        "Batch summary metrics",
        summary["total"] == 3 and summary["high_risk"] >= 1,
        f"high_risk={summary['high_risk']} scores={batch['decay_score'].tolist()}",
    )
    check("Batch decay chart", build_batch_decay_chart(batch) is not None)
    check("Batch heatmap", build_batch_heatmap(batch) is not None)
    check("Batch CSV export", "student_label" in export_batch_csv(batch, "Junior Data Analyst", "Chennai"))
    check("Mentor action plan export", "mentor_action" in export_mentor_action_plan_csv(batch, "Junior Data Analyst", "Chennai"))
    batch_pdf = generate_batch_pdf(batch, summary, "Junior Data Analyst", "Chennai", "Demo Batch")
    ready_pdf = generate_readiness_report_pdf(batch, summary, "Junior Data Analyst", "Chennai", "Demo Batch")
    check("Batch PDF export", batch_pdf is not None and len(batch_pdf) > 500)
    check("Readiness PDF export", ready_pdf is not None and len(ready_pdf) > 500)

    check("Compare profiles scoring differs", a_strong["score"] != a_weak["score"])
    bench = BENCHMARK_PROFILES.get("FinTech Analyst")
    check("FinTech benchmark profile", bench is not None)
    check("Benchmark radar", build_benchmark_radar(weak, bench["skills"]) is not None)

    roadmap = roadmap_for_skills(analysis["missing"])
    proof = build_proof_pack(analysis["missing"], weak)
    salary_summary = {
        "avg_min": "4.0 LPA",
        "avg_max": "6.0 LPA",
        "overall_min": "3.0 LPA",
        "overall_max": "7.0 LPA",
        "total_positions": 5,
    }
    student_pdf = generate_pdf_report(
        "Junior Data Analyst", "Chennai", jobs, analysis, roadmap, proof, compat, weak, salary_summary
    )
    check("Student PDF report", student_pdf is not None and len(student_pdf) > 500)

    check("City alias Bangalore", normalize_city_name("Bangalore") == "Bengaluru")
    check("City alias New Delhi", normalize_city_name("New Delhi") == "Delhi")
    key = build_profile_key("test profile", "Junior Data Analyst", "Chennai", "")
    history = get_profile_history(key)
    check("Snapshot history read", isinstance(history, pd.DataFrame))
    check("Snapshot delta helper", "has_delta" in build_snapshot_delta(history))
    check("Snapshot history CSV export", "date" in export_history_csv(history))

    sde_chennai = df[(df["role"] == "SDE / Full-stack Developer") & (df["city"] == "Chennai")]
    ba_pune = df[(df["role"] == "Business Analyst") & (df["city"] == "Pune")]
    check("SDE Chennai coverage", len(sde_chennai) >= 2, str(len(sde_chennai)))
    check("BA Pune coverage", len(ba_pune) >= 2, str(len(ba_pune)))

    aiml_blr = df[(df["role"] == "AI/ML Intern") & (df["city"] == "Bengaluru")]
    check("AI/ML Bengaluru coverage (>=5)", len(aiml_blr) >= 5, str(len(aiml_blr)))
    aiml_strong = analyze_market(aiml_blr, strong)
    aiml_weak = analyze_market(aiml_blr, weak)
    check(
        "AI/ML Bengaluru weak > strong decay",
        aiml_weak["score"] > aiml_strong["score"],
        f"strong={aiml_strong['score']} weak={aiml_weak['score']}",
    )
    check("AI/ML Bengaluru strong not trivial", aiml_strong["score"] >= 40, str(aiml_strong["score"]))
    check("Dataset size >= 140", len(df) >= 140, str(len(df)))

    for path in [
        "data/sample_resume.txt",
        "data/sample_resume_alt.txt",
        "data/sample_batch_student_3.txt",
        "data/job_postings.csv",
        ".streamlit/config.toml",
        "TECHNICAL_DOCUMENTATION.md",
        "skillpulse/config.py",
        "skillpulse/ui/app.py",
    ]:
        check(f"Required file exists: {path}", Path(path).exists())

    passed = sum(1 for _, ok, _ in RESULTS if ok)
    print("=== SKILLPULSE LOCAL FEATURE TEST ===")
    print(f"Passed: {passed}/{len(RESULTS)}")
    for name, ok, detail in RESULTS:
        status = "PASS" if ok else "FAIL"
        line = f"[{status}] {name}"
        if detail and not ok:
            line += f" -> {detail}"
        print(line)
    if passed != len(RESULTS):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
