"""
Reproducible baseline experiments for ClinAssist Nigeria.
Uses only the public Pima benchmark (explicitly labelled).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from xgboost import XGBClassifier

# Local imports
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ml.evaluation.metrics import full_evaluation
from ml.preprocessing.pipeline import build_preprocessing_pipeline, load_pima_benchmark

RANDOM_SEED = 42
N_SPLITS = 5
DATA_PATH = ROOT / "ml" / "datasets" / "diabetes_dataset.csv"
RESULTS_DIR = ROOT / "ml" / "artifacts" / "experiments"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def get_models():
    return {
        "logistic_regression": LogisticRegression(max_iter=1000, random_state=RANDOM_SEED),
        "random_forest": RandomForestClassifier(
            n_estimators=200, max_depth=6, random_state=RANDOM_SEED, n_jobs=-1
        ),
        "gradient_boosting": GradientBoostingClassifier(
            n_estimators=150, max_depth=3, random_state=RANDOM_SEED
        ),
        "xgboost": XGBClassifier(
            n_estimators=150,
            max_depth=3,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_SEED,
            eval_metric="logloss",
            verbosity=0,
        ),
        "svm_rbf": SVC(kernel="rbf", probability=True, random_state=RANDOM_SEED),
    }


def run_cv_baselines():
    X, y = load_pima_benchmark(str(DATA_PATH))
    X = X.values
    y = y.values

    cv = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)
    results = {}
    prediction_rows = []
    fold_ids = np.full(len(y), -1, dtype=int)
    for fold_number, (_, test_indices) in enumerate(cv.split(X, y), start=1):
        fold_ids[test_indices] = fold_number

    for name, model in get_models().items():
        pipe = Pipeline(
            [
                ("preprocess", build_preprocessing_pipeline(impute_strategy="median", scale=True)),
                ("clf", model),
            ]
        )
        # Out-of-fold probabilities for honest evaluation
        oof_prob = cross_val_predict(
            pipe, X, y, cv=cv, method="predict_proba", n_jobs=-1
        )[:, 1]

        metrics = full_evaluation(y, oof_prob)
        results[name] = metrics
        prediction_rows.extend({
            "model": name,
            "dataset_row_index": int(row_index),
            "fold": int(fold_ids[row_index]),
            "y_true": int(y[row_index]),
            "probability": float(oof_prob[row_index]),
        } for row_index in range(len(y)))
        print(f"{name:20s}  AUROC={metrics['auroc']:.4f}  AUPRC={metrics['auprc']:.4f}  "
              f"Brier={metrics['brier']:.4f}  ECE={metrics['ece']:.4f}")

    out_path = RESULTS_DIR / "baseline_cv_results.json"
    with open(out_path, "w") as f:
        json.dump(
            {
                "data_source": "Public Pima Indians Diabetes (UCI) – methodological benchmark only",
                "note": "Not Nigerian multi-hospital data. See docs/dataset_provenance.md",
                "n_samples": int(len(y)),
                "n_splits": N_SPLITS,
                "random_seed": RANDOM_SEED,
                "results": results,
            },
            f,
            indent=2,
        )
    predictions_path = RESULTS_DIR / "baseline_cv_predictions.csv"
    pd.DataFrame(prediction_rows).to_csv(predictions_path, index=False)
    print(f"\nResults written to {out_path}")
    print(f"Unaggregated out-of-fold predictions written to {predictions_path}")
    return results


if __name__ == "__main__":
    run_cv_baselines()
