# SkillPulse Technical Documentation

## 1. Architecture Overview

SkillPulse is a Streamlit application that compares student profiles against curated (and optionally live) job-market data to detect skill decay, identify gaps, and generate proof-oriented career guidance.

### Student Flow

```
Profile input (paste / upload / preset)
        ↓
Skill extraction (SKILL_CATALOG + aliases)
        ↓
Market analysis (analyze_market)
        ↓
Scores + charts + roadmap + exports
```

### Batch / Placement Cell Flow

```
Multiple student profiles (upload / paste / demo batch)
        ↓
run_batch_analysis()  ← reuses single-profile engine
        ↓
Batch table + heatmap + summary cards
        ↓
Mentor CSV/PDF + College Readiness Report
```

Both flows use the same core analysis functions. Placement Cell Mode does not duplicate scoring logic.

---

## 2. File Structure

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app, analysis engine, charts, exports |
| `data/job_postings.csv` | Curated multi-role, multi-city job dataset |
| `data/sample_resume.txt` | Strong-match demo profile |
| `data/sample_resume_alt.txt` | Weak-match demo profile |
| `data/sample_batch_student_3.txt` | Moderate demo profile for batch mode |
| `data/live_jobs_sample.csv` | Optional upload format for live jobs |
| `scripts/feature_smoke_test.py` | Local automated feature smoke test |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Upload size limit (10 MB) |
| `.env` | Local API keys (not committed) |

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

**Current coverage:** 88 rows, 8 roles, 7 cities.

**Roles:** Junior Data Analyst, Frontend Developer, AI/ML Intern, Business Analyst, Data Science Intern, SDE / Full-stack Developer, FinTech Analyst, Healthcare Data Analyst

**Cities:** Chennai, Bengaluru, Hyderabad, Pune, Gurugram, Mumbai, Delhi

---

## 4. Key Functions

| Function | Purpose |
|----------|---------|
| `extract_skills()` | Keyword/alias matching against `SKILL_CATALOG` |
| `analyze_market()` | Gap analysis, trend detection, decay risk score |
| `compute_resume_compatibility()` | Fit score with breakdown |
| `run_batch_analysis()` | Runs single-profile analysis across a batch |
| `aggregate_batch_summary()` | Batch-wide risk buckets and training focus |
| `build_batch_decay_chart()` | Per-student decay bar chart |
| `build_batch_heatmap()` | Students × missing skills heatmap |
| `export_batch_csv()` | Mentor CSV export |
| `generate_batch_pdf()` | Faculty batch summary PDF |
| `generate_readiness_report_pdf()` | College Placement Readiness Report |
| `resolve_gemini_curriculum()` | On-demand Gemini generation with session cache |
| `generate_gemini_curriculum()` | Optional Gemini API call (cached) |
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

The app runs fully offline with curated CSV data when no API keys are set.

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
```

Optional: create `.env` with API keys for Gemini, Adzuna, or GitHub.
