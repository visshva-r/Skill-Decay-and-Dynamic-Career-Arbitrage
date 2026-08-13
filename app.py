from __future__ import annotations

from dotenv import load_dotenv
import streamlit as st

load_dotenv()

st.set_page_config(page_title="SkillPulse", page_icon="SP", layout="wide")

from skillpulse.ui.app import main

if __name__ == "__main__":
    main()
