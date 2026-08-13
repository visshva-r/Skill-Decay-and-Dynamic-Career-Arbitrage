"""Reusable Streamlit UI components."""
from __future__ import annotations

import html

import streamlit as st


def display_skill_tags_html(skills: list[str], css_class: str, empty_text: str) -> None:
    if skills:
        tags = "".join(f'<span class="skill-tag {css_class}">{html.escape(skill)}</span>' for skill in skills)
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.caption(empty_text)
