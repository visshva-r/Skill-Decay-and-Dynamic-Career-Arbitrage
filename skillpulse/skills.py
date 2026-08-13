"""Skill extraction, normalization, and learning resource lookup."""
from __future__ import annotations

import re
from collections import Counter

import pandas as pd

from skillpulse.config import LEARNING_RESOURCES, SKILL_ALIAS, SKILL_CATALOG


def normalize_token(text: str) -> str:
    return re.sub(r"[^a-z0-9+#]+", " ", text.lower()).strip()


def _skill_in_text(skill_token: str, normalized_text: str) -> bool:
    if len(skill_token) <= 3:
        return bool(re.search(r"(?:^|\s)" + re.escape(skill_token) + r"(?:\s|$)", normalized_text))
    return skill_token in normalized_text


def extract_skills(text: str) -> list[str]:
    normalized = normalize_token(text)
    found: list[str] = []
    for skill in SKILL_CATALOG:
        if _skill_in_text(normalize_token(skill), normalized):
            found.append(skill)
    for alias, canonical in SKILL_ALIAS.items():
        if _skill_in_text(alias, normalized) and canonical not in found:
            found.append(canonical)
    return sorted(found)


def count_skills(rows: pd.DataFrame) -> Counter:
    counter: Counter = Counter()
    for skills in rows["skill_list"]:
        counter.update(skills)
    return counter


def get_learning_resources(skill: str) -> list[dict[str, str]]:
    resources = LEARNING_RESOURCES.get(skill)
    if resources:
        return resources
    query = skill.replace(" ", "+")
    return [
        {
            "title": f"{skill} learning path",
            "url": f"https://www.google.com/search?q={query}+learning+path",
            "type": "Search Guide",
            "time": "Varies",
        },
        {
            "title": f"{skill} hands-on tutorial",
            "url": f"https://www.youtube.com/results?search_query={query}+tutorial",
            "type": "Video Search",
            "time": "Varies",
        },
    ]
