"""GitHub portfolio enrichment with per-skill evidence."""
from __future__ import annotations

import requests
import streamlit as st

from skillpulse.config import DEFAULT_GITHUB_SKILL_MAP
from skillpulse.secrets import get_secret
from skillpulse.skills import extract_skills, normalize_token


def _github_headers() -> dict[str, str]:
    token = get_secret("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "SkillPulse",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _skill_in_text(skill_token: str, normalized_text: str) -> bool:
    import re

    if len(skill_token) <= 3:
        return bool(re.search(r"(?:^|\s)" + re.escape(skill_token) + r"(?:\s|$)", normalized_text))
    return skill_token in normalized_text


@st.cache_data(show_spinner=False, ttl=1800)
def fetch_github_profile_data(username: str) -> dict[str, object]:
    empty = {"username": "", "skills": [], "summary": "", "repos": [], "evidence": []}
    if not username:
        return empty
    headers = _github_headers()
    base_url = f"https://api.github.com/users/{username}"
    try:
        user_response = requests.get(base_url, headers=headers, timeout=15)
        user_response.raise_for_status()
        repos_response = requests.get(f"{base_url}/repos?per_page=6&sort=updated", headers=headers, timeout=20)
        repos_response.raise_for_status()
    except requests.RequestException as error:
        return {
            **empty,
            "username": username,
            "summary": f"GitHub fetch failed: {error}",
        }

    repos = repos_response.json()
    extracted_tokens: list[str] = []
    repo_summaries: list[str] = []
    evidence: list[dict[str, str]] = []
    skill_sources: dict[str, list[str]] = {}

    for repo in repos:
        if repo.get("fork"):
            continue
        repo_name = repo.get("name", "")
        description = repo.get("description") or ""
        topics = repo.get("topics") or []
        language = repo.get("language") or ""
        extracted_tokens.extend([repo_name, description, language, *topics])
        repo_summaries.append(f"{repo_name}: {description or 'No description'}")

        repo_text = normalize_token(" ".join([repo_name, description, language, *topics]))
        for token, canonical in DEFAULT_GITHUB_SKILL_MAP.items():
            if _skill_in_text(normalize_token(token), repo_text):
                source = f"repo:{repo_name}"
                skill_sources.setdefault(canonical, [])
                if source not in skill_sources[canonical]:
                    skill_sources[canonical].append(source)
        for skill in extract_skills(" ".join([repo_name, description, language, *topics])):
            source = f"repo:{repo_name}"
            skill_sources.setdefault(skill, [])
            if source not in skill_sources[skill]:
                skill_sources[skill].append(source)

    normalized_text = normalize_token(" ".join(extracted_tokens))
    detected: list[str] = []
    for token, canonical in DEFAULT_GITHUB_SKILL_MAP.items():
        if _skill_in_text(normalize_token(token), normalized_text) and canonical not in detected:
            detected.append(canonical)
    detected.extend([skill for skill in extract_skills(" ".join(extracted_tokens)) if skill not in detected])

    for skill in sorted(detected):
        sources = skill_sources.get(skill, [])
        evidence.append({
            "skill": skill,
            "sources": "; ".join(sources) if sources else "profile text",
            "detail": f"Detected from {len(sources) or 1} GitHub signal(s)",
        })

    summary = user_response.json().get("bio") or ""
    return {
        "username": username,
        "skills": sorted(detected),
        "summary": summary,
        "repos": repo_summaries[:5],
        "evidence": evidence,
    }
