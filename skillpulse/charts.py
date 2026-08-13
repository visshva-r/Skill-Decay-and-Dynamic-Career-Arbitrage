"""Plotly chart builders for SkillPulse dashboards."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from skillpulse.config import CAREER_PATHS, SKILL_CATEGORIES

# Ink + teal palette (shared across charts)
ACCENT = "#0d9488"
ACCENT_FILL = "rgba(13, 148, 136, 0.14)"
INK = "#0f172a"
SLATE = "#94a3b8"
MATCH = "#059669"
MISS = "#e11d48"
WARN = "#d97706"
MARKET = "#475569"
MARKET_FILL = "rgba(71, 85, 105, 0.10)"


def build_radar_chart(student_skills: list[str], required_skills: list[str]) -> go.Figure:
    categories, student_vals, market_vals = [], [], []
    for category, category_skills in SKILL_CATEGORIES.items():
        student_count = sum(1 for skill in category_skills if skill in student_skills)
        market_count = sum(1 for skill in category_skills if skill in required_skills)
        total = max(len(category_skills), 1)
        categories.append(category)
        student_vals.append(round(student_count / total * 100))
        market_vals.append(round(market_count / total * 100))
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=student_vals + [student_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Your Skills",
        fillcolor=ACCENT_FILL,
        line=dict(color=ACCENT, width=2),
    ))
    fig.add_trace(go.Scatterpolar(
        r=market_vals + [market_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Market Demand",
        fillcolor=MARKET_FILL,
        line=dict(color=MARKET, width=2, dash="dash"),
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_trend_chart(analysis: dict) -> go.Figure:
    trend_df = analysis["trend_df"].head(12).copy()
    if trend_df.empty:
        return go.Figure()
    trend_df = trend_df.sort_values("delta", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=trend_df["skill"],
        x=trend_df["previous_mentions"],
        name="Previous Period",
        orientation="h",
        marker_color=SLATE,
    ))
    fig.add_trace(go.Bar(
        y=trend_df["skill"],
        x=trend_df["recent_mentions"],
        name="Recent Period",
        orientation="h",
        marker_color=ACCENT,
    ))
    fig.update_layout(
        barmode="group",
        height=max(300, len(trend_df) * 35),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Mentions in Job Postings",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_monthly_trend_chart(monthly_df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    fig = go.Figure()
    if monthly_df.empty:
        return fig
    top_skills = monthly_df.groupby("skill")["mentions"].sum().nlargest(top_n).index.tolist()
    filtered = monthly_df[monthly_df["skill"].isin(top_skills)]
    palette = [ACCENT, MARKET, MATCH, WARN, MISS, "#0891b2", "#4f46e5", "#a16207"]
    for index, skill in enumerate(top_skills):
        skill_data = filtered[filtered["skill"] == skill].sort_values("month")
        fig.add_trace(go.Scatter(
            x=skill_data["month"],
            y=skill_data["mentions"],
            mode="lines+markers",
            name=skill,
            line=dict(color=palette[index % len(palette)], width=2),
        ))
    fig.update_layout(
        height=400,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Month",
        yaxis_title="Mentions",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_skill_gap_chart(matched: list[str], missing: list[str]) -> go.Figure:
    skills = matched + missing
    if not skills:
        return go.Figure()
    colors = [MATCH] * len(matched) + [MISS] * len(missing)
    labels = ["Matched"] * len(matched) + ["Missing"] * len(missing)
    fig = go.Figure(go.Bar(
        y=skills,
        x=[1] * len(skills),
        orientation="h",
        marker_color=colors,
        text=labels,
        textposition="inside",
    ))
    fig.update_layout(
        height=max(250, len(skills) * 32),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_resume_gauge(score: int) -> go.Figure:
    color = MATCH if score >= 70 else WARN if score >= 40 else MISS
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Resume Compatibility", "font": {"size": 16, "color": INK}},
        number={"suffix": "%", "font": {"size": 34, "color": INK}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "steps": [
                {"range": [0, 40], "color": "#ffe4e6"},
                {"range": [40, 70], "color": "#fef3c7"},
                {"range": [70, 100], "color": "#d1fae5"},
            ],
        },
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def build_career_path_chart(role: str, student_skills: list[str]) -> go.Figure:
    path_data = next(
        (CAREER_PATHS[key] for key in CAREER_PATHS if key.lower() in role.lower() or role.lower() in key.lower()),
        list(CAREER_PATHS.values())[0],
    )
    labels, parents, values, colors = [path_data["current"]], [""], [100], [ACCENT]
    for path in path_data["paths"]:
        labels.append(f"{path['role']} ({path['years']})")
        parents.append(path_data["current"])
        skill_match = sum(1 for skill in path["key_skills"] if skill in student_skills)
        readiness = round(skill_match / max(len(path["key_skills"]), 1) * 100)
        values.append(readiness)
        colors.append(MATCH if readiness >= 70 else WARN if readiness >= 40 else MISS)
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=[max(value, 10) for value in values],
        marker=dict(colors=colors),
        textinfo="label+text",
        text=[f"Readiness: {value}%" if index > 0 else "You are here" for index, value in enumerate(values)],
    ))
    fig.update_layout(height=350, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def build_history_chart(history_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if history_df.empty:
        return fig
    fig.add_trace(go.Scatter(
        x=history_df["date"],
        y=history_df["compatibility"],
        mode="lines+markers",
        name="Resume Compatibility",
        line=dict(color=ACCENT, width=3),
    ))
    fig.add_trace(go.Scatter(
        x=history_df["date"],
        y=history_df["decay_risk"],
        mode="lines+markers",
        name="Skill Decay Risk",
        line=dict(color=MISS, width=3),
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Score",
        xaxis_title="Snapshot Date",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_salary_chart(filtered_jobs: pd.DataFrame) -> go.Figure:
    salary_jobs = filtered_jobs[(filtered_jobs["salary_min"] > 0) & (filtered_jobs["salary_max"] > 0)].copy()
    if salary_jobs.empty:
        return go.Figure()
    salary_jobs["salary_avg"] = (salary_jobs["salary_min"] + salary_jobs["salary_max"]) / 2
    by_company = salary_jobs.groupby("company").agg(
        avg_min=("salary_min", "mean"), avg_max=("salary_max", "mean")
    ).reset_index().sort_values("avg_max", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=by_company["company"],
        x=by_company["avg_min"] / 100000,
        name="Min (LPA)",
        orientation="h",
        marker_color=SLATE,
    ))
    fig.add_trace(go.Bar(
        y=by_company["company"],
        x=by_company["avg_max"] / 100000,
        name="Max (LPA)",
        orientation="h",
        marker_color=ACCENT,
    ))
    fig.update_layout(
        barmode="group",
        height=max(250, len(by_company) * 40),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Salary (LPA)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_salary_city_chart(jobs_df: pd.DataFrame, role: str) -> go.Figure:
    role_jobs = jobs_df[(jobs_df["role"] == role) & (jobs_df["salary_min"] > 0) & (jobs_df["salary_max"] > 0)].copy()
    if role_jobs.empty:
        return go.Figure()
    by_city = role_jobs.groupby("city").agg(
        avg_min=("salary_min", "mean"), avg_max=("salary_max", "mean")
    ).reset_index().sort_values("avg_max", ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=by_city["city"],
        x=by_city["avg_min"] / 100000,
        name="Avg Min (LPA)",
        orientation="h",
        marker_color=WARN,
    ))
    fig.add_trace(go.Bar(
        y=by_city["city"],
        x=by_city["avg_max"] / 100000,
        name="Avg Max (LPA)",
        orientation="h",
        marker_color=MATCH,
    ))
    fig.update_layout(
        barmode="group",
        height=max(200, len(by_city) * 50),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Salary (LPA)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_openings_chart(jobs_df: pd.DataFrame, role: str) -> go.Figure:
    role_jobs = jobs_df[jobs_df["role"] == role].copy()
    if role_jobs.empty:
        return go.Figure()
    by_city = role_jobs.groupby("city")["positions"].sum().reset_index().sort_values("positions", ascending=True)
    fig = go.Figure(go.Bar(
        y=by_city["city"],
        x=by_city["positions"],
        orientation="h",
        marker_color=ACCENT,
        text=by_city["positions"],
        textposition="outside",
    ))
    fig.update_layout(
        height=max(200, len(by_city) * 50),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Total Positions",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_benchmark_radar(student_skills: list[str], benchmark_skills: list[str]) -> go.Figure:
    categories, student_vals, bench_vals = [], [], []
    for category, category_skills in SKILL_CATEGORIES.items():
        student_count = sum(1 for skill in category_skills if skill in student_skills)
        bench_count = sum(1 for skill in category_skills if skill in benchmark_skills)
        total = max(len(category_skills), 1)
        categories.append(category)
        student_vals.append(round(student_count / total * 100))
        bench_vals.append(round(bench_count / total * 100))
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=student_vals + [student_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Your Profile",
        fillcolor=ACCENT_FILL,
        line=dict(color=ACCENT, width=2),
    ))
    fig.add_trace(go.Scatterpolar(
        r=bench_vals + [bench_vals[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Placed Professional",
        fillcolor="rgba(5, 150, 105, 0.10)",
        line=dict(color=MATCH, width=2, dash="dash"),
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        height=400,
        margin=dict(l=60, r=60, t=40, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_batch_decay_chart(batch_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        go.Bar(
            x=batch_df["student_label"],
            y=batch_df["decay_score"],
            marker_color=[MISS if score >= 70 else WARN if score >= 40 else MATCH for score in batch_df["decay_score"]],
            text=batch_df["decay_score"],
            textposition="outside",
        )
    )
    fig.update_layout(
        title="Skill Decay Risk by Student",
        xaxis_title="Student",
        yaxis_title="Decay Risk Score",
        height=420,
        yaxis=dict(range=[0, 110]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_batch_heatmap(batch_df: pd.DataFrame) -> go.Figure:
    from collections import Counter

    all_missing: list[str] = []
    for column in ["missing_skill_1", "missing_skill_2", "missing_skill_3"]:
        all_missing.extend([skill for skill in batch_df[column].tolist() if skill])
    top_skills = [skill for skill, _ in Counter(all_missing).most_common(8)]
    if not top_skills:
        top_skills = ["No gaps detected"]
    matrix = []
    for _, row in batch_df.iterrows():
        student_missing = {row["missing_skill_1"], row["missing_skill_2"], row["missing_skill_3"]} - {""}
        matrix.append([1 if skill in student_missing else 0 for skill in top_skills])
    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=top_skills,
            y=batch_df["student_label"].tolist(),
            colorscale=[[0, "#f8fafc"], [1, MISS]],
            showscale=False,
        )
    )
    fig.update_layout(
        title="Batch Skill Gap Heatmap",
        height=420,
        xaxis_title="High-demand missing skills",
        yaxis_title="Student",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
