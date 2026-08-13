"""Roadmap, proof pack, and micro-curriculum generation."""
from __future__ import annotations

from skillpulse.config import MICRO_CURRICULUM_TEMPLATES, PROJECT_MAP
from skillpulse.skills import get_learning_resources


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
        roadmap.append({"day": f"Day {index * 2 - 1}-{index * 2}", "focus": skill, "task": task})
    roadmap.append({"day": "Day 7", "focus": "Proof Pack", "task": "Publish the mini project, write a README, and add one resume bullet with measurable impact."})
    return roadmap


def build_proof_pack(missing: list[str], student_skills: list[str]) -> dict[str, str]:
    target_skill = missing[0] if missing else "Power BI"
    support_skill = missing[1] if len(missing) > 1 else (student_skills[0] if student_skills else "SQL")
    project_title = f"{target_skill} Career Proof Dashboard"
    project_idea = PROJECT_MAP.get(target_skill, f"Build a mini project showing {target_skill} in action with a realistic student-friendly dataset.")
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


def generate_micro_curriculum(missing: list[str]) -> list[dict[str, object]]:
    selected = missing[:3] if missing else ["Power BI", "SQL", "Prompt Engineering"]
    curriculum = []
    for skill in selected:
        resources = get_learning_resources(skill)
        lessons = MICRO_CURRICULUM_TEMPLATES.get(
            skill,
            [
                f"Study the core concepts behind {skill}.",
                f"Build one small hands-on exercise using {skill}.",
                f"Package the result into a visible proof-of-skill artifact.",
            ],
        )
        curriculum.append({"skill": skill, "lessons": lessons, "resources": resources[:2]})
    return curriculum
