"""Sidebar configuration for Student and Placement Cell modes."""
from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from skillpulse.batch import (
    load_demo_batch_profiles,
    parse_batch_from_files,
    parse_batch_from_text,
)
from skillpulse.config import (
    LIVE_CACHE_PATH,
    RESUME_VISSHVA_AIML_PATH,
    RESUME_VISSHVA_SDE_PATH,
    SAMPLE_RESUME_ALT_PATH,
    SAMPLE_RESUME_PATH,
)
from skillpulse.data_loader import fetch_live_jobs, standardize_jobs_df
from skillpulse.github_enrichment import fetch_github_profile_data
from skillpulse.resume_io import extract_text_from_upload, parse_github_username


def render_sidebar(jobs_df: pd.DataFrame) -> dict[str, Any]:
    with st.sidebar:
        st.header("Mode")
        app_mode = st.radio("App mode", ["Student Mode", "Placement Cell Mode"], horizontal=True)
        st.divider()
        st.header("Configuration")
        role = st.selectbox("Target role", sorted(jobs_df["role"].unique()))
        city = st.selectbox("Target city", sorted(jobs_df["city"].unique()))
        batch_name = ""
        batch_profiles: list[tuple[str, str]] = []
        github_data: dict[str, object] = {"username": "", "skills": [], "summary": "", "repos": [], "evidence": []}
        profile_text = ""
        portfolio_source = ""
        profile_choice = "Fresh profile"

        if app_mode == "Placement Cell Mode":
            st.divider()
            st.subheader("Placement Cell Batch")
            batch_name = st.text_input("Batch name (optional)", placeholder="e.g. Final Year Analytics Batch")
            if st.button("Load demo batch (3 students)", width="stretch"):
                st.session_state.batch_paste_text = "\n---\n".join(
                    text for _, text in load_demo_batch_profiles()
                )
            batch_files = st.file_uploader(
                "Upload student profiles (TXT)",
                type=["txt"],
                accept_multiple_files=True,
                help="Upload one TXT file per student profile.",
            )
            if "batch_paste_text" not in st.session_state:
                st.session_state.batch_paste_text = ""
            batch_paste_text = st.text_area(
                "Paste multiple profiles (separate with ---)",
                value=st.session_state.batch_paste_text,
                height=180,
                placeholder="Student 1 profile...\n---\nStudent 2 profile...\n---\nStudent 3 profile...",
            )
            st.session_state.batch_paste_text = batch_paste_text
            if batch_files:
                batch_profiles.extend(parse_batch_from_files(batch_files))
            if batch_paste_text.strip():
                batch_profiles.extend(parse_batch_from_text(batch_paste_text))
            seen_labels: set[tuple[str, str]] = set()
            deduped_profiles: list[tuple[str, str]] = []
            for label, text in batch_profiles:
                key = (label, text[:120])
                if key not in seen_labels:
                    seen_labels.add(key)
                    deduped_profiles.append((label, text))
            batch_profiles = deduped_profiles
            if batch_profiles:
                st.caption(f"{len(batch_profiles)} profile(s) ready for batch analysis.")
            st.divider()
            st.subheader("Data Source")
            uploaded_csv = st.file_uploader("Upload a live jobs CSV (optional)", type=["csv"], key="placement_csv")
            if uploaded_csv is not None:
                try:
                    jobs_df = standardize_jobs_df(pd.read_csv(uploaded_csv))
                    st.success("Loaded uploaded job dataset.")
                except Exception as error:
                    st.error(f"Could not read uploaded CSV: {error}")
        else:
            st.divider()
            st.subheader("Quick start")
            st.caption("Fastest path: pick a sample below, then **Apply profile**.")
            st.subheader("Resume Upload")
            resume_upload = st.file_uploader("Upload your resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"], help="Extract text and auto-detect skills.")
            uploaded_resume_text = ""
            if resume_upload is not None:
                with st.spinner("Extracting text from resume..."):
                    uploaded_resume_text = extract_text_from_upload(resume_upload)
                if uploaded_resume_text and not uploaded_resume_text.startswith("["):
                    st.success(f"Extracted {len(uploaded_resume_text)} characters from {resume_upload.name}")
                elif uploaded_resume_text.startswith("["):
                    st.warning(uploaded_resume_text)
                    uploaded_resume_text = ""
            st.divider()
            st.subheader("Student Profile")
            st.caption("Use Apply profile to avoid rerunning Gemini and GitHub analysis on every sidebar change.")
            if "applied_profile_text" not in st.session_state:
                st.session_state.applied_profile_text = ""
            if "applied_portfolio_source" not in st.session_state:
                st.session_state.applied_portfolio_source = ""
            if "applied_profile_label" not in st.session_state:
                st.session_state.applied_profile_label = "Fresh profile"
            with st.form("profile_input_form"):
                profile_choice = st.radio(
                    "Profile source",
                    options=[
                        "Uploaded Resume" if resume_upload else "Upload a resume above",
                        "Fresh profile",
                        "Sample (Strong match)",
                        "Sample (Weak match)",
                        "Resume (AIML/Data)",
                        "Resume (SDE/Full-stack)",
                        "Custom paste",
                    ],
                    index=1,
                )
                if "Uploaded Resume" in profile_choice and uploaded_resume_text:
                    profile_text = uploaded_resume_text
                elif profile_choice == "Fresh profile":
                    profile_text = ""
                elif profile_choice == "Sample (Strong match)":
                    profile_text = SAMPLE_RESUME_PATH.read_text(encoding="utf-8")
                elif profile_choice == "Sample (Weak match)":
                    profile_text = SAMPLE_RESUME_ALT_PATH.read_text(encoding="utf-8")
                elif profile_choice == "Resume (AIML/Data)":
                    profile_text = RESUME_VISSHVA_AIML_PATH.read_text(encoding="utf-8")
                elif profile_choice == "Resume (SDE/Full-stack)":
                    profile_text = RESUME_VISSHVA_SDE_PATH.read_text(encoding="utf-8")
                else:
                    profile_text = st.session_state.applied_profile_text if profile_choice == st.session_state.applied_profile_label else ""
                profile_text = st.text_area(
                    "Edit or paste profile text",
                    value=profile_text,
                    height=220,
                    placeholder="Paste a fresh resume summary, skills, projects, or achievements here...",
                )
                portfolio_source = st.text_input(
                    "GitHub / portfolio URL or notes (optional)",
                    value=st.session_state.applied_portfolio_source,
                    placeholder="https://github.com/username or brief portfolio notes",
                )
                apply_profile = st.form_submit_button("Apply profile")
            if apply_profile:
                st.session_state.applied_profile_text = profile_text
                st.session_state.applied_portfolio_source = portfolio_source
                st.session_state.applied_profile_label = profile_choice
            profile_text = st.session_state.applied_profile_text
            portfolio_source = st.session_state.applied_portfolio_source
            profile_choice = st.session_state.applied_profile_label
            github_username = parse_github_username(portfolio_source)
            if github_username:
                try:
                    with st.spinner("Analyzing GitHub profile..."):
                        github_data = fetch_github_profile_data(github_username)
                    st.success(f"Loaded public GitHub signals for @{github_username}")
                    if github_data["skills"]:
                        st.caption("GitHub-detected skills: " + ", ".join(github_data["skills"][:8]))
                    if github_data.get("evidence"):
                        st.caption(f"{len(github_data['evidence'])} skill evidence signal(s) collected.")
                except Exception as error:
                    st.warning(f"GitHub analysis unavailable: {error}")
            elif profile_choice == "Fresh profile" and not profile_text.strip():
                st.info("Load a sample or paste a profile, then click **Apply profile**.")
            st.divider()
            st.subheader("Data Source")
            uploaded_csv = st.file_uploader("Upload a live jobs CSV (optional)", type=["csv"])
            if uploaded_csv is not None:
                try:
                    jobs_df = standardize_jobs_df(pd.read_csv(uploaded_csv))
                    st.success("Loaded uploaded job dataset.")
                except Exception as error:
                    st.error(f"Could not read uploaded CSV: {error}")
            live_limit = st.slider("Live refresh size", min_value=10, max_value=80, value=30, step=10)
            if st.button("Refresh live signals"):
                try:
                    live_df = standardize_jobs_df(fetch_live_jobs(role=role, city=city, limit=live_limit))
                    live_df.to_csv(LIVE_CACHE_PATH, index=False)
                    st.success("Live refresh complete.")
                    st.cache_data.clear()
                except Exception as error:
                    st.warning(f"Live refresh not available: {error}")

    return {
        "app_mode": app_mode,
        "role": role,
        "city": city,
        "batch_name": batch_name,
        "batch_profiles": batch_profiles,
        "jobs_df": jobs_df,
        "profile_text": profile_text,
        "portfolio_source": portfolio_source,
        "profile_choice": profile_choice,
        "github_data": github_data,
    }
