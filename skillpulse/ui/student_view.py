"""Student mode dashboard and tabs."""
from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from skillpulse.charts import (
    build_benchmark_radar,
    build_career_path_chart,
    build_history_chart,
    build_monthly_trend_chart,
    build_openings_chart,
    build_radar_chart,
    build_resume_gauge,
    build_salary_chart,
    build_salary_city_chart,
    build_skill_gap_chart,
    build_trend_chart,
)
from skillpulse.config import BENCHMARK_PROFILES, LEARNING_RESOURCES, PROJECT_MAP
from skillpulse.curriculum import build_proof_pack, generate_micro_curriculum, roadmap_for_skills
from skillpulse.gemini_curriculum import resolve_gemini_curriculum, show_gemini_setup_hint
from skillpulse.market import (
    analyze_market,
    build_market_alert,
    compute_resume_compatibility,
    format_salary_lpa,
    score_label,
)
from skillpulse.reports import generate_pdf_report
from skillpulse.skills import extract_skills, get_learning_resources
from skillpulse.snapshots import (
    build_profile_key,
    build_snapshot_delta,
    export_history_csv,
    get_profile_history,
    record_snapshot,
)
from skillpulse.ui.components import display_skill_tags_html


def _next_action_line(analysis: dict, proof_pack: dict) -> str:
    missing = analysis.get("missing") or []
    if not missing:
        return "Your profile covers the current high-demand set. Maintain proof with one portfolio update this week."
    top = html.escape(missing[0])
    title = html.escape(str(proof_pack.get("title", "a focused proof project")))
    return f"Priority gap: <strong>{top}</strong>. Build this next: {title}."


def _hero_status(score: int) -> str:
    label = score_label(score)
    if score >= 75:
        return f"High decay risk ({score}/100, {label})"
    if score >= 45:
        return f"Moderate decay risk ({score}/100, {label})"
    return f"Low decay risk ({score}/100, {label})"


def render_student_view(
    jobs_df: pd.DataFrame,
    role: str,
    city: str,
    profile_text: str,
    portfolio_source: str,
    github_data: dict[str, object],
) -> None:
    filtered_jobs = jobs_df[(jobs_df["role"] == role) & (jobs_df["city"] == city)].copy()
    if filtered_jobs.empty:
        st.error("No job postings available for this role/city combination in the current dataset.")
        st.stop()

    if not profile_text.strip() and not portfolio_source.strip() and not github_data.get("username"):
        st.markdown(
            '<div class="sp-hero"><h2>Start with a profile</h2>'
            "<p>Upload a resume or load a sample in the sidebar, then click <strong>Apply profile</strong>. "
            "SkillPulse compares your skills against current hiring signals for the selected role and city.</p></div>",
            unsafe_allow_html=True,
        )
        st.caption("Tip: use **Sample (Strong match)** or **Sample (Weak match)** for a fast demo.")

    github_profile_text = ""
    if github_data.get("summary"):
        github_profile_text += f"\nGitHub bio: {github_data['summary']}"
    if github_data.get("repos"):
        github_profile_text += "\nRecent repositories:\n- " + "\n- ".join(github_data["repos"])
    if github_data.get("skills"):
        github_profile_text += "\nGitHub-detected skills: " + ", ".join(github_data["skills"])

    profile_context = profile_text
    if portfolio_source.strip():
        profile_context = f"{profile_text}\n{portfolio_source.strip()}"
    if github_profile_text.strip():
        profile_context = f"{profile_context}\n{github_profile_text}".strip()

    student_skills = extract_skills(profile_context)
    analysis = analyze_market(filtered_jobs, student_skills)
    roadmap = roadmap_for_skills(analysis["missing"])
    proof_pack = build_proof_pack(analysis["missing"], student_skills)
    compatibility_data = compute_resume_compatibility(student_skills, analysis["required_skills"], profile_context, role)
    market_alert = build_market_alert(analysis, student_skills, role, portfolio_source.strip())
    micro_curriculum = generate_micro_curriculum(analysis["missing"])

    missing_key = ",".join(analysis["missing"][:3]) if analysis["missing"] else ""
    skills_key = ",".join(student_skills)

    profile_key = build_profile_key(profile_context, role, city, str(github_data.get("username", "")))
    record_snapshot(profile_key, role, city, analysis, compatibility_data, student_skills)
    history_df = get_profile_history(profile_key)
    snapshot_delta = build_snapshot_delta(history_df)

    salary_jobs = filtered_jobs[(filtered_jobs["salary_min"] > 0) & (filtered_jobs["salary_max"] > 0)]
    if not salary_jobs.empty:
        sal_avg_min = int(salary_jobs["salary_min"].mean())
        sal_avg_max = int(salary_jobs["salary_max"].mean())
        sal_overall_min = int(salary_jobs["salary_min"].min())
        sal_overall_max = int(salary_jobs["salary_max"].max())
    else:
        sal_avg_min = sal_avg_max = sal_overall_min = sal_overall_max = 0
    total_positions = int(filtered_jobs["positions"].sum())
    salary_summary = {
        "avg_min": format_salary_lpa(sal_avg_min),
        "avg_max": format_salary_lpa(sal_avg_max),
        "overall_min": format_salary_lpa(sal_overall_min),
        "overall_max": format_salary_lpa(sal_overall_max),
        "total_positions": total_positions,
    }

    hero_title = html.escape(_hero_status(analysis["score"]))
    evidence_preview = analysis.get("evidence_cards") or []
    top_evidence = html.escape(evidence_preview[0]) if evidence_preview else "Waiting for enough job-signal volume to form evidence."
    next_action = _next_action_line(analysis, proof_pack)
    st.markdown(
        f'<div class="sp-hero"><h2>{hero_title}</h2>'
        f"<p><strong>{html.escape(role)}</strong> in <strong>{html.escape(city)}</strong> | "
        f"{len(filtered_jobs)} postings | {len(analysis['matched'])} skills matched | "
        f"{len(analysis['missing'])} high-demand gaps</p>"
        f"<p style='margin-top:0.45rem'>{top_evidence}</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="sp-next">{next_action}</div>', unsafe_allow_html=True)

    metrics = st.columns(4)
    metrics[0].metric("Decay Risk", f"{analysis['score']}/100", score_label(analysis["score"]))
    metrics[1].metric("Resume Compatibility", f"{compatibility_data['overall']}%")
    metrics[2].metric("Market Matches", len(analysis["matched"]))
    metrics[3].metric("Missing Skills", len(analysis["missing"]))
    st.caption(
        f"Trend window: recent postings since **{analysis['recent_cutoff'].date()}** vs older postings."
    )

    tab_overview, tab_market, tab_fit, tab_plan, tab_grow = st.tabs([
        "Overview",
        "Market Evidence",
        "Fit & Roadmap",
        "Plan & Progress",
        "Grow",
    ])

    with tab_overview:
        left, right = st.columns([1.1, 0.9])
        with left:
            st.markdown('<p class="section-header">You vs market demand</p>', unsafe_allow_html=True)
            st.plotly_chart(build_radar_chart(student_skills, analysis["required_skills"]), width="stretch")
            st.markdown('<p class="section-header">Skill gaps</p>', unsafe_allow_html=True)
            if analysis["matched"] or analysis["missing"]:
                st.plotly_chart(build_skill_gap_chart(analysis["matched"], analysis["missing"]), width="stretch")
            else:
                st.caption("No skill gap chart yet. Add profile text to detect skills.")
        with right:
            st.markdown('<p class="section-header">Detected skills</p>', unsafe_allow_html=True)
            display_skill_tags_html(student_skills, "skill-matched", "No recognizable skills found yet.")
            st.markdown('<p class="section-header">Matched</p>', unsafe_allow_html=True)
            display_skill_tags_html(analysis["matched"], "skill-matched", "No strong market matches yet.")
            st.markdown('<p class="section-header">Missing (high demand)</p>', unsafe_allow_html=True)
            display_skill_tags_html(analysis["missing"], "skill-missing", "No major market gaps detected.")
            st.markdown('<p class="section-header">Market evidence</p>', unsafe_allow_html=True)
            if analysis.get("evidence_cards"):
                for card in analysis["evidence_cards"][:5]:
                    st.markdown(f'<div class="sp-evidence">{html.escape(card)}</div>', unsafe_allow_html=True)
            else:
                st.caption("Not enough trend data to build evidence lines yet.")
            if analysis["explanations"]:
                st.markdown('<p class="section-header">Why demand is shifting</p>', unsafe_allow_html=True)
                for line in analysis["explanations"]:
                    st.markdown(f"- {line}")

        with st.expander("How decay risk is calculated"):
            st.markdown(
                """
                Decay risk (0–100) rises when:
                1. **Gap ratio**: more of the role's required skills are missing from your profile.
                2. **Rising misses**: skills trending up in recent job posts are also missing.
                3. **Baseline penalty**: weaker coverage of the required set adds a fixed lift.

                Weights are intentionally soft so thicker markets (more postings) do not clamp every profile to 100.
                It is a **relative signal for this role × city dataset**, not a universal employability score.
                Lower is better. Pair it with Resume Compatibility and the evidence lines above.
                """
            )

    with tab_market:
        st.markdown('<p class="section-header">Skill demand: recent vs previous</p>', unsafe_allow_html=True)
        st.plotly_chart(build_trend_chart(analysis), width="stretch")
        col_rise, col_decay = st.columns(2)
        with col_rise:
            st.markdown("**Rising skills**")
            rising_df = analysis["rising"][["skill", "recent_mentions", "previous_mentions", "delta"]].copy()
            rising_df.columns = ["Skill", "Recent", "Previous", "Trend Delta"]
            st.dataframe(rising_df, width="stretch", hide_index=True)
        with col_decay:
            st.markdown("**Declining skills**")
            decline_df = analysis["declining"][["skill", "recent_mentions", "previous_mentions", "delta"]].copy()
            decline_df.columns = ["Skill", "Recent", "Previous", "Trend Delta"]
            st.dataframe(decline_df, width="stretch", hide_index=True)

        st.markdown('<p class="section-header">Month-over-month skill trends</p>', unsafe_allow_html=True)
        if not analysis["monthly_df"].empty:
            st.plotly_chart(build_monthly_trend_chart(analysis["monthly_df"]), width="stretch")
        else:
            st.caption("Not enough monthly data to show trends.")
        if analysis.get("monthly_stability"):
            st.markdown("**Most stable skills across months**")
            for item in analysis["monthly_stability"][:5]:
                st.caption(f"- {item['skill']}: stability {item['stability']} ({item['months_seen']} month(s))")
        if analysis["new_this_month"]:
            st.markdown("**New this month**")
            display_skill_tags_html(analysis["new_this_month"], "skill-rising", "")
        else:
            st.caption("No new skills emerged this month compared to last month.")

        st.markdown('<p class="section-header">Salary & openings</p>', unsafe_allow_html=True)
        sal_cols = st.columns(4)
        sal_cols[0].metric("Avg Min Salary", salary_summary["avg_min"])
        sal_cols[1].metric("Avg Max Salary", salary_summary["avg_max"])
        sal_cols[2].metric("Lowest Offered", salary_summary["overall_min"])
        sal_cols[3].metric("Highest Offered", salary_summary["overall_max"])
        sal_left, sal_right = st.columns(2)
        with sal_left:
            st.caption("Salary by company")
            st.plotly_chart(build_salary_chart(filtered_jobs), width="stretch")
        with sal_right:
            st.caption(f"Salary across cities for {role}")
            st.plotly_chart(build_salary_city_chart(jobs_df, role), width="stretch")
        open_cols = st.columns(3)
        open_cols[0].metric(f"Positions in {city}", total_positions)
        open_cols[1].metric(f"All-city {role} positions", int(jobs_df[jobs_df["role"] == role]["positions"].sum()))
        open_cols[2].metric("Unique companies", filtered_jobs["company"].nunique())
        st.plotly_chart(build_openings_chart(jobs_df, role), width="stretch")

    with tab_fit:
        st.markdown('<p class="section-header">Resume compatibility</p>', unsafe_allow_html=True)
        compat_left, compat_right = st.columns([1, 1.2])
        with compat_left:
            st.plotly_chart(build_resume_gauge(compatibility_data["overall"]), width="stretch")
            if compatibility_data["overall"] >= 70:
                st.success("Strong alignment with current market requirements for this role.")
            elif compatibility_data["overall"] >= 40:
                st.warning("Moderate alignment. Closing the missing skills below will lift fit.")
            else:
                st.error("Low alignment. Focus on the highest-demand gaps first.")
        with compat_right:
            st.markdown("**Score breakdown**")
            for label, key, caption in [
                ("Skill Match", "skill_match", "Share of market-required skills present in your profile."),
                ("Keyword Density", "keyword_density", "Coverage of in-demand keywords in your text."),
                ("Profile Completeness", "completeness", "Structure, detail, and quantifiable outcomes."),
                ("Role Alignment", "role_alignment", "How tightly the profile targets this role."),
            ]:
                st.markdown(f"**{label}**: `{compatibility_data[key]}%`")
                st.progress(compatibility_data[key] / 100)
                st.caption(caption)
            if github_data.get("username"):
                st.markdown("**GitHub overlay**")
                st.caption(f"Public signals from `@{github_data['username']}` are included in the profile context.")
                if github_data.get("evidence"):
                    with st.expander("GitHub skill evidence"):
                        for item in github_data["evidence"][:8]:
                            st.markdown(f"- **{item['skill']}**: {item['detail']} ({item['sources']})")

        road_left, road_right = st.columns(2)
        with road_left:
            st.markdown('<p class="section-header">7-day roadmap</p>', unsafe_allow_html=True)
            for item in roadmap:
                st.markdown(f"**{item['day']}: {item['focus']}**")
                st.write(item["task"])
                st.divider()
        with road_right:
            st.markdown('<p class="section-header">Proof pack</p>', unsafe_allow_html=True)
            st.markdown(f"**Project:** `{proof_pack['title']}`")
            st.write(proof_pack["idea"])
            st.success(proof_pack["resume_bullet"])
            st.code(proof_pack["github_blurb"], language=None)

        st.markdown('<p class="section-header">Download report</p>', unsafe_allow_html=True)
        report_md = "\n".join([
            "# SkillPulse Report",
            f"- Role: {role}",
            f"- City: {city}",
            f"- Job postings analyzed: {len(filtered_jobs)}",
            f"- Total positions: {total_positions}",
            f"- Salary range: {salary_summary['avg_min']} - {salary_summary['avg_max']}",
            f"- Skill decay risk: {analysis['score']}/100 ({score_label(analysis['score'])})",
            f"- Resume compatibility: {compatibility_data['overall']}%",
            "",
            "## Your Skills",
            ", ".join(student_skills) if student_skills else "None detected",
            "",
            "## Matched Skills",
            ", ".join(analysis["matched"]) if analysis["matched"] else "None",
            "",
            "## Missing High-Demand Skills",
            ", ".join(analysis["missing"]) if analysis["missing"] else "None",
            "",
            "## Top Trending Signals",
            "\n".join([f"- {line}" for line in analysis["explanations"]]) if analysis["explanations"] else "None",
            "",
            "## Resume Compatibility Breakdown",
            f"- Overall: {compatibility_data['overall']}%",
            f"- Skill Match: {compatibility_data['skill_match']}%",
            f"- Keyword Density: {compatibility_data['keyword_density']}%",
            f"- Completeness: {compatibility_data['completeness']}%",
            f"- Role Alignment: {compatibility_data['role_alignment']}%",
            "",
            "## 7-Day Roadmap",
            "\n".join([f"- **{item['day']}**: {item['focus']} -- {item['task']}" for item in roadmap]),
            "",
            "## Proof Pack",
            f"- Title: {proof_pack['title']}",
            f"- Idea: {proof_pack['idea']}",
            f"- Resume Bullet: {proof_pack['resume_bullet']}",
            f"- GitHub Blurb: {proof_pack['github_blurb']}",
        ])
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                "Download Report (Markdown)",
                data=report_md.encode("utf-8"),
                file_name="skillpulse_report.md",
                mime="text/markdown",
            )
        with dl_col2:
            pdf_bytes = generate_pdf_report(
                role, city, filtered_jobs, analysis, roadmap, proof_pack,
                compatibility_data, student_skills, salary_summary,
            )
            if pdf_bytes:
                st.download_button(
                    "Download Report (PDF)",
                    data=pdf_bytes,
                    file_name="skillpulse_report.pdf",
                    mime="application/pdf",
                )
            else:
                st.caption("Install `fpdf2` for PDF report downloads.")

    with tab_plan:
        st.markdown('<p class="section-header">Market shift alert</p>', unsafe_allow_html=True)
        st.warning(market_alert["title"])
        st.write(market_alert["body"])

        st.markdown('<p class="section-header">Profile snapshot history</p>', unsafe_allow_html=True)
        if len(history_df) >= 1:
            st.plotly_chart(build_history_chart(history_df), width="stretch")
            if snapshot_delta.get("has_delta"):
                st.info(snapshot_delta["explanation"])
            elif len(history_df) == 1:
                st.caption("First snapshot for this profile/role pair. Revisit after skill updates to see progress.")
            else:
                st.caption(str(snapshot_delta.get("message", "")))
            st.download_button(
                "Export Snapshot History (CSV)",
                data=export_history_csv(history_df).encode("utf-8"),
                file_name=f"skillpulse_history_{role.replace(' ', '_')}_{city}.csv",
                mime="text/csv",
            )

        st.markdown('<p class="section-header">Micro-curriculum</p>', unsafe_allow_html=True)
        st.caption("Short, proof-oriented lessons from the strongest missing market signals.")
        for block in micro_curriculum:
            with st.expander(block["skill"], expanded=block["skill"] == micro_curriculum[0]["skill"]):
                for idx, lesson in enumerate(block["lessons"], start=1):
                    st.markdown(f"{idx}. {lesson}")
                if block["resources"]:
                    st.markdown("**Suggested resources**")
                    for resource in block["resources"]:
                        st.markdown(
                            f"- [{resource['title']}]({resource['url']}): {resource['type']} ({resource['time']})"
                        )

        st.markdown('<p class="section-header">AI study plan (optional)</p>', unsafe_allow_html=True)
        st.caption("On-demand Gemini plan with weekly milestones. Offline fallback works without an API key.")
        request_gemini = st.button("Generate AI study plan", key="generate_gemini_btn")
        gemini_curriculum, gemini_status = resolve_gemini_curriculum(
            missing_key, role, city, skills_key, request_gemini
        )
        st.caption(gemini_status)
        if gemini_curriculum:
            st.markdown(gemini_curriculum)
        elif show_gemini_setup_hint(gemini_status):
            st.caption("Optional: set `GEMINI_API_KEY` in Streamlit secrets or environment variables for live generation.")

    with tab_grow:
        st.markdown('<p class="section-header">Learning resources</p>', unsafe_allow_html=True)
        target_skills = analysis["missing"] if analysis["missing"] else list(LEARNING_RESOURCES.keys())[:3]
        for skill in target_skills:
            resources = get_learning_resources(skill)
            with st.expander(skill, expanded=skill == target_skills[0]):
                for resource in resources:
                    st.markdown(
                        f"**{resource['title']}** ({resource['type']}, {resource['time']})  \n"
                        f"[Open resource]({resource['url']})"
                    )
                    st.divider()

        st.markdown('<p class="section-header">Career path</p>', unsafe_allow_html=True)
        st.plotly_chart(build_career_path_chart(role, student_skills), width="stretch")

        st.markdown('<p class="section-header">Benchmark: you vs placed profile</p>', unsafe_allow_html=True)
        benchmark = BENCHMARK_PROFILES.get(role)
        if not benchmark:
            closest_key = next(
                (k for k in BENCHMARK_PROFILES if k.lower() in role.lower() or role.lower() in k.lower()),
                None,
            )
            benchmark = BENCHMARK_PROFILES.get(closest_key) if closest_key else list(BENCHMARK_PROFILES.values())[0]

        st.caption(f"**{benchmark['label']}**: {benchmark['summary']}")
        bench_left, bench_right = st.columns([1.2, 0.8])
        with bench_left:
            st.plotly_chart(build_benchmark_radar(student_skills, benchmark["skills"]), width="stretch")
        with bench_right:
            your_set = set(student_skills)
            bench_set = set(benchmark["skills"])
            common = sorted(your_set & bench_set)
            you_only = sorted(your_set - bench_set)
            they_only = sorted(bench_set - your_set)
            st.markdown("**Shared**")
            display_skill_tags_html(common, "skill-matched", "No overlap yet.")
            st.markdown("**Only you**")
            display_skill_tags_html(you_only, "skill-benchmark", "None. The benchmark already covers your set.")
            st.markdown("**Only benchmark**")
            display_skill_tags_html(they_only, "skill-missing", "You already match the benchmark.")

        if they_only:
            st.markdown("**To close the gap**")
            for i, skill in enumerate(they_only[:5], 1):
                project = PROJECT_MAP.get(skill, f"Build a hands-on project demonstrating {skill}.")
                st.markdown(f"{i}. **{skill}**: {project}")

        if benchmark["skills"]:
            readiness = round(len(common) / len(benchmark["skills"]) * 100)
            color = "success" if readiness >= 70 else "warning" if readiness >= 40 else "error"
            getattr(st, color)(
                f"Benchmark readiness: **{readiness}%** ({len(common)}/{len(benchmark['skills'])} skills matched)"
            )

    _render_bottom_expanders(filtered_jobs, role, city, jobs_df)


def _render_bottom_expanders(filtered_jobs: pd.DataFrame, role: str, city: str, jobs_df: pd.DataFrame) -> None:
    with st.expander("Compare two profiles"):
        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            profile_a = st.text_area("Profile A", height=180, key="comp_a")
        with comp_col2:
            profile_b = st.text_area("Profile B", height=180, key="comp_b")
        if profile_a.strip() and profile_b.strip():
            skills_a = extract_skills(profile_a)
            skills_b = extract_skills(profile_b)
            analysis_a = analyze_market(filtered_jobs, skills_a)
            analysis_b = analyze_market(filtered_jobs, skills_b)
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("**Profile A**")
                st.metric("Skills Detected", len(skills_a))
                st.metric("Market Matches", len(analysis_a["matched"]))
                st.metric("Decay Risk", f"{analysis_a['score']}/100")
            with res_col2:
                st.markdown("**Profile B**")
                st.metric("Skills Detected", len(skills_b))
                st.metric("Market Matches", len(analysis_b["matched"]))
                st.metric("Decay Risk", f"{analysis_b['score']}/100")

    with st.expander("Who this is for"):
        st.markdown(
            """
            Students can see which skills still match hiring demand.
            Placement teams get one market view across a batch.
            Early-career seekers get gaps turned into a concrete portfolio plan.
            """
        )

    with st.expander("Evidence & sources"):
        st.markdown(
            """
            - Analysis is driven by the curated (or live-refreshed) job dataset for the selected role and city.
            - External references support product rationale only; they do not override posting-level counts.
            """
        )
