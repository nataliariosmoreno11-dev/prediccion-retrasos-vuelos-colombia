from datetime import datetime, timezone

import pandas as pd
import requests

from .config import AIRPORTS

BASE_URL = "https://airlabs.co/api/v9/schedules"


def _delay_minutes(scheduled, actual_or_estimated):
    scheduled = pd.to_datetime(scheduled, errors="coerce", utc=True)
    actual = pd.to_datetime(actual_or_estimated, errors="coerce", utc=True)
    if pd.isna(scheduled) or pd.isna(actual):
        return None
    return max(0.0, (actual - scheduled).total_seconds() / 60)


def normalize(payload: list[dict], observed_at: str | None = None) -> pd.DataFrame:
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    rows = []
    for item in payload:
        origin, destination = item.get("dep_iata"), item.get("arr_iata")
        if origin not in AIRPORTS or destination not in AIRPORTS or origin == destination:
            continue
        scheduled = item.get("dep_time_utc") or item.get("dep_time")
        estimated = item.get("dep_estimated_utc") or item.get("dep_estimated")
        actual = item.get("dep_actual_utc") or item.get("dep_actual")
        rows.append({
            "observation_time": observed_at,
            "flight_date": str(scheduled or "")[:10],
            "flight_number": item.get("flight_iata") or item.get("flight_icao") or "UNKNOWN",
            "airline_iata": item.get("airline_iata"),
            "origin": origin,
            "destination": destination,
            "scheduled_departure": scheduled,
            "estimated_departure": estimated,
            "actual_departure": actual,
            "status": item.get("status"),
            "aircraft_icao": item.get("aircraft_icao"),
            "delay_minutes": _delay_minutes(scheduled, actual or estimated),
            "source": "airlabs",
        })
    return pd.DataFrame(rows)


def collect(api_key: str, airports: list[str] = AIRPORTS) -> pd.DataFrame:
    if not api_key:
        raise ValueError("Falta AIRLABS_API_KEY en el archivo .env")
    records: list[dict] = []
    for airport in airports:
        response = requests.get(BASE_URL, params={"dep_iata": airport, "api_key": api_key}, timeout=30)
        response.raise_for_status()
        body = response.json()
        if body.get("error"):
            raise RuntimeError(body["error"].get("message", str(body["error"])))
        records.extend(body.get("response", []))
    return normalize(records)

