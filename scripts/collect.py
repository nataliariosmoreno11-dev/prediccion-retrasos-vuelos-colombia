import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.collector import collect
from src.config import AIRLABS_API_KEY, DATABASE_PATH
from src.database import connect, upsert_flights


if __name__ == "__main__":
    frame = collect(AIRLABS_API_KEY)
    with connect(DATABASE_PATH) as connection:
        count = upsert_flights(connection, frame)
    print(f"Guardados {count} registros en {DATABASE_PATH}")
