from src.collector import normalize


def test_normalize_filters_routes_and_calculates_delay():
    payload = [{
        "dep_iata": "BOG", "arr_iata": "MDE", "flight_iata": "AV123",
        "airline_iata": "AV", "dep_time_utc": "2026-08-26T15:00:00Z",
        "dep_actual_utc": "2026-08-26T15:25:00Z", "status": "landed",
    }]
    result = normalize(payload, "2026-08-26T16:00:00Z")
    assert len(result) == 1
    assert result.iloc[0]["delay_minutes"] == 25

