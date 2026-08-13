"""Market analysis, compatibility scoring, and alerts."""
from __future__ import annotations

import re

import pandas as pd

from skillpulse.skills import count_skills, normalize_token


def analyze_market(df: pd.DataFrame, student_skills: list[str]) -> dict:
    latest_date = df["posted_date"].max()
    recent_cutoff = latest_date - pd.Timedelta(days=30)
    recent_rows = df[df["posted_date"] >= recent_cutoff]
    previous_rows = df[df["posted_date"] < recent_cutoff]
    recent_counts = count_skills(recent_rows)
    previous_counts = count_skills(previous_rows)
    total_recent = max(len(recent_rows), 1)
    total_previous = max(len(previous_rows), 1)
    min_count = 2 if len(recent_rows) <= 6 else 3
    required_skills = [skill for skill, count in recent_counts.most_common(10) if count >= min_count]
    if not required_skills:
        required_skills = [skill for skill, _ in recent_counts.most_common(5)]
    matched = sorted([skill for skill in student_skills if skill in required_skills])
    missing = sorted([skill for skill in required_skills if skill not in student_skills])

    trend_rows = []
    for skill in sorted(set(recent_counts) | set(previous_counts)):
        recent_rate = recent_counts[skill] / total_recent
        previous_rate = previous_counts[skill] / total_previous
        delta = recent_rate - previous_rate
        trend_rows.append({
            "skill": skill,
            "recent_mentions": recent_counts[skill],
            "previous_mentions": previous_counts[skill],
            "delta": round(delta, 3),
            "recent_rate": recent_rate,
        })

    trend_df = pd.DataFrame(trend_rows).sort_values(by=["delta", "recent_mentions"], ascending=[False, False])
    rising = trend_df[trend_df["delta"] > 0].head(5)
    declining = trend_df.sort_values(by=["delta", "previous_mentions"]).head(5)
    gap_ratio = len(missing) / max(len(required_skills), 1)
    rising_missing = sum(1 for skill in rising["skill"].tolist() if skill in missing)
    # Soft saturation keeps strong vs weak ordered without clamping both to 100
    # on thicker role×city slices (e.g. AI/ML Intern · Bengaluru).
    trend_bonus = min(rising_missing * 6, 18)
    baseline_penalty = max(0, (len(required_skills) - len(matched)) * 2)
    score = min(
        100,
        round(gap_ratio * 55 + trend_bonus + baseline_penalty + (8 if not student_skills else 4)),
    )

    explanations = []
    evidence_cards: list[str] = []
    for _, row in rising.head(5).iterrows():
        card = (
            f"Skill {row['skill']} in {int(row['recent_mentions'])}/{total_recent} recent "
            f"vs {int(row['previous_mentions'])}/{total_previous} older posts"
        )
        evidence_cards.append(card)
        if len(explanations) < 3:
            explanations.append(
                f"`{row['skill']}` appears in **{int(row['recent_mentions'])}/{total_recent}** recent postings "
                f"vs **{int(row['previous_mentions'])}/{total_previous}** older postings (delta={row['delta']})."
            )

    df_sorted = df.copy()
    df_sorted["month"] = df_sorted["posted_date"].dt.to_period("M")
    months = sorted(df_sorted["month"].unique())
    monthly_skill_data: list[dict] = []
    for month in months:
        month_rows = df_sorted[df_sorted["month"] == month]
        month_counts = count_skills(month_rows)
        for skill, cnt in month_counts.items():
            monthly_skill_data.append({"month": str(month), "skill": skill, "mentions": cnt})
    monthly_df = pd.DataFrame(monthly_skill_data) if monthly_skill_data else pd.DataFrame(columns=["month", "skill", "mentions"])

    monthly_stability: list[dict[str, object]] = []
    if not monthly_df.empty:
        for skill in monthly_df["skill"].unique():
            skill_months = monthly_df[monthly_df["skill"] == skill]["mentions"]
            if len(skill_months) >= 2:
                mean_val = skill_months.mean()
                std_val = skill_months.std()
                stability = round(1 - min(std_val / max(mean_val, 1), 1), 2)
            else:
                stability = 0.0
            monthly_stability.append({"skill": skill, "stability": stability, "months_seen": len(skill_months)})
        monthly_stability = sorted(monthly_stability, key=lambda item: item["stability"], reverse=True)[:10]

    new_this_month: list[str] = []
    if len(months) >= 2:
        current_month_skills = set(count_skills(df_sorted[df_sorted["month"] == months[-1]]).keys())
        prev_month_skills = set(count_skills(df_sorted[df_sorted["month"] == months[-2]]).keys())
        new_this_month = sorted(current_month_skills - prev_month_skills)

    return {
        "recent_rows": recent_rows,
        "previous_rows": previous_rows,
        "required_skills": required_skills,
        "matched": matched,
        "missing": missing,
        "rising": rising,
        "declining": declining,
        "score": score,
        "recent_cutoff": recent_cutoff,
        "explanations": explanations,
        "evidence_cards": evidence_cards,
        "trend_df": trend_df,
        "monthly_df": monthly_df,
        "monthly_stability": monthly_stability,
        "new_this_month": new_this_month,
    }


def compute_resume_compatibility(student_skills: list[str], required_skills: list[str], profile_text: str, role: str) -> dict:
    if required_skills:
        skill_match_pct = len([s for s in student_skills if s in required_skills]) / len(required_skills)
    else:
        skill_match_pct = 0.0
    all_market_skills = set(required_skills)
    keyword_hits = sum(1 for s in student_skills if s in all_market_skills)
    keyword_score = min(keyword_hits / max(len(all_market_skills), 1), 1.0)
    text_len = len(profile_text.strip())
    has_sections = any(kw in profile_text.lower() for kw in ["skills", "projects", "experience", "education", "profile"])
    has_numbers = bool(re.search(r"\d+", profile_text))
    completeness = min(1.0, (text_len / 800) * 0.5 + (0.3 if has_sections else 0) + (0.2 if has_numbers else 0))
    role_tokens = set(normalize_token(role).split())
    profile_norm = normalize_token(profile_text)
    role_hits = sum(1 for token in role_tokens if token in profile_norm)
    role_alignment = min(1.0, role_hits / max(len(role_tokens), 1))
    overall = round(skill_match_pct * 50 + keyword_score * 20 + completeness * 15 + role_alignment * 15)
    return {
        "overall": min(overall, 100),
        "skill_match": round(skill_match_pct * 100),
        "keyword_density": round(keyword_score * 100),
        "completeness": round(completeness * 100),
        "role_alignment": round(role_alignment * 100),
    }


def build_market_alert(analysis: dict, student_skills: list[str], target_role: str, portfolio_source: str) -> dict[str, str]:
    rising_missing = [skill for skill in analysis["rising"]["skill"].tolist() if skill not in student_skills]
    focus_skill = rising_missing[0] if rising_missing else (analysis["missing"][0] if analysis["missing"] else "")
    if not focus_skill:
        return {
            "title": "No critical alert right now",
            "body": f"Your current profile already covers the strongest visible signals for `{target_role}` in this dataset window.",
        }
    row = analysis["trend_df"][analysis["trend_df"]["skill"] == focus_skill].head(1)
    if row.empty:
        evidence = f"`{focus_skill}` is appearing more frequently in the recent market window."
    else:
        row = row.iloc[0]
        evidence = (
            f"`{focus_skill}` appears in {int(row['recent_mentions'])}/{len(analysis['recent_rows']) or 1} recent postings "
            f"vs {int(row['previous_mentions'])}/{len(analysis['previous_rows']) or 1} older postings."
        )
    source_line = f"Based on the provided profile context and portfolio input: `{portfolio_source}`." if portfolio_source else "Based on the provided profile context."
    return {
        "title": f"Market alert: `{focus_skill}` is becoming more important",
        "body": f"{evidence} You do not currently show this skill strongly in your profile. {source_line}",
    }


def score_label(score: int) -> str:
    if score >= 70:
        return "High risk"
    if score >= 40:
        return "Medium risk"
    return "Low risk"


def format_salary_lpa(amount: int) -> str:
    if amount <= 0:
        return "N/A"
    return f"{amount / 100000:.1f} LPA"
