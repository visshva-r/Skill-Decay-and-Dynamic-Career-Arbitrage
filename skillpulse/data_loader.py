"""Job dataset loading, normalization, and optional live refresh."""
from __future__ import annotations

import hashlib

import pandas as pd
import requests
import streamlit as st

from skillpulse.config import (
    CITY_ALIAS_MAP,
    CITY_TO_STATE_MAP,
    DATA_PATH,
    LIVE_CACHE_PATH,
    ROLE_QUERY_MAP,
)
from skillpulse.secrets import get_secret
from skillpulse.skills import extract_skills


def load_jobs() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["posted_date"] = pd.to_datetime(df["posted_date"])
    df["skill_list"] = df["skills"].apply(
        lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
    )
    return df


def normalize_city_name(value: object) -> str:
    text = str(value).strip()
    if not text:
        return text
    return CITY_ALIAS_MAP.get(text.lower(), text)


def standardize_jobs_df(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = {"job_id", "role", "city", "posted_date", "title", "company", "skills"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Job dataset missing columns: {sorted(missing)}")
    df = df.copy()
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["city"] = df["city"].apply(normalize_city_name)
    df["skills"] = df["skills"].fillna("")
    df["skill_list"] = df["skills"].apply(
        lambda value: [item.strip() for item in str(value).split(";") if item.strip()]
    )
    if "salary_min" not in df.columns:
        df["salary_min"] = 0
    if "salary_max" not in df.columns:
        df["salary_max"] = 0
    if "positions" not in df.columns:
        df["positions"] = 1
    df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce").fillna(0).astype(int)
    df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce").fillna(0).astype(int)
    df["positions"] = pd.to_numeric(df["positions"], errors="coerce").fillna(1).astype(int)
    return df.dropna(subset=["posted_date"])


@st.cache_data(show_spinner=False)
def load_cached_jobs() -> pd.DataFrame:
    base = load_jobs()
    if LIVE_CACHE_PATH.exists():
        try:
            live = pd.read_csv(LIVE_CACHE_PATH)
            combined = pd.concat([base, live], ignore_index=True)
            return standardize_jobs_df(combined)
        except Exception:
            return standardize_jobs_df(base)
    return standardize_jobs_df(base)


def _adzuna_secrets() -> tuple[str, str, str]:
    app_id = get_secret("ADZUNA_APP_ID")
    app_key = get_secret("ADZUNA_APP_KEY")
    country = get_secret("ADZUNA_COUNTRY", "in")
    return app_id, app_key, country


def _extract_api_skills(job_text: str) -> list[str]:
    return extract_skills(job_text)[:8]


def _normalize_live_job_row(raw_job: dict, role: str, city: str) -> dict | None:
    title = raw_job.get("title") or role
    company_info = raw_job.get("company") or {}
    company = company_info.get("display_name") if isinstance(company_info, dict) else str(company_info or "Unknown Company")
    location_info = raw_job.get("location") or {}
    area = location_info.get("area") if isinstance(location_info, dict) else []
    detected_city = city
    if isinstance(area, list) and area:
        normalized_area = [str(part).strip() for part in area if str(part).strip()]
        city_matches = [part for part in normalized_area if part.lower() == city.lower()]
        if city_matches:
            detected_city = city_matches[0]
        else:
            state_name = CITY_TO_STATE_MAP.get(city, "").lower()
            non_state_parts = [part for part in normalized_area if part.lower() != state_name]
            detected_city = non_state_parts[-1] if non_state_parts else city
    description = raw_job.get("description") or ""
    skill_list = _extract_api_skills(f"{title}\n{description}")
    if not skill_list:
        return None
    posted_date = pd.to_datetime(raw_job.get("created"), errors="coerce")
    if pd.isna(posted_date):
        posted_date = pd.Timestamp.utcnow()
    sal_min = raw_job.get("salary_min") or 0
    sal_max = raw_job.get("salary_max") or 0
    return {
        "job_id": raw_job.get("id") or f"adzuna-{hashlib.md5((title + company).encode('utf-8')).hexdigest()[:10]}",
        "role": role,
        "city": detected_city or city,
        "posted_date": posted_date.strftime("%Y-%m-%d"),
        "title": title,
        "company": company,
        "skills": ";".join(skill_list),
        "salary_min": sal_min,
        "salary_max": sal_max,
        "positions": 1,
    }


def fetch_adzuna_jobs(role: str, city: str, limit: int) -> pd.DataFrame:
    app_id, app_key, country = _adzuna_secrets()
    if not app_id or not app_key:
        raise RuntimeError("Adzuna credentials are missing. Add `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` to enable live refresh.")
    query = ROLE_QUERY_MAP.get(role, role)
    state = CITY_TO_STATE_MAP.get(city, "")
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": min(limit, 50),
        "what": query,
        "where": city,
        "content-type": "application/json",
    }
    if state:
        params["where"] = f"{city}, {state}"
    response = requests.get(
        f"https://api.adzuna.com/v1/api/jobs/{country}/search/1",
        params=params,
        timeout=25,
    )
    response.raise_for_status()
    data = response.json()
    total_count = data.get("count", 0)
    results = data.get("results", [])
    rows = []
    for raw_job in results:
        normalized = _normalize_live_job_row(raw_job, role=role, city=city)
        if normalized:
            rows.append(normalized)
    if not rows:
        raise RuntimeError("The live API returned jobs, but none contained recognizable skills for the current role.")
    df = pd.DataFrame(rows)
    df.attrs["adzuna_total_count"] = total_count
    return df


def fetch_live_jobs(role: str, city: str, limit: int) -> pd.DataFrame:
    try:
        return fetch_adzuna_jobs(role=role, city=city, limit=limit)
    except Exception as primary_error:
        raise RuntimeError(str(primary_error)) from primary_error
