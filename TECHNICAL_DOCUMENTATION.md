# SkillPulse Technical Documentation

## 1. Architecture Overview

SkillPulse is a Streamlit application that compares student profiles against curated (and optionally live) job-market data to detect skill decay, identify gaps, and generate proof-oriented career guidance.

### Student Flow

```
Profile input (paste / upload / preset)
        ↓
Skill extraction (SKILL_CATALOG + aliases)
        ↓
Market analysis (analyze_market + evidence_cards)
        ↓
Scores + charts + roadmap + exports
```

### Batch / Placement Cell Flow

```
Multiple student profiles (upload / paste / demo batch)
        ↓
run_batch_analysis()  ← reuses single-profile engine
        ↓
Batch table (high-risk first) + heatmap + summary cards
        ↓
Mentor CSV / action plan / PDF + College Readiness Report
```

Both flows use the same core analysis functions. Placement Cell Mode does not duplicate scoring logic.

---

## 2. Module Layout

| Module | Purpose |
|--------|---------|
| `app.py` | Thin entry: `load_dotenv`, page config, calls `skillpulse.ui.app.main()` |
| `skillpulse/config.py` | Paths, constants, `CUSTOM_CSS`, skill/project/hackathon maps |
| `skillpulse/secrets.py` | `get_secret()` from env or Streamlit secrets |
| `skillpulse/skills.py` | `extract_skills`, `normalize_token`, `count_skills`, `get_learning_resources` |
| `skillpulse/resume_io.py` | PDF/DOCX/TXT upload parsing, GitHub username parsing |
| `skillpulse/data_loader.py` | Job CSV loading, Adzuna live refresh, cache merge |
| `skillpulse/market.py` | `analyze_market` (evidence cards, monthly stability), compatibility, alerts |
| `skillpulse/curriculum.py` | 7-day roadmap, proof pack, micro-curriculum |
| `skillpulse/snapshots.py` | Profile history, delta explanation, CSV export |
| `skillpulse/github_enrichment.py` | GitHub API enrichment with per-skill evidence list |
| `skillpulse/gemini_curriculum.py` | Optional Gemini curriculum with weekly milestones + offline fallback |
| `skillpulse/charts.py` | Plotly charts (ink + teal palette) |
| `skillpulse/reports.py` | Student and batch PDF generation |
| `skillpulse/batch.py` | Batch analysis, mentor action plan CSV, placement cell UI |
| `skillpulse/ui/components.py` | Shared HTML skill tag renderer |
| `skillpulse/ui/sidebar.py` | Sidebar configuration for both modes |
| `skillpulse/ui/student_view.py` | Student UI: 5 tabs (Overview, Market Evidence, Fit & Roadmap, Plan & Progress, Grow) |
| `skillpulse/ui/app.py` | Main orchestration |

### UI notes

- Visual system uses ink/slate + teal accent (not purple gradient “AI dashboard” defaults).
- Overview leads with decay status, top evidence line, and one next action.
- Optional Gemini is labeled **AI study plan**; competitions sit under Grow as secondary.

---

## 3. Data Model (`job_postings.csv`)

| Column | Type | Description |
|--------|------|-------------|
| `job_id` | int | Unique posting identifier |
| `role` | string | Target role (e.g. Junior Data Analyst) |
| `city` | string | Indian city |
| `posted_date` | date | Posting date (used for trend windows) |
| `title` | string | Job title |
| `company` | string | Employer label |
| `skills` | string | Semicolon-separated skill list |
| `salary_min` | int | Minimum salary (INR) |
| `salary_max` | int | Maximum salary (INR) |
| `positions` | int | Open positions count |

**Current coverage:** 146 rows, 8 roles, 7 cities (minimum 2 postings per role×city; AI/ML Intern 4–7 per city).

**Roles:** Junior Data Analyst, Frontend Developer, AI/ML Intern, Business Analyst, Data Science Intern, SDE / Full-stack Developer, FinTech Analyst, Healthcare Data Analyst

**Cities:** Chennai, Bengaluru, Hyderabad, Pune, Gurugram, Mumbai, Delhi

---

## 4. Key Functions

| Function | Purpose |
|----------|---------|
| `extract_skills()` | Keyword/alias matching against `SKILL_CATALOG` |
| `analyze_market()` | Gap analysis, trend detection, decay risk, `evidence_cards`, `monthly_stability` |
| `compute_resume_compatibility()` | Fit score with breakdown |
| `build_snapshot_delta()` | Current vs previous snapshot explanation |
| `export_history_csv()` | Snapshot history CSV for student UI download |
| `run_batch_analysis()` | Runs single-profile analysis across a batch |
| `prioritize_batch_risk()` | Sorts batch results high-risk first |
| `export_mentor_action_plan_csv()` | Who trains on which rising skills |
| `aggregate_batch_summary()` | Batch-wide risk buckets and training focus |
| `fetch_github_profile_data()` | GitHub enrichment with `evidence` list |
| `generate_gemini_curriculum()` | Optional Gemini API call with offline fallback |
| `resolve_gemini_curriculum()` | On-demand Gemini generation with session cache |
| `fetch_adzuna_jobs()` | Optional live job refresh |

---

## 5. How Batch Dashboard Reuses Single-Profile Engine

`run_batch_analysis()` calls `analyze_single_profile()` for each student. That function internally uses:

- `extract_skills(profile_text)`
- `analyze_market(filtered_jobs, student_skills)`
- `compute_resume_compatibility(...)`

No separate batch scoring rules exist. This keeps student and institutional views consistent.

---

## 6. Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `GEMINI_API_KEY` | No | Live micro-curriculum generation |
| `GEMINI_MODEL` | No | Gemini model override (default: gemini-2.5-flash) |
| `ADZUNA_APP_ID` | No | Live job refresh |
| `ADZUNA_APP_KEY` | No | Live job refresh |
| `ADZUNA_COUNTRY` | No | Default: `in` |
| `GITHUB_TOKEN` | No | Higher GitHub API rate limits |

The app runs fully offline with curated CSV data when no API keys are set. Gemini and GitHub degrade gracefully to built-in fallbacks or warnings.

---

## 7. Scalability Notes

- **Add roles/cities:** append rows to `job_postings.csv` and update `ROLE_QUERY_MAP` / `CITY_TO_STATE_MAP` if Adzuna live refresh is needed.
- **Institutional mode:** Placement Cell Mode scales to any number of pasted/uploaded TXT profiles in one session.
- **Domain packs:** FinTech and Healthcare roles demonstrate vertical expansion without changing the core engine.
- **Exports:** CSV and PDF outputs are generated in-memory for mentor workflows.

---

## 8. Future Work

- Department-level dashboards across multiple batches
- Scheduled market refresh and email alerts to placement coordinators
- LMS integration for assigning proof projects
- Stronger resume parsing (section-aware extraction)
- Authentication and saved batch history per institution

---

## 9. Run Instructions

```bash
pip install -r requirements.txt
streamlit run app.py
python scripts/feature_smoke_test.py
python -m py_compile app.py skillpulse/**/*.py
```

Optional: create `.env` with API keys for Gemini, Adzuna, or GitHub.
