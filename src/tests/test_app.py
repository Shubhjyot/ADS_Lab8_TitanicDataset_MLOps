# src/tests/test_app.py
import os
import sys
import joblib
import pytest
from fastapi.testclient import TestClient

# Set testing mode before importing app
os.environ["TESTING"] = "true"

# Add parent directory to path for importing app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

def test_root():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "Titanic" in r.json().get("message", "")

def test_predict_minimal():
    client = TestClient(app)
    payload = {"features": {"Age": 30, "Fare": 7.25, "Sex": "male", "Embarked": "S", "Pclass": "3"}}
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    assert "prediction" in r.json()