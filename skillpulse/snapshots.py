"""Profile snapshot history, deltas, and CSV export."""
from __future__ import annotations

import hashlib
import json

import pandas as pd

from skillpulse.config import SNAPSHOT_HISTORY_PATH
from skillpulse.skills import normalize_token


def _load_snapshot_history() -> list[dict[str, object]]:
    if not SNAPSHOT_HISTORY_PATH.exists():
        return []
    try:
        return json.loads(SNAPSHOT_HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_snapshot_history(entries: list[dict[str, object]]) -> None:
    SNAPSHOT_HISTORY_PATH.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def build_profile_key(profile_context: str, role: str, city: str, github_username: str) -> str:
    fingerprint = f"{normalize_token(profile_context)}|{role}|{city}|{github_username}"
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:16]


def record_snapshot(profile_key: str, role: str, city: str, analysis: dict, compatibility_data: dict[str, int], student_skills: list[str]) -> None:
    history = _load_snapshot_history()
    today = pd.Timestamp.utcnow().strftime("%Y-%m-%d")
    entry = {
        "profile_key": profile_key,
        "date": today,
        "role": role,
        "city": city,
        "decay_risk": analysis["score"],
        "compatibility": compatibility_data["overall"],
        "missing_skills": analysis["missing"][:5],
        "detected_skills": student_skills[:12],
    }
    history = [item for item in history if not (item.get("profile_key") == profile_key and item.get("date") == today)]
    history.append(entry)
    history = sorted(history, key=lambda item: (item.get("profile_key", ""), item.get("date", "")))[-200:]
    _save_snapshot_history(history)


def get_profile_history(profile_key: str) -> pd.DataFrame:
    history = [item for item in _load_snapshot_history() if item.get("profile_key") == profile_key]
    if not history:
        return pd.DataFrame()
    return pd.DataFrame(history).sort_values("date")


def build_snapshot_delta(history_df: pd.DataFrame) -> dict[str, object]:
    if history_df.empty or len(history_df) < 2:
        return {
            "has_delta": False,
            "message": "Save at least two snapshots on different days to compare progress.",
        }
    latest = history_df.iloc[-1]
    previous = history_df.iloc[-2]
    compat_delta = int(latest["compatibility"]) - int(previous["compatibility"])
    risk_delta = int(latest["decay_risk"]) - int(previous["decay_risk"])
    explanation = (
        f"Compared to your previous snapshot ({previous['date']}): "
        f"resume compatibility moved {compat_delta:+d} points "
        f"({previous['compatibility']}% → {latest['compatibility']}%), "
        f"and skill decay risk moved {risk_delta:+d} points "
        f"({previous['decay_risk']} → {latest['decay_risk']})."
    )
    if compat_delta > 0 and risk_delta <= 0:
        explanation += " Your profile is trending in a positive direction."
    elif compat_delta < 0 or risk_delta > 0:
        explanation += " Consider reinforcing missing high-demand skills from the latest market window."
    return {
        "has_delta": True,
        "compatibility_delta": compat_delta,
        "decay_risk_delta": risk_delta,
        "previous_date": str(previous["date"]),
        "latest_date": str(latest["date"]),
        "explanation": explanation,
    }


def export_history_csv(history_df: pd.DataFrame) -> str:
    if history_df.empty:
        return "date,decay_risk,compatibility,role,city\n"
    export_df = history_df[["date", "decay_risk", "compatibility", "role", "city"]].copy()
    return export_df.to_csv(index=False)
