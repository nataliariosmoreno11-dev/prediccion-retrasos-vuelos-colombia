import sqlite3
from pathlib import Path

import pandas as pd

SCHEMA = """
CREATE TABLE IF NOT EXISTS flights (
    observation_time TEXT NOT NULL,
    flight_date TEXT NOT NULL,
    flight_number TEXT NOT NULL,
    airline_iata TEXT,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    scheduled_departure TEXT,
    estimated_departure TEXT,
    actual_departure TEXT,
    status TEXT,
    aircraft_icao TEXT,
    delay_minutes REAL,
    source TEXT NOT NULL,
    PRIMARY KEY (observation_time, flight_date, flight_number, origin, destination)
)
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute(SCHEMA)
    return connection


def upsert_flights(connection: sqlite3.Connection, frame: pd.DataFrame) -> int:
    if frame.empty:
        return 0
    columns = list(frame.columns)
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT OR REPLACE INTO flights ({','.join(columns)}) VALUES ({placeholders})"
    connection.executemany(sql, frame.where(pd.notna(frame), None).itertuples(index=False, name=None))
    connection.commit()
    return len(frame)


def read_flights(connection: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM flights ORDER BY scheduled_departure DESC", connection)

