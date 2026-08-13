"""SkillPulse Streamlit application entry orchestration."""
from __future__ import annotations

import streamlit as st

from skillpulse.batch import render_placement_cell_mode
from skillpulse.config import CUSTOM_CSS
from skillpulse.data_loader import load_cached_jobs
from skillpulse.ui.sidebar import render_sidebar
from skillpulse.ui.student_view import render_student_view


def main() -> None:
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.title("SkillPulse")
    st.caption(
        "Compare a student or batch profile to current hiring signals, "
        "score skill decay risk, and get a proof-oriented next step."
    )

    jobs_df = load_cached_jobs()
    sidebar_state = render_sidebar(jobs_df)
    jobs_df = sidebar_state["jobs_df"]

    if sidebar_state["app_mode"] == "Placement Cell Mode":
        render_placement_cell_mode(
            jobs_df,
            sidebar_state["role"],
            sidebar_state["city"],
            sidebar_state["batch_name"],
            sidebar_state["batch_profiles"],
        )
        return

    render_student_view(
        jobs_df=jobs_df,
        role=sidebar_state["role"],
        city=sidebar_state["city"],
        profile_text=sidebar_state["profile_text"],
        portfolio_source=sidebar_state["portfolio_source"],
        github_data=sidebar_state["github_data"],
    )
