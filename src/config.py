import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", ROOT / "data" / "flights.db"))
MODEL_PATH = ROOT / "models" / "delay_model.joblib"
AIRLABS_API_KEY = os.getenv("AIRLABS_API_KEY", "")
AIRPORTS = ["BOG", "MDE", "CLO", "CTG", "BAQ"]

