# Live Data (Optional) — Expo-Safe Setup

For a winning expo demo, use **hybrid mode**:

- **Guaranteed demo**: curated dataset (`data/job_postings.csv`)
- **Bonus**: live refresh or live CSV upload (if internet/API is available)
- **Fallback**: cached live refresh stored locally (`data/live_cache.csv`) when it succeeds

This avoids demo failure while still letting you claim *real-time capable*.

## Optional Gemini Vision Upgrade

If you want the app to generate a live micro-curriculum instead of only using the built-in templates:

1. Create a Gemini API key.
2. Add `GEMINI_API_KEY` to Streamlit secrets or your local environment.
3. Re-run the app.

The app will continue to work without this key; Gemini simply upgrades the curriculum section when available.

## Optional GitHub Signal Upgrade

Paste a public GitHub profile URL in the sidebar.

- SkillPulse will read public repository metadata through the GitHub API.
- Detected stack/language signals are merged into the profile analysis.
- This makes the demo closer to a portfolio-aware continuous monitoring workflow.

## Fastest path (no API keys)

Use the in-app uploader:

1. Export job postings into a CSV with columns:
   - `job_id`, `role`, `city`, `posted_date`, `title`, `company`, `skills`
2. `skills` must be a `;` separated list, e.g. `SQL;Excel;Power BI`
3. Upload in the sidebar using **Upload a live jobs CSV**

## With an API (optional)

SkillPulse now supports an Adzuna-based live refresh path.

Add these secrets locally or in Streamlit Cloud:

```toml
ADZUNA_APP_ID = "your_app_id"
ADZUNA_APP_KEY = "your_app_key"
ADZUNA_COUNTRY = "in"
```

Then click **Refresh live signals** in the sidebar.

What happens:

- the app queries Adzuna for the selected role and city
- extracts recognizable skills from returned job descriptions
- normalizes them into the same CSV schema
- caches the result into `data/live_cache.csv`

If no Adzuna credentials are provided, the app will still work in curated mode or with uploaded CSV files.

## What to say to judges

`Our demo is offline-safe. We use a curated dataset so the pipeline is reproducible, and we also support live refresh and caching to capture real-time market drift when internet/API is available.`
