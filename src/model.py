from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .features import FEATURES, build_features


def train(frame: pd.DataFrame, model_path: Path):
    data = build_features(frame).dropna(subset=["delay_minutes"])
    if len(data) < 100:
        raise ValueError("Se necesitan al menos 100 vuelos con retraso conocido para entrenar.")
    categorical = ["origin", "destination", "airline_iata"]
    numeric = ["departure_hour", "day_of_week", "month"]
    transformer = ColumnTransformer([
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("encode", OneHotEncoder(handle_unknown="ignore"))]), categorical),
        ("num", SimpleImputer(strategy="median"), numeric),
    ])
    pipeline = Pipeline([
        ("features", transformer),
        ("model", RandomForestRegressor(n_estimators=250, min_samples_leaf=3, random_state=42, n_jobs=-1)),
    ])
    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
    pipeline.fit(train_data[FEATURES], train_data["delay_minutes"])
    predictions = pipeline.predict(test_data[FEATURES])
    metrics = {
        "mae": float(mean_absolute_error(test_data["delay_minutes"], predictions)),
        "rmse": float(mean_squared_error(test_data["delay_minutes"], predictions) ** 0.5),
        "records": int(len(data)),
    }
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "metrics": metrics}, model_path)
    return metrics


def predict(frame: pd.DataFrame, model_path: Path):
    artifact = joblib.load(model_path)
    features = build_features(frame)
    return artifact["pipeline"].predict(features[FEATURES])

