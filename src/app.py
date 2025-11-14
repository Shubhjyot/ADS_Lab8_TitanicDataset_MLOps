# src/app.py
import os
import joblib
import time
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from logger_config import logger

# Load model bundle (pipeline + feature order)
MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Train and place model.joblib there.")

bundle = joblib.load(MODEL_PATH)
model = bundle["pipeline"]
FEATURE_ORDER = bundle.get("feature_order", ["Age", "Fare", "Sex", "Embarked", "Pclass"])

app = FastAPI(title="Titanic Survival Predictor")

# Prometheus metrics
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["endpoint", "method", "status"])
PRED_LATENCY = Histogram("prediction_latency_seconds", "Prediction latency seconds")
PRED_CLASS = Counter("prediction_class_total", "Prediction count per class", ["prediction_class"])

class InputData(BaseModel):
    # Accept partial feature dict — missing values will be filled with defaults in API
    features: dict

@app.get("/")
def root():
    return {"message": "Titanic Survival Predictor API"}

@app.post("/predict")
def predict(data: InputData):
    start = time.time()
    try:
        REQUEST_COUNT.labels(endpoint="/predict", method="POST", status="200").inc()
        # Build a single-row df using FEATURE_ORDER keys; missing -> None (preprocessor will impute)
        input_dict = data.features
        row = {feat: input_dict.get(feat) for feat in FEATURE_ORDER}
        # Ensure types: Pclass as string (we trained as string)
        if "Pclass" in row and row["Pclass"] is not None:
            row["Pclass"] = str(row["Pclass"])
        df = pd.DataFrame([row])
        pred = int(model.predict(df)[0])
        pred_prob = float(model.predict_proba(df)[0][pred]) if hasattr(model, "predict_proba") else None
        PRED_CLASS.labels(prediction_class=str(pred)).inc()
        PRED_LATENCY.observe(time.time() - start)
        logger.info("prediction", input=row, prediction=int(pred), probability=pred_prob)
        response = {"prediction": int(pred)}
        if pred_prob is not None:
            response["probability"] = pred_prob
        return response
    except Exception as e:
        REQUEST_COUNT.labels(endpoint="/predict", method="POST", status="500").inc()
        logger.error("prediction_error", error=str(e))
        return {"error": str(e)}

@app.get("/metrics")
def metrics():
    # Prometheus scrape endpoint
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)