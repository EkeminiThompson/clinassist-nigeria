from pydantic import ValidationError
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
import pytest
from backend.app.services.prediction import build_classifier
from backend.app.schemas import PredictionRequest

def _payload(model_name=None):
    payload={"features":{"Pregnancies":1,"Glucose":100,"BloodPressure":70,"SkinThickness":20,
        "Insulin":80,"BMI":25,"DiabetesPedigreeFunction":0.4,"Age":35}}
    if model_name is not None:
        payload["model_name"]=model_name
    return payload

def test_model_registry_exposes_three_supported_estimators():
    assert isinstance(build_classifier("logistic_regression"),LogisticRegression)
    assert isinstance(build_classifier("random_forest"),RandomForestClassifier)
    assert isinstance(build_classifier("xgboost"),XGBClassifier)

def test_model_registry_rejects_unknown_models():
    with pytest.raises(ValueError):
        build_classifier("unsupported")

def test_prediction_request_defaults_to_logistic_model():
    assert PredictionRequest(**_payload()).model_name=="logistic_regression"

def test_prediction_request_rejects_unknown_model():
    with pytest.raises(ValidationError):
        PredictionRequest(**_payload("svm"))
