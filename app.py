from __future__ import annotations

from collections import Counter
from pathlib import Path
import re

import pandas as pd
import requests
import streamlit as st


DATA_PATH = Path("data/job_postings.csv")
SAMPLE_RESUME_PATH = Path("data/sample_resume.txt")
SAMPLE_RESUME_ALT_PATH = Path("data/sample_resume_alt.txt")
RESUME_VISSHVA_AIML_PATH = Path("data/resume_visshva_aiml_redacted.txt")
RESUME_VISSHVA_SDE_PATH = Path("data/resume_visshva_sde_redacted.txt")
LIVE_CACHE_PATH = Path("data/live_cache.csv")

SKILL_CATALOG = [
    "Excel",
    "SQL",
    "Python",
    "Power BI",
    "Tableau",
    "DAX",
    "Data Cleaning",
    "Data Visualization",
    "Dashboard Storytelling",
    "Dashboard Design",
    "Data Modeling",
    "Statistics",
    "EDA",
    "Business Communication",
    "Communication",
    "Presentation Skills",
    "Business Analysis",
    "Documentation",
    "Reporting",
    "Stakeholder Reporting",
    "KPI Tracking",
    "Data Validation",
    "A/B Testing",
    "Experiment Analysis",
    "ETL Basics",
    "MIS Reporting",
    "Problem Solving",
    "Storytelling",
    "Attention to Detail",
    "LLM-assisted Analytics",
    "Prompt Engineering",
    "TypeScript",
    "Next.js",
    "Tailwind CSS",
    "Node.js",
    "Express.js",
    "REST APIs",
    "Docker",
    "Postman",
    "PostgreSQL",
    "MongoDB",
    "MySQL",
    "Prisma",
    "Supabase",
    "NextAuth.js",
    "HuggingFace Transformers",
    "DistilGPT-2",
    "Scikit-learn",
    "XGBoost",
    "NumPy",
    "Pandas",
    "Flask",
]

SKILL_ALIAS = {
    "powerbi": "Power BI",
    "prompting": "Prompt Engineering",
    "llm analytics": "LLM-assisted Analytics",
    "story telling": "Storytelling",
    "nextjs": "Next.js",
    "tailwind": "Tailwind CSS",
    "typescript": "TypeScript",
    "node": "Node.js",
    "express": "Express.js",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",
    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",
    "huggingface": "HuggingFace Transformers",
}

PROJECT_MAP = {
    "Power BI": "Build a Chennai retail KPI dashboard with filters, drill-down views, and one executive summary page.",
    "Dashboard Storytelling": "Create a business dashboard that ends with three written insights and one recommendation slide.",
    "DAX": "Build a Power BI report using calculated measures for revenue, growth, and customer retention.",
    "LLM-assisted Analytics": "Create an analytics copilot that turns natural language questions into chart suggestions from a CSV file.",
    "Prompt Engineering": "Design prompts for summarizing dataset insights and compare output quality using a fixed rubric.",
    "Data Modeling": "Create a star-schema style mini warehouse for sales data and show how joins improve reporting speed.",
    "A/B Testing": "Analyze a mock marketing campaign and recommend the winning variant using a simple significance check.",
    "TypeScript": "Convert an existing React UI to TypeScript with strict types and robust API error handling.",
    "Next.js": "Build a small Next.js app with SSR/SSG and an authenticated dashboard flow.",
    "Tailwind CSS": "Rebuild a UI with Tailwind and document a small design system (tokens + components).",
    "Docker": "Containerize a small API + UI, document local run steps, and add health checks.",
    "REST APIs": "Build and document a REST API with pagination, validation, and consistent error responses.",
    "HuggingFace Transformers": "Fine-tune or prompt a small transformer model and evaluate outputs with a measurable rubric.",
}


def normalize_token(text: str) -> str:
    return re.sub(r"[^a-z0-9+]+", " ", text.lower()).strip()


def load_jobs() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["posted_date"] = pd.to_datetime(df["posted_date"])
    df["skill_list"] = df["skills"].apply(
        lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
    )
    return df


def _standardize_jobs_df(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {"job_id", "role", "city", "posted_date", "title", "company", "skills"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Job dataset missing columns: {sorted(missing)}")
    df = df.copy()
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["skills"] = df["skills"].fillna("")
    df["skill_list"] = df["skills"].apply(
        lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
    )
    df = df.dropna(subset=["posted_date"])
    return df


@st.cache_data(show_spinner=False)
def load_cached_jobs() -> pd.DataFrame:
    base = load_jobs()
    if LIVE_CACHE_PATH.exists():
        try:
            live = pd.read_csv(LIVE_CACHE_PATH)
            combined = pd.concat([base, live], ignore_index=True)
            return _standardize_jobs_df(combined)
        except Exception:
            return _standardize_jobs_df(base)
    return _standardize_jobs_df(base)


def _dummy_live_fetch(role: str, city: str, limit: int) -> pd.DataFrame:
    raise RuntimeError(
        "Live refresh is not configured. Provide a job API, or upload a live CSV, or use curated mode."
    )


def fetch_live_jobs(role: str, city: str, limit: int) -> pd.DataFrame:
    """
    Expo-safe: hook point for a real job API.

    For tomorrow, this function intentionally fails unless you wire an API.
    The UI provides fallback options (cached + upload), so the demo never breaks.
    """
    _ = requests  # keep dependency explicit for quick wiring later
    return _dummy_live_fetch(role, city, limit)


def extract_skills(text: str) -> list[str]:
    normalized = normalize_token(text)
    found: list[str] = []

    for skill in SKILL_CATALOG:
        if normalize_token(skill) in normalized:
            found.append(skill)

    for alias, canonical in SKILL_ALIAS.items():
        if alias in normalized and canonical not in found:
            found.append(canonical)

    return sorted(found)


def count_skills(rows: pd.DataFrame) -> Counter:
    counter: Counter = Counter()
    for skills in rows["skill_list"]:
        counter.update(skills)
    return counter


def analyze_market(df: pd.DataFrame, student_skills: list[str]) -> dict:
    latest_date = df["posted_date"].max()
    recent_cutoff = latest_date - pd.Timedelta(days=30)

    recent_rows = df[df["posted_date"] >= recent_cutoff]
    previous_rows = df[df["posted_date"] < recent_cutoff]

    recent_counts = count_skills(recent_rows)
    previous_counts = count_skills(previous_rows)

    total_recent = max(len(recent_rows), 1)
    total_previous = max(len(previous_rows), 1)

    required_skills = [skill for skill, count in recent_counts.most_common(10) if count >= 3]
    matched = sorted([skill for skill in student_skills if skill in required_skills])
    missing = sorted([skill for skill in required_skills if skill not in student_skills])

    trend_rows = []
    for skill in sorted(set(recent_counts) | set(previous_counts)):
        recent_rate = recent_counts[skill] / total_recent
        previous_rate = previous_counts[skill] / total_previous
        delta = recent_rate - previous_rate
        trend_rows.append(
            {
                "skill": skill,
                "recent_mentions": recent_counts[skill],
                "previous_mentions": previous_counts[skill],
                "delta": round(delta, 3),
                "recent_rate": recent_rate,
            }
        )

    trend_df = pd.DataFrame(trend_rows).sort_values(
        by=["delta", "recent_mentions"], ascending=[False, False]
    )

    rising = trend_df[trend_df["delta"] > 0].head(5)
    declining = trend_df.sort_values(by=["delta", "previous_mentions"]).head(5)

    gap_ratio = len(missing) / max(len(required_skills), 1)
    rising_missing = sum(1 for skill in rising["skill"].tolist() if skill in missing)
    trend_bonus = min(rising_missing * 8, 24)
    score = min(100, round(gap_ratio * 70 + trend_bonus + 10))

    explanations = []
    for _, row in rising.head(3).iterrows():
        explanations.append(
            f"`{row['skill']}` appears in **{int(row['recent_mentions'])}/{total_recent}** recent postings "
            f"vs **{int(row['previous_mentions'])}/{total_previous}** older postings (Δ={row['delta']})."
        )

    return {
        "recent_rows": recent_rows,
        "required_skills": required_skills,
        "matched": matched,
        "missing": missing,
        "rising": rising,
        "declining": declining,
        "score": score,
        "recent_cutoff": recent_cutoff,
        "explanations": explanations,
    }


def roadmap_for_skills(missing: list[str]) -> list[dict[str, str]]:
    default_tasks = [
        "Watch one focused tutorial and take concise notes.",
        "Implement one small hands-on exercise using sample data.",
        "Convert the exercise into a mini portfolio artifact.",
    ]

    roadmap = []
    selected = missing[:3] if missing else ["Power BI", "Dashboard Storytelling", "Prompt Engineering"]

    for index, skill in enumerate(selected, start=1):
        task = PROJECT_MAP.get(skill, default_tasks[(index - 1) % len(default_tasks)])
        roadmap.append(
            {
                "day": f"Day {index * 2 - 1}-{index * 2}",
                "focus": skill,
                "task": task,
            }
        )

    roadmap.append(
        {
            "day": "Day 7",
            "focus": "Proof Pack",
            "task": "Publish the mini project, write a README, and add one resume bullet with measurable impact.",
        }
    )
    return roadmap


def build_proof_pack(missing: list[str], student_skills: list[str]) -> dict[str, str]:
    target_skill = missing[0] if missing else "Power BI"
    support_skill = missing[1] if len(missing) > 1 else (student_skills[0] if student_skills else "SQL")

    project_title = f"{target_skill} Career Proof Dashboard"
    project_idea = PROJECT_MAP.get(
        target_skill,
        f"Build a mini project showing {target_skill} in action with a realistic student-friendly dataset.",
    )
    resume_bullet = (
        f"Built a {target_skill}-focused analytics project integrating {support_skill} to solve a real reporting use case, "
        "documented insights, and packaged the work for recruiter review."
    )

    return {
        "title": project_title,
        "idea": project_idea,
        "resume_bullet": resume_bullet,
        "github_blurb": f"{project_title}: a portfolio project built to demonstrate market-relevant analytics skills for fresher roles.",
    }


def score_label(score: int) -> str:
    if score >= 75:
        return "High risk"
    if score >= 45:
        return "Medium risk"
    return "Low risk"


def display_skill_tags(skills: list[str], empty_text: str) -> None:
    if skills:
        st.write(" | ".join(f"`{skill}`" for skill in skills))
    else:
        st.caption(empty_text)


def main() -> None:
    st.set_page_config(page_title="SkillPulse", page_icon="SP", layout="wide")

    st.title("SkillPulse")
    st.caption(
        "Detect skill decay, compare against current job signals, and generate a proof-oriented roadmap."
    )

    jobs_df = load_cached_jobs()

    with st.sidebar:
        st.header("Demo Setup")
        role = st.selectbox("Target role", sorted(jobs_df["role"].unique()))
        city = st.selectbox("Target city", sorted(jobs_df["city"].unique()))

        st.divider()
        st.subheader("Data Source")
        st.caption("Curated data is always available. Live refresh is optional and cached when it works.")

        uploaded_csv = st.file_uploader("Upload a live jobs CSV (optional)", type=["csv"])
        if uploaded_csv is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_csv)
                jobs_df = _standardize_jobs_df(uploaded_df)
                st.success("Loaded uploaded job dataset.")
            except Exception as e:
                st.error(f"Could not read uploaded CSV: {e}")

        live_limit = st.slider("Live refresh size (optional)", min_value=10, max_value=80, value=30, step=10)
        live_refresh = st.button("Refresh live signals")
        if live_refresh:
            try:
                live_df = fetch_live_jobs(role=role, city=city, limit=live_limit)
                live_df = _standardize_jobs_df(live_df)
                live_df.to_csv(LIVE_CACHE_PATH, index=False)
                st.success("Live refresh complete. Cached for offline demo.")
                st.cache_data.clear()
            except Exception as e:
                st.warning(f"Live refresh not available right now: {e}")

        st.divider()
        st.subheader("Student Profile")
        profile_choice = st.radio(
            "Quick demo profiles",
            options=[
                "Sample (Strong match)",
                "Sample (Weak match)",
                "Resume (Visshva - AIML/Data)",
                "Resume (Visshva - SDE/Full-stack)",
                "Custom paste",
            ],
            index=0,
        )
        if profile_choice == "Sample (Strong match)":
            profile_text = SAMPLE_RESUME_PATH.read_text(encoding="utf-8")
        elif profile_choice == "Sample (Weak match)":
            profile_text = SAMPLE_RESUME_ALT_PATH.read_text(encoding="utf-8")
        elif profile_choice == "Resume (Visshva - AIML/Data)":
            profile_text = RESUME_VISSHVA_AIML_PATH.read_text(encoding="utf-8")
        elif profile_choice == "Resume (Visshva - SDE/Full-stack)":
            profile_text = RESUME_VISSHVA_SDE_PATH.read_text(encoding="utf-8")
        else:
            profile_text = ""

        profile_text = st.text_area(
            "Student profile or resume text",
            value=profile_text,
            height=260,
            help="Paste a resume summary, skills, or project descriptions.",
        )

    filtered_jobs = jobs_df[(jobs_df["role"] == role) & (jobs_df["city"] == city)].copy()
    if filtered_jobs.empty:
        st.error("No job postings available for this role/city combination in the current dataset.")
        st.stop()

    student_skills = extract_skills(profile_text)
    analysis = analyze_market(filtered_jobs, student_skills)
    roadmap = roadmap_for_skills(analysis["missing"])
    proof_pack = build_proof_pack(analysis["missing"], student_skills)

    st.subheader("Product Overview")
    st.info(
        "SkillPulse is a local job-signal engine that detects emerging skill decay and tells students what to build next to prove missing skills."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Job postings analyzed", len(filtered_jobs))
    col2.metric("Matched skills", len(analysis["matched"]))
    col3.metric("Skill decay risk", f"{analysis['score']}/100", score_label(analysis["score"]))

    st.caption(
        f"Trend window: recent postings since **{analysis['recent_cutoff'].date()}** vs older postings."
    )

    left, right = st.columns([1.1, 0.9])

    with left:
        st.subheader("Student Skill Snapshot")
        display_skill_tags(student_skills, "No recognizable skills found in the profile text.")

        st.subheader("Why the market is shifting (Explainability)")
        if analysis["explanations"]:
            for line in analysis["explanations"]:
                st.write(f"- {line}")
        else:
            st.caption("No strong trend explanations found for this dataset window.")

        st.subheader("Market Match")
        match_col, missing_col = st.columns(2)
        with match_col:
            st.markdown("**Matched skills**")
            display_skill_tags(analysis["matched"], "No strong market matches yet.")
        with missing_col:
            st.markdown("**Missing high-demand skills**")
            display_skill_tags(analysis["missing"], "No major market gaps detected.")

        st.subheader("Trending Market Signals")
        rising_df = analysis["rising"][["skill", "recent_mentions", "previous_mentions", "delta"]].copy()
        rising_df.columns = ["Skill", "Recent", "Previous", "Trend Delta"]
        st.dataframe(rising_df, use_container_width=True, hide_index=True)
        if not rising_df.empty:
            chart_df = rising_df.set_index("Skill")[["Recent", "Previous"]]
            st.bar_chart(chart_df, horizontal=True)

        st.subheader("Skill Decay Meter")
        decline_df = analysis["declining"][["skill", "recent_mentions", "previous_mentions", "delta"]].copy()
        decline_df.columns = ["Skill", "Recent", "Previous", "Trend Delta"]
        st.dataframe(decline_df, use_container_width=True, hide_index=True)
        if not decline_df.empty:
            decay_chart_df = decline_df.set_index("Skill")[["Previous", "Recent"]]
            st.bar_chart(decay_chart_df, horizontal=True)

    with right:
        st.subheader("7-Day Micro Roadmap")
        for item in roadmap:
            st.markdown(f"**{item['day']} - {item['focus']}**")
            st.write(item["task"])

        st.subheader("Proof Pack")
        st.markdown(f"**Mini-project title:** `{proof_pack['title']}`")
        st.write(proof_pack["idea"])
        st.markdown(f"**Resume bullet:** {proof_pack['resume_bullet']}")
        st.markdown(f"**GitHub blurb:** {proof_pack['github_blurb']}")

        st.subheader("Downloadable Analysis Report")
        report_md = "\n".join(
            [
                "# SkillPulse Report",
                f"- Role: {role}",
                f"- City: {city}",
                f"- Job postings analyzed: {len(filtered_jobs)}",
                f"- Skill decay risk: {analysis['score']}/100 ({score_label(analysis['score'])})",
                "",
                "## Matched skills",
                ", ".join(analysis["matched"]) if analysis["matched"] else "None",
                "",
                "## Missing high-demand skills",
                ", ".join(analysis["missing"]) if analysis["missing"] else "None",
                "",
                "## Top trending signals",
                "\n".join([f"- {x}" for x in analysis["explanations"]]) if analysis["explanations"] else "None",
                "",
                "## 7-day roadmap",
                "\n".join([f"- **{r['day']}**: {r['focus']} — {r['task']}" for r in roadmap]),
                "",
                "## Proof Pack",
                f"- Title: {proof_pack['title']}",
                f"- Idea: {proof_pack['idea']}",
                f"- Resume bullet: {proof_pack['resume_bullet']}",
                f"- GitHub blurb: {proof_pack['github_blurb']}",
                "",
                "## SDG alignment",
                "- SDG 4 (Quality Education): personalized upskilling roadmap",
                "- SDG 8 (Decent Work & Economic Growth): improved employability for students",
                "",
            ]
        )
        st.download_button(
            "Download report (Markdown)",
            data=report_md.encode("utf-8"),
            file_name="skillpulse_report.md",
            mime="text/markdown",
        )

    with st.expander("Real-World Relevance"):
        st.markdown(
            """
            - **Students:** identify which current skills still align with hiring demand and which ones need reinforcement.
            - **Placement cells:** use one consistent market-signal view to guide multiple students.
            - **Early-career job seekers:** convert missing skills into focused portfolio evidence instead of generic learning plans.
            """
        )

    with st.expander("Reference Case Studies"):
        st.markdown(
            """
            - **Case 1:** a final-year student with `Excel`, `SQL`, and `Python` sees that `Power BI` and `Dashboard Storytelling` are becoming stronger differentiators.
            - **Case 2:** a weakly aligned student with only reporting experience gets a higher risk score and a targeted recovery roadmap.
            - **Case 3:** a placement mentor uses the same role dataset to guide multiple students consistently.
            """
        )

    with st.expander("SDG Alignment"):
        st.markdown(
            """
            - **SDG 4 (Quality Education):** guides students to targeted micro-skills and proof-based learning.
            - **SDG 8 (Decent Work & Economic Growth):** improves employability by aligning skills with real job demand.
            """
        )

    with st.expander("Evidence & Sources (Optional, if asked)"):
        st.markdown(
            """
            - **Business analysis + agentic workflow trends (2026):** ModernAnalyst article on evolving BA responsibilities, governance, provenance, and monitoring.
            - **Skills taxonomy / skills graph concept:** Cornerstone Skills Graph writeup on mapping skills to people, roles, and learning paths.
            - **Workforce upskilling pressure:** Hays skills reporting and related workforce-skilling references.
            - **Important:** the app's analysis comes from the job dataset; these documents support the product rationale, not the live scoring pipeline.
            """
        )


if __name__ == "__main__":
    main()
