# Predicción de retrasos de vuelos en Colombia

Proyecto de machine learning que recopila vuelos nacionales entre BOG, MDE, CLO, CTG y BAQ, conserva observaciones históricas, entrena un modelo de regresión y muestra resultados en un dashboard Streamlit.

## Variable objetivo

`delay_minutes`: diferencia no negativa entre la salida programada y la salida real (o estimada mientras el vuelo está activo). El proyecto no mezcla retraso de llegada con retraso de salida.

## Fuente

La integración usa AirLabs `schedules`, que entrega horarios programados, estimados y reales. La disponibilidad y cuota dependen del plan contratado. La clave nunca se guarda en GitHub.

## Inicio rápido

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python scripts/generate_demo.py
python scripts/train.py
streamlit run app.py
```

Los datos sintéticos permiten verificar todo el flujo. El dashboard los etiqueta como demostración. Para datos reales, crea una cuenta en AirLabs, pega la clave en `.env` y ejecuta:

```bash
python scripts/collect.py
```

## Automatización

El workflow incluido puede ejecutarse cada hora. En GitHub agrega `AIRLABS_API_KEY` en **Settings → Secrets and variables → Actions**. SQLite sirve para desarrollo; para despliegue persistente se recomienda PostgreSQL, porque los archivos generados por GitHub Actions y muchos hosts no son una base de datos durable.

## Advertencia metodológica

Para una evaluación académica válida, separa entrenamiento y prueba por tiempo, acumula varias semanas de vuelos reales y compara Random Forest con una línea base. Los datos sintéticos solo prueban el software; no sirven para reportar desempeño real.
