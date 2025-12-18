from fastapi import FastAPI
from pydantic import BaseModel
from feast import FeatureStore
import mlflow.pyfunc
import pandas as pd
import os

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

app = FastAPI(title="StreamFlow Churn Prediction API")

# Création des métriques Prometheus
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests"
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "Latency of API requests in seconds"
)

# --------------------
# Config
# --------------------
REPO_PATH = "/repo"
MODEL_NAME = "streamflow_churn"
MODEL_URI = f"models:/{MODEL_NAME}/Production"

# --------------------
# Init Feature Store + Model
# --------------------
try:
    store = FeatureStore(repo_path=REPO_PATH)
    model = mlflow.pyfunc.load_model(MODEL_URI)
except Exception as e:
    print(f"Warning: init failed: {e}")
    store = None
    model = None


# --------------------
# Request schema
# --------------------
class UserPayload(BaseModel):
    user_id: str


# --------------------
# Health check
# --------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# --------------------
# Predict endpoint
# --------------------
@app.post("/predict")
def predict(payload: UserPayload):
    # Prendre le temps au départ
    start_time = time.time()

    # Incrémenter le compteur de requêtes
    REQUEST_COUNT.inc()

    if store is None or model is None:
        return {"error": "Model or feature store not initialized"}

    # Liste des features online à récupérer
    features_request = [
        "subs_profile_fv:months_active",
        "subs_profile_fv:monthly_fee",
        "subs_profile_fv:paperless_billing",
        "subs_profile_fv:plan_stream_tv",
        "subs_profile_fv:plan_stream_movies",
        "subs_profile_fv:net_service",
        "usage_agg_30d_fv:watch_hours_30d",
        "usage_agg_30d_fv:avg_session_mins_7d",
        "usage_agg_30d_fv:unique_devices_30d",
        "usage_agg_30d_fv:skips_7d",
        "usage_agg_30d_fv:rebuffer_events_7d",
        "payments_agg_90d_fv:failed_payments_90d",
        "support_agg_90d_fv:support_tickets_90d",
        "support_agg_90d_fv:ticket_avg_resolution_hrs_90d",
    ]

    # Récupération des features online
    feature_dict = store.get_online_features(
        features=features_request,
        entity_rows=[{"user_id": payload.user_id}],
    ).to_dict()

    # Construction d’un DataFrame 1 ligne
    X = pd.DataFrame({k: [v[0]] for k, v in feature_dict.items()})

    # Vérification des features manquantes
    if X.isnull().any().any():
        missing = X.columns[X.isnull().any()].tolist()
        return {
            "error": f"Missing features for user_id={payload.user_id}",
            "missing_features": missing,
        }

    # Nettoyage minimal
    X = X.drop(columns=["user_id"], errors="ignore")

    # Appel du modèle MLflow (pyfunc)
    y_pred = model.predict(X)

    # Observer la latence (en secondes)
    REQUEST_LATENCY.observe(time.time() - start_time)

    # Réponse JSON
    return {
        "user_id": payload.user_id,
        "prediction": int(y_pred[0]),
        "features_used": X.to_dict(orient="records")[0],
    }

@app.get("/metrics")
def metrics():
    # Retourner les métriques au format Prometheus
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
