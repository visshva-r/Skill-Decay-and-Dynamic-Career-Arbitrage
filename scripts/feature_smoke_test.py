"""Local feature smoke test for SkillPulse (logic + export layer)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pandas as pd

import app

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))


def main() -> None:
    df = app.load_jobs()
    check("Dataset loads (88 rows)", len(df) == 88, str(len(df)))
    roles = sorted(df["role"].unique())
    cities = sorted(df["city"].unique())
    check("8 roles present", len(roles) == 8, ", ".join(roles))
    check("7 cities present", len(cities) == 7, ", ".join(cities))
    check("FinTech role data", "FinTech Analyst" in roles)
    check("Healthcare role data", "Healthcare Data Analyst" in roles)
    check("Mumbai and Delhi data", "Mumbai" in cities and "Delhi" in cities)

    strong = app.extract_skills(Path("data/sample_resume.txt").read_text(encoding="utf-8"))
    weak = app.extract_skills(Path("data/sample_resume_alt.txt").read_text(encoding="utf-8"))
    check("Strong profile skill extraction", len(strong) >= 5, ", ".join(strong[:6]))
    check("Weak profile skill extraction", len(weak) >= 3, ", ".join(weak))

    for role in ["Junior Data Analyst", "FinTech Analyst", "Healthcare Data Analyst"]:
        city = "Mumbai" if role != "Healthcare Data Analyst" else "Bengaluru"
        jobs = df[(df["role"] == role) & (df["city"] == city)]
        if jobs.empty:
            jobs = df[df["role"] == role].head(8)
        analysis = app.analyze_market(jobs, weak)
        compat = app.compute_resume_compatibility(weak, analysis["required_skills"], "weak profile", role)
        check(f"Market analysis: {role}", analysis["score"] > 0)
        check(f"Compatibility score: {role}", 0 <= compat["overall"] <= 100)

    jobs = df[(df["role"] == "Junior Data Analyst") & (df["city"] == "Chennai")]
    a_strong = app.analyze_market(jobs, strong)
    a_weak = app.analyze_market(jobs, weak)
    check(
        "Weak profile higher decay than strong",
        a_weak["score"] > a_strong["score"],
        f"weak={a_weak['score']} strong={a_strong['score']}",
    )

    analysis = a_weak
    compat = app.compute_resume_compatibility(weak, analysis["required_skills"], "weak", "Junior Data Analyst")
    check("Radar chart builds", app.build_radar_chart(weak, analysis["required_skills"]) is not None)
    check("Trend chart builds", app.build_trend_chart(analysis) is not None)
    check("Gap chart builds", app.build_skill_gap_chart(analysis["matched"], analysis["missing"]) is not None)
    check("Resume gauge builds", app.build_resume_gauge(compat["overall"]) is not None)
    check("Career path chart builds", app.build_career_path_chart("FinTech Analyst", weak) is not None)
    check("Salary chart builds", app.build_salary_chart(jobs) is not None)
    check("Openings chart builds", app.build_openings_chart(df, "Junior Data Analyst") is not None)
    check("Monthly trend chart builds", app.build_monthly_trend_chart(analysis["monthly_df"]) is not None)

    check("7-day roadmap", len(app.roadmap_for_skills(analysis["missing"])) >= 1)
    check("Proof pack", "title" in app.build_proof_pack(analysis["missing"], weak))
    check("Micro curriculum", len(app.generate_micro_curriculum(analysis["missing"])) >= 1)
    check("Market alert", "title" in app.build_market_alert(analysis, weak, "Junior Data Analyst", ""))
    check("Learning resources", len(app.get_learning_resources("Financial Modeling")) >= 2)
    check("Hackathon map", len(app.HACKATHON_MAP) > 0)

    profiles = app.load_demo_batch_profiles()
    batch = app.run_batch_analysis(profiles, "Junior Data Analyst", jobs)
    summary = app.aggregate_batch_summary(batch)
    check("Placement batch analysis (3 students)", len(batch) == 3)
    check("Batch summary metrics", summary["total"] == 3 and summary["high_risk"] >= 1)
    check("Batch decay chart", app.build_batch_decay_chart(batch) is not None)
    check("Batch heatmap", app.build_batch_heatmap(batch) is not None)
    check("Batch CSV export", "student_label" in app.export_batch_csv(batch, "Junior Data Analyst", "Chennai"))
    batch_pdf = app.generate_batch_pdf(batch, summary, "Junior Data Analyst", "Chennai", "Demo Batch")
    ready_pdf = app.generate_readiness_report_pdf(batch, summary, "Junior Data Analyst", "Chennai", "Demo Batch")
    check("Batch PDF export", batch_pdf is not None and len(batch_pdf) > 500)
    check("Readiness PDF export", ready_pdf is not None and len(ready_pdf) > 500)

    check("Compare profiles scoring differs", a_strong["score"] != a_weak["score"])
    bench = app.BENCHMARK_PROFILES.get("FinTech Analyst")
    check("FinTech benchmark profile", bench is not None)
    check("Benchmark radar", app.build_benchmark_radar(weak, bench["skills"]) is not None)

    roadmap = app.roadmap_for_skills(analysis["missing"])
    proof = app.build_proof_pack(analysis["missing"], weak)
    salary_summary = {
        "avg_min": "4.0 LPA",
        "avg_max": "6.0 LPA",
        "overall_min": "3.0 LPA",
        "overall_max": "7.0 LPA",
        "total_positions": 5,
    }
    student_pdf = app.generate_pdf_report(
        "Junior Data Analyst", "Chennai", jobs, analysis, roadmap, proof, compat, weak, salary_summary
    )
    check("Student PDF report", student_pdf is not None and len(student_pdf) > 500)

    check("City alias Bangalore", app.normalize_city_name("Bangalore") == "Bengaluru")
    check("City alias New Delhi", app.normalize_city_name("New Delhi") == "Delhi")
    key = app.build_profile_key("test profile", "Junior Data Analyst", "Chennai", "")
    check("Snapshot history read", isinstance(app.get_profile_history(key), pd.DataFrame))

    for path in [
        "data/sample_resume.txt",
        "data/sample_resume_alt.txt",
        "data/sample_batch_student_3.txt",
        "data/job_postings.csv",
        ".streamlit/config.toml",
        "TECHNICAL_DOCUMENTATION.md",
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
