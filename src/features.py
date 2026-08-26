import pandas as pd

FEATURES = ["origin", "destination", "airline_iata", "departure_hour", "day_of_week", "month"]


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    data = frame.copy()
    departure = pd.to_datetime(data["scheduled_departure"], errors="coerce", utc=True)
    data["departure_hour"] = departure.dt.hour
    data["day_of_week"] = departure.dt.dayofweek
    data["month"] = departure.dt.month
    return data

