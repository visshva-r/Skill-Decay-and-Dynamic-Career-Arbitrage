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
- a 7-day micro-roadmap
- a proof pack containing a mini-project idea, resume bullet, and repository description

## Key Capabilities

- Role- and location-specific job signal analysis
- Skill extraction from profile or resume text
- Explainable trend analysis showing why a skill is rising or declining
- Hybrid data model with curated data, optional live upload, and cache-ready refresh support
- Downloadable markdown report for sharing or review
- Multiple demo profiles to compare strong and weak role alignment

## Why SkillPulse Stands Out

- `Novelty`: focuses on skill decay and market drift instead of generic course recommendation
- `Utility`: converts skill gaps into concrete, portfolio-oriented action
- `Explainability`: shows the evidence behind trend shifts
- `Reliability`: works offline with curated data while remaining compatible with live updates

## Real-World Use Cases

- A final-year student checks whether their current data analyst profile aligns with fresh hiring demand in Chennai.
- A placement cell uses recent job signals to advise students on the most valuable next-step skills.
- A learner converts a missing skill like `Power BI` or `Prompt Engineering` into a focused mini-project and resume-ready evidence.

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

## Evidence (Optional)

If you want to cite credible external context during judging or in a report:

- `evidence_notes.md`: summary of the external PDFs and what they support
- ModernAnalyst (2026) on agentic workflows, governance-in-the-flow, provenance, monitoring, and decision rights
- Cornerstone on skills graphs and skills taxonomies used to map skills to roles
- Hays skills reporting on rapid shifts in workforce capability expectations

## Project Structure

- `app.py`: Streamlit application
- `data/job_postings.csv`: curated role-specific job dataset
- `data/sample_resume.txt`: sample profile with stronger alignment
- `data/sample_resume_alt.txt`: sample profile with weaker alignment
- `data/resume_visshva_aiml_redacted.txt`: your AIML/data resume content (redacted)
- `data/resume_visshva_sde_redacted.txt`: your SDE/full-stack resume content (redacted)
- `case_studies.md`: concise real-world scenarios and product relevance
- `evidence_notes.md`: summary of supporting references and how to cite them honestly
- `pitch.md`: presentation summary
- `demo_script.md`: short walkthrough script
- `LIVE_DATA_SETUP.md`: optional hybrid/live data integration guide

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Product Summary

`SkillPulse translates job-market drift into clear, explainable, and actionable career intelligence for students and early-career professionals.`

## Optional SDG Alignment

- SDG 4 (Quality Education)
- SDG 8 (Decent Work and Economic Growth)
