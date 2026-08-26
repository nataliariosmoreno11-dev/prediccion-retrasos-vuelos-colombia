from datetime import datetime, timedelta, timezone
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import AIRPORTS, DATABASE_PATH
from src.database import connect, upsert_flights

rng = np.random.default_rng(42)
airlines = ["AV", "LA", "JA", "P5"]
rows = []
start = datetime.now(timezone.utc) - timedelta(days=120)
for index in range(1500):
    origin = rng.choice(AIRPORTS)
    destination = rng.choice([a for a in AIRPORTS if a != origin])
    scheduled = start + timedelta(minutes=int(rng.integers(0, 120 * 24 * 60)))
    rush = 12 if scheduled.hour in [6, 7, 17, 18, 19] else 0
    delay = max(0, rng.gamma(2, 7) + rush + rng.normal(0, 4))
    actual = scheduled + timedelta(minutes=float(delay))
    rows.append({
        "observation_time": actual.isoformat(), "flight_date": scheduled.date().isoformat(),
        "flight_number": f"{rng.choice(airlines)}{rng.integers(100, 9999)}",
        "airline_iata": rng.choice(airlines), "origin": origin, "destination": destination,
        "scheduled_departure": scheduled.isoformat(), "estimated_departure": actual.isoformat(),
        "actual_departure": actual.isoformat(), "status": "landed", "aircraft_icao": None,
        "delay_minutes": round(float(delay), 1), "source": "demo_synthetic",
    })
frame = pd.DataFrame(rows)
with connect(DATABASE_PATH) as connection:
    print(f"Guardados {upsert_flights(connection, frame)} registros de demostración")
