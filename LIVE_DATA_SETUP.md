# Live Data (Optional) — Expo-Safe Setup

For a winning expo demo, use **hybrid mode**:

- **Guaranteed demo**: curated dataset (`data/job_postings.csv`)
- **Bonus**: live refresh or live CSV upload (if internet/API is available)
- **Fallback**: cached live refresh stored locally (`data/live_cache.csv`) when it succeeds

This avoids demo failure while still letting you claim *real-time capable*.

## Fastest path (no API keys)

Use the in-app uploader:

1. Export job postings into a CSV with columns:
   - `job_id`, `role`, `city`, `posted_date`, `title`, `company`, `skills`
2. `skills` must be a `;` separated list, e.g. `SQL;Excel;Power BI`
3. Upload in the sidebar using **Upload a live jobs CSV**

## With an API (optional)

If you have a job API available (RapidAPI, Adzuna, etc.), wire it into:

- `fetch_live_jobs()` in `app.py`

Return a DataFrame with the same columns as above. When the **Refresh live signals** button is clicked, the app caches the results into `data/live_cache.csv`.

## What to say to judges

`Our demo is offline-safe. We use a curated dataset so the pipeline is reproducible, and we also support live refresh and caching to capture real-time market drift when internet/API is available.`
