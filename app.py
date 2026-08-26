from datetime import date, datetime, time, timezone

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import AIRPORTS, DATABASE_PATH, MODEL_PATH
from src.database import connect, read_flights
from src.model import predict

st.set_page_config(page_title="Retrasos aéreos Colombia", page_icon="✈️", layout="wide")
st.title("✈️ Predicción de retrasos en vuelos nacionales")
st.caption("Bogotá · Medellín · Cali · Cartagena · Barranquilla")

with connect(DATABASE_PATH) as connection:
    flights = read_flights(connection)

if flights.empty:
    st.warning("Aún no hay datos. Ejecuta `python scripts/generate_demo.py` o configura AirLabs.")
    st.stop()

flights["scheduled_departure"] = pd.to_datetime(flights["scheduled_departure"], errors="coerce", utc=True)
real = flights[flights["source"] == "airlabs"]
if real.empty:
    st.info("Modo demostración: las cifras visibles son sintéticas y no representan vuelos reales.")

c1, c2, c3 = st.columns(3)
c1.metric("Vuelos registrados", f"{len(flights):,}")
c2.metric("Retraso promedio", f"{flights['delay_minutes'].mean():.1f} min")
c3.metric("Vuelos con +15 min", f"{(flights['delay_minutes'] >= 15).mean():.1%}")

route = flights.assign(route=flights["origin"] + " → " + flights["destination"])
summary = route.groupby("route", as_index=False)["delay_minutes"].mean().sort_values("delay_minutes", ascending=False)
st.plotly_chart(px.bar(summary, x="route", y="delay_minutes", title="Retraso promedio por ruta"), use_container_width=True)

st.subheader("Estimar un vuelo")
left, middle, right = st.columns(3)
origin = left.selectbox("Origen", AIRPORTS)
destination = middle.selectbox("Destino", [a for a in AIRPORTS if a != origin])
airline = right.selectbox("Aerolínea", sorted(flights["airline_iata"].dropna().unique()))
flight_date = left.date_input("Fecha", date.today())
flight_time = middle.time_input("Hora", time(12, 0))

if st.button("Predecir retraso", type="primary"):
    if not MODEL_PATH.exists():
        st.error("El modelo aún no está entrenado. Ejecuta `python scripts/train.py`.")
    else:
        row = pd.DataFrame([{"origin": origin, "destination": destination, "airline_iata": airline,
                             "scheduled_departure": datetime.combine(flight_date, flight_time, tzinfo=timezone.utc)}])
        minutes = max(0, float(predict(row, MODEL_PATH)[0]))
        st.success(f"Retraso estimado: {minutes:.0f} minutos")
        metrics = joblib.load(MODEL_PATH)["metrics"]
        st.caption(f"Error absoluto medio de validación: {metrics['mae']:.1f} minutos.")

st.subheader("Datos recientes")
st.dataframe(flights.head(100), use_container_width=True, hide_index=True)

