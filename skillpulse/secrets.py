"""Secret resolution from environment or Streamlit secrets."""
from __future__ import annotations

import os

import streamlit as st


def get_secret(name: str, default: str = "") -> str:
    env_value = os.getenv(name)
    if env_value:
        return env_value
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default
