# SkillPulse

`SkillPulse` is a market-intelligence and career guidance platform that detects emerging skill decay, identifies role-specific skill gaps, and generates proof-oriented learning roadmaps for early-career talent.

## Overview

SkillPulse helps a learner answer three practical questions:

1. Which skills in my profile still match current hiring demand?
2. Which high-signal skills are rising in the market and missing from my profile?
3. What should I build next to prove those missing skills credibly?

## Problem

Academic curricula change slowly, while hiring signals change continuously. As a result, students and fresh graduates often prepare using outdated assumptions, apply with incomplete skill profiles, and struggle to convert learning into portfolio-ready proof.

## Solution

SkillPulse compares a learner profile against recent role-specific job data and produces:

- matched skills
- missing high-demand skills
- rising and declining market signals
- a skill decay risk score
- a resume compatibility score
- salary insights and position openings count
- month-over-month skill trend analysis
- a 7-day micro-roadmap
- a proof pack containing a mini-project idea, resume bullet, and repository description
- hackathon and competition recommendations
- profile benchmark against placed professionals

## Key Capabilities

- Role- and location-specific job signal analysis
- Resume upload for `PDF`, `DOCX`, or `TXT` files (with 10 MB size limit)
- Skill extraction from profile or resume text
- Interactive charts for skill coverage, trends, salary, and career paths
- Explainable trend analysis showing why a skill is rising or declining
- Month-over-month trend comparison with new skill detection
- Salary insights with company-level and city-level comparisons (LPA)
- Job openings count per role and city
- GitHub-aware profile enrichment using public repository signals
- Profile benchmark comparing your resume against a placed professional's profile
- Hackathon and competition recommendations based on missing skills
- Snapshot history to show how compatibility and skill-decay risk change over time
- Optional Gemini-powered micro-curriculum generation (cached for performance)
- Optional Adzuna-powered live refresh for real-time job signals with salary extraction
- Curated learning resources for missing skills
- Profile comparison mode for side-by-side analysis
- Hybrid data model with curated data, optional live upload, and cache-ready refresh support
- Downloadable markdown and PDF reports (including salary and positions data)
- Multiple demo profiles to compare strong and weak role alignment
- Career path progression for all 6 supported roles

## Why SkillPulse Stands Out

- `Novelty`: focuses on skill decay and market drift instead of generic course recommendation
- `Utility`: converts skill gaps into concrete, portfolio-oriented action
- `Explainability`: shows the evidence behind trend shifts
- `Reliability`: works offline with curated data while remaining compatible with live updates
- `Interactivity`: uses visual analytics for a stronger demo and easier interpretation
- `Benchmarking`: compares your profile against real placed professionals

## Real-World Use Cases

- A final-year student checks whether their current data analyst profile aligns with fresh hiring demand in Chennai.
- A placement cell uses recent job signals to advise students on the most valuable next-step skills.
- A learner converts a missing skill like `Power BI` or `Prompt Engineering` into a focused mini-project and resume-ready evidence.
- A student compares their resume against a placed professional's profile to identify exact skill gaps.
- A learner finds relevant hackathons and competitions to build portfolio evidence for missing skills.

## Example Case Studies

- `Case 1: Strong profile alignment`
  - A student already knows `Excel`, `SQL`, and `Python`.
  - SkillPulse shows that `Power BI` and `Dashboard Storytelling` are the main missing differentiators.
  - The platform generates a short roadmap and a portfolio artifact idea instead of generic learning advice.

- `Case 2: Weak profile alignment`
  - A student mainly has reporting and documentation skills.
  - SkillPulse highlights a higher decay risk and identifies missing analytical skills that are now common in recent postings.
  - The learner gets a targeted recovery path rather than broad career suggestions.

- `Case 3: Placement support`
  - A faculty mentor or placement coordinator reviews multiple student profiles against the same role dataset.
  - SkillPulse provides consistent evidence of market drift and helps prioritize training topics.

## Project Structure

- `app.py`: Streamlit application
- `data/job_postings.csv`: curated multi-role, multi-city job dataset (with salary and positions data)
- `data/live_jobs_sample.csv`: upload-ready sample live jobs CSV
- `data/sample_resume.txt`: sample profile with stronger alignment
- `data/sample_resume_alt.txt`: sample profile with weaker alignment
- `data/resume_visshva_aiml_redacted.txt`: redacted AIML/data resume example
- `data/resume_visshva_sde_redacted.txt`: redacted SDE/full-stack resume example

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dependencies

- `streamlit` for the web interface
- `pandas` for data processing
- `plotly` for interactive charts
- `pdfplumber` for PDF resume extraction
- `python-docx` for DOCX resume extraction
- `fpdf2` for PDF report generation
- `requests` for optional live-data integration
- public GitHub API support for portfolio-aware analysis
- Gemini API support through `GEMINI_API_KEY` for live curriculum generation
- Adzuna API support through `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` for live refresh

## Product Summary

`SkillPulse translates job-market drift into clear, explainable, and actionable career intelligence for students and early-career professionals.`

