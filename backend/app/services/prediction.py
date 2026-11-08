"""
Prediction service with uncertainty and coefficient-based explanations.
Trained on public Pima benchmark only – clearly labelled.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from ml.preprocessing.pipeline import (  # noqa: E402
    FEATURE_COLUMNS,
    build_preprocessing_pipeline,
    load_pima_benchmark,
)
from ml.uncertainty.selective import entropy_uncertainty  # noqa: E402

logger = logging.getLogger(__name__)

DATA_PATH = _ROOT / "ml" / "datasets" / "diabetes_dataset.csv"
MODEL_DIR = _ROOT / "ml" / "artifacts" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "baseline_logistic.joblib"

MODEL_VERSION = "baseline-lr-0.1.0"
DATA_SOURCE_NOTE = (
    "Model trained on the public Pima Indians Diabetes dataset "
    "(methodological benchmark only). Not Nigerian multi-hospital data. "
    "See docs/dataset_provenance.md."
)


def _train_and_persist_baseline() -> Pipeline:
    X, y = load_pima_benchmark(str(DATA_PATH))
    pipe = Pipeline(
        [
            ("preprocess", build_preprocessing_pipeline(impute_strategy="median", scale=True)),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000, C=1.0, class_weight="balanced", random_state=42
                ),
            ),
        ]
    )
    pipe.fit(X, y)
    joblib.dump(pipe, MODEL_PATH)
    logger.info("Baseline model trained and saved to %s", MODEL_PATH)
    return pipe


def load_model() -> Pipeline:
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return _train_and_persist_baseline()


def risk_category(prob: float) -> str:
    if prob < 0.3:
        return "low"
    if prob < 0.6:
        return "moderate"
    return "high"


def compute_shap_style_contributions(
    model: Pipeline, features: Dict[str, float]
) -> List[Dict[str, Any]]:
    clf = model.named_steps["clf"]
    preprocess = model.named_steps["preprocess"]
    row = pd.DataFrame([features])[FEATURE_COLUMNS]
    X_scaled = preprocess.transform(row)
    if hasattr(X_scaled, "values"):
        X_scaled = X_scaled.values
    X_scaled = np.asarray(X_scaled).ravel()
    coefs = clf.coef_.ravel()
    contributions = []
    for i, name in enumerate(FEATURE_COLUMNS):
        contrib = float(coefs[i] * X_scaled[i])
        contributions.append(
            {
                "feature": name,
                "value": float(features[name]),
                "contribution": contrib,
                "direction": "increases_risk" if contrib > 0 else "decreases_risk",
            }
        )
    contributions.sort(key=lambda x: abs(x["contribution"]), reverse=True)
    return contributions


def predict(
    features: Dict[str, float],
    return_explanation: bool = True,
    return_uncertainty: bool = True,
    uncertainty_threshold: float = 0.5,
) -> Dict[str, Any]:
    model = load_model()
    row = pd.DataFrame([features])[FEATURE_COLUMNS]
    proba = float(model.predict_proba(row)[0, 1])
    pred = int(proba >= 0.5)

    uncertainty = None
    abstain = False
    if return_uncertainty:
        uncertainty = float(entropy_uncertainty(np.array([proba]))[0])
        abstain = uncertainty > uncertainty_threshold

    contributions = None
    if return_explanation:
        contributions = compute_shap_style_contributions(model, features)

    confidence_statement = (
        "Model abstains due to high uncertainty – clinician review recommended."
        if abstain
        else f"Predicted probability of diabetes: {proba:.1%}. Risk category: {risk_category(proba)}."
    )

    limitations = [
        "Trained on public Pima Indians Diabetes dataset (methodological benchmark).",
        "Not validated on Nigerian multi-hospital data.",
        "Statistical associations only – not causal explanations.",
        "Missing or out-of-distribution values may reduce reliability.",
    ]

    return {
        "model_version": MODEL_VERSION,
        "data_source_note": DATA_SOURCE_NOTE,
        "probability": proba,
        "risk_category": risk_category(proba),
        "prediction": pred if not abstain else -1,
        "abstain": abstain,
        "uncertainty": uncertainty,
        "uncertainty_measure": "binary_entropy" if uncertainty is not None else None,
        "confidence_statement": confidence_statement,
        "feature_contributions": contributions,
        "limitations": limitations,
    }
