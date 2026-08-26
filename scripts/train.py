import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import DATABASE_PATH, MODEL_PATH
from src.database import connect, read_flights
from src.model import train


if __name__ == "__main__":
    with connect(DATABASE_PATH) as connection:
        frame = read_flights(connection)
    print(train(frame, MODEL_PATH))
