"""Optional Gemini curriculum generation with offline fallback."""
from __future__ import annotations

import time

import requests
import streamlit as st

from skillpulse.config import PROJECT_MAP
from skillpulse.curriculum import generate_micro_curriculum
from skillpulse.secrets import get_secret
from skillpulse.skills import get_learning_resources


def build_fallback_curriculum(missing_key: str, role: str, city: str, skills_key: str) -> str:
    focus_skills = missing_key.split(",") if missing_key else ["Power BI", "SQL", "Prompt Engineering"]
    focus_skills = [skill for skill in focus_skills if skill]
    student_skills = [skill for skill in skills_key.split(",") if skill] if skills_key else []
    blocks = generate_micro_curriculum(focus_skills)
    lines = [
        "# Built-in Micro-Curriculum (Offline Fallback)",
        "",
        f"**Target role:** {role}",
        f"**City:** {city}",
        f"**Current skills:** {', '.join(student_skills) if student_skills else 'None detected'}",
        "",
        "## Goal",
        "Close the top missing market gaps with a proof-oriented 4-week plan.",
        "",
        "## Weekly Milestones",
        "- **Week 1:** Study core concepts and complete one guided tutorial per focus skill.",
        "- **Week 2:** Build small hands-on exercises and document learnings.",
        "- **Week 3:** Integrate skills into one mini project with measurable outcomes.",
        "- **Week 4:** Publish proof artifacts (README, demo, resume bullet).",
        "",
        "## Focus Skills",
    ]
    for block in blocks:
        lines.append(f"### {block['skill']}")
        for idx, lesson in enumerate(block["lessons"], start=1):
            lines.append(f"{idx}. {lesson}")
        if block["resources"]:
            lines.append("")
            lines.append("**Resources:**")
            for resource in block["resources"]:
                lines.append(f"- [{resource['title']}]({resource['url']}) ({resource['type']}, {resource['time']})")
        lines.append("")
    proof_skill = focus_skills[0] if focus_skills else "Power BI"
    lines.extend([
        "## Proof Project",
        PROJECT_MAP.get(proof_skill, f"Build a portfolio project demonstrating {proof_skill}."),
        "",
        "## Portfolio Outcomes",
        "1. One published GitHub repository with a clear README.",
        "2. One resume bullet quantifying impact from the proof project.",
    ])
    return "\n".join(lines)


@st.cache_data(show_spinner="Generating Gemini curriculum...", ttl=3600)
def generate_gemini_curriculum(missing_key: str, role: str, city: str, skills_key: str) -> tuple[str | None, str | None]:
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        fallback = build_fallback_curriculum(missing_key, role, city, skills_key)
        return fallback, "Gemini key not detected. Showing built-in fallback curriculum."

    model_name = get_secret("GEMINI_MODEL", "gemini-2.5-flash")
    focus_skills = missing_key.split(",") if missing_key else ["Power BI", "SQL", "Prompt Engineering"]
    student_skills = skills_key.split(",") if skills_key else []
    resource_lines = []
    for skill in focus_skills[:3]:
        if not skill:
            continue
        for resource in get_learning_resources(skill)[:1]:
            resource_lines.append(f"- {skill}: {resource['title']} ({resource['url']})")

    prompt = f"""
You are helping generate a concise, practical micro-curriculum for an early-career candidate.

Target role: {role}
City: {city}
Current detected skills: {", ".join(student_skills) if student_skills else "None"}
Missing high-demand skills: {", ".join(focus_skills)}

Create a 4-week proof-oriented learning plan in markdown with these sections:
1. Goal
2. Weekly milestones (Week 1 through Week 4 with concrete deliverables)
3. 3 learning steps for the top missing skills
4. 1 mini proof project idea tied to the role
5. 2 concrete portfolio outcomes
6. Resource links section with at least 2 URLs

Keep it realistic, concise, and suitable for a student project demo.
Suggested resources:
{chr(10).join(resource_lines) if resource_lines else "Use well-known free learning resources."}
""".strip()

    response = None
    last_error = None
    for attempt in range(3):
        try:
            response = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent",
                params={"key": api_key},
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30,
            )
        except requests.RequestException as error:
            last_error = str(error)
            response = None
        if response is not None and response.ok:
            break
        if response is not None and response.status_code != 503:
            break
        if attempt < 2:
            time.sleep(1.5 * (attempt + 1))

    if response is None:
        fallback = build_fallback_curriculum(missing_key, role, city, skills_key)
        return fallback, f"Gemini request failed: {last_error or 'Unknown network error.'} Showing fallback curriculum."

    if not response.ok:
        fallback = build_fallback_curriculum(missing_key, role, city, skills_key)
        if response.status_code == 503:
            return fallback, "Gemini is temporarily unavailable. Showing built-in fallback curriculum."
        return fallback, f"Gemini API error {response.status_code}. Showing built-in fallback curriculum."

    data = response.json()
    candidates = data.get("candidates") or []
    if not candidates:
        fallback = build_fallback_curriculum(missing_key, role, city, skills_key)
        return fallback, "Gemini returned no candidates. Showing built-in fallback curriculum."

    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [part.get("text", "") for part in parts if part.get("text")]
    generated = "\n".join(text_parts).strip()
    if not generated:
        fallback = build_fallback_curriculum(missing_key, role, city, skills_key)
        return fallback, "Gemini returned an empty response. Showing built-in fallback curriculum."

    return generated, None


def show_gemini_setup_hint(gemini_status: str) -> bool:
    lowered = gemini_status.lower()
    return "key not detected" in lowered or "api key" in lowered


def resolve_gemini_curriculum(
    missing_key: str,
    role: str,
    city: str,
    skills_key: str,
    request_generation: bool,
) -> tuple[str | None, str]:
    cache_key = f"{missing_key}|{role}|{city}|{skills_key}"
    if "gemini_cache_key" not in st.session_state:
        st.session_state.gemini_cache_key = ""
        st.session_state.gemini_curriculum = None
        st.session_state.gemini_status = "Click **Generate AI study plan** for an optional AI-enhanced curriculum."

    if request_generation:
        try:
            curriculum, error = generate_gemini_curriculum(missing_key, role, city, skills_key)
            st.session_state.gemini_cache_key = cache_key
            st.session_state.gemini_curriculum = curriculum
            st.session_state.gemini_status = (
                "Gemini live generation enabled." if error is None else (error or "Showing built-in fallback curriculum.")
            )
        except Exception as error:
            st.session_state.gemini_curriculum = build_fallback_curriculum(missing_key, role, city, skills_key)
            st.session_state.gemini_status = f"Gemini request failed: {error}. Showing built-in fallback curriculum."
    elif st.session_state.gemini_cache_key != cache_key:
        st.session_state.gemini_cache_key = cache_key
        st.session_state.gemini_curriculum = None
        st.session_state.gemini_status = "Click **Generate AI study plan** for an optional AI-enhanced curriculum."

    return st.session_state.gemini_curriculum, st.session_state.gemini_status
