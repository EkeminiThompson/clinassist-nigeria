"""
Unit tests for the prediction service.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.services.prediction import predict, risk_category


def test_risk_category():
    assert risk_category(0.1) == "low"
    assert risk_category(0.45) == "moderate"
    assert risk_category(0.8) == "high"


def test_predict_high_risk_case():
    features = {
        "Pregnancies": 6,
        "Glucose": 148,
        "BloodPressure": 72,
        "SkinThickness": 35,
        "Insulin": 0,
        "BMI": 33.6,
        "DiabetesPedigreeFunction": 0.627,
        "Age": 50,
    }
    result = predict(features)
    assert "probability" in result
    assert 0.0 <= result["probability"] <= 1.0
    assert result["risk_category"] in ("low", "moderate", "high")
    assert result["model_version"]
    assert "Pima" in result["data_source_note"]
    assert result["feature_contributions"] is not None
    assert len(result["feature_contributions"]) == 8
    assert result["uncertainty"] is not None


def test_predict_low_risk_case():
    features = {
        "Pregnancies": 1,
        "Glucose": 85,
        "BloodPressure": 66,
        "SkinThickness": 29,
        "Insulin": 0,
        "BMI": 26.6,
        "DiabetesPedigreeFunction": 0.351,
        "Age": 31,
    }
    result = predict(features)
    assert result["probability"] < 0.5
