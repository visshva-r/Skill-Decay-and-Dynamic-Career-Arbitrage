# SkillPulse

SkillPulse compares a profile to role-specific hiring signals, scores skill decay risk from job-post evidence, and turns gaps into a concrete proof plan for students and placement batches.

**Live demo:** [https://skillpulse-visshva.streamlit.app/](https://skillpulse-visshva.streamlit.app/)

## Overview

SkillPulse helps learners and placement teams answer:

1. Which skills still match current hiring demand?
2. Which rising skills are missing from a profile or batch?
3. What should students build next to prove those skills?

## Problem

Academic curricula change slowly, while hiring signals change continuously. Students often prepare using outdated assumptions, and placement teams lack a consistent batch-level view of skill decay and market alignment.

## Solution

SkillPulse compares learner profiles against recent role-specific job data and produces:

- matched and missing skills
- rising and declining market signals
- a skill decay risk score
- a resume compatibility score
- salary insights and position openings
- month-over-month skill trend analysis
- a 7-day micro-roadmap and proof pack
- competition recommendations for portfolio building
- institutional batch dashboards and mentor exports

## Key Capabilities

### Student Mode
- Resume upload for `PDF`, `DOCX`, or `TXT` (10 MB limit)
- Five tabs: Overview, Market Evidence, Fit & Roadmap, Plan & Progress, Grow
- Decay risk hero with evidence preview, next action, and score methodology
- Rising/declining trends, salary/openings, career paths, benchmarks
- 7-day roadmap, proof pack, snapshot history CSV, optional AI study plan
- Optional Adzuna live refresh and GitHub portfolio enrichment
- Individual Markdown/PDF report download

### Placement Cell Mode
- Toggle between **Student Mode** and **Placement Cell Mode**
- Multi-profile input via TXT upload, `---` separated paste, or demo batch preset
- Batch table sorted high-risk first: decay risk, fit score, missing skills, risk level
- Batch decay chart, skill-gap heatmap, mentor action plan CSV
- Export Batch CSV/PDF and College Readiness Report (PDF)

## Dataset Coverage

- **146** curated job postings (at least 2 per role×city; AI/ML Intern thickened to 4–7 per city)
- **8 roles:** Junior Data Analyst, Frontend Developer, AI/ML Intern, Business Analyst, Data Science Intern, SDE / Full-stack Developer, FinTech Analyst, Healthcare Data Analyst
- **7 cities:** Chennai, Bengaluru, Hyderabad, Pune, Gurugram, Mumbai, Delhi

## Why this project

- Focuses on skill decay and market drift, not generic course lists
- Turns gaps into portfolio work you can actually ship
- Shows the job-post evidence behind each trend
- Runs offline on curated data, with optional live refresh
- Same engine for one student or a full placement batch

## Project Structure

- `app.py` - thin Streamlit entry point
- `skillpulse/` - Python package
  - `config.py` - paths, constants, skill maps, CSS
  - `skills.py`, `market.py`, `curriculum.py`, `snapshots.py` - core analysis
  - `data_loader.py`, `resume_io.py`, `github_enrichment.py`, `gemini_curriculum.py` - data and enrichment
  - `charts.py`, `reports.py`, `batch.py` - visualization and exports
  - `ui/` - Streamlit sidebar, student view, and app orchestration
- `data/job_postings.csv` - curated job dataset
- `data/sample_resume.txt` / `data/sample_resume_alt.txt` - demo profiles
- `data/sample_batch_student_3.txt` - third demo student for batch mode
- `TECHNICAL_DOCUMENTATION.md` - architecture and technical reference
- `scripts/feature_smoke_test.py` - local feature smoke test

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

### Optional environment variables

```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
ADZUNA_COUNTRY=in
GITHUB_TOKEN=your_token
```

The core demo works offline without any API keys.

## Demo Walkthrough

### Student Mode
1. Select **Student Mode**
2. Choose role + city (e.g. Junior Data Analyst, Chennai)
3. Load **Sample (Weak match)** or paste a profile → **Apply profile**
4. Review decay risk, gaps, trends, roadmap, and proof pack
5. Open **Micro-Curriculum** → click **Generate with Gemini** if you want the optional AI layer

### Placement Cell Mode
1. Select **Placement Cell Mode**
2. Choose role + city and optional batch name
3. Click **Load demo batch (3 students)** or paste/upload profiles
4. Review batch table, charts, and training focus
5. Export CSV, batch PDF, and College Readiness Report

## Dependencies

- `streamlit`, `pandas`, `plotly`, `requests`, `python-dotenv`
- `pdfplumber`, `python-docx`, `fpdf2` for resume parsing and PDF exports

## Product Summary

`SkillPulse translates job-market drift into clear, explainable, and actionable career intelligence for students and placement coordinators.`
