"""Exploratory subgroup and paired-bootstrap audit of synthetic-shift predictions.

Subgroups are descriptive benchmark strata, not Nigerian demographic fairness evidence.
Bootstrap resampling is paired within each held-out split; split-level intervals are
reported separately to avoid pretending repeated overlapping splits are independent.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from ml.preprocessing.pipeline import load_pima_benchmark
from ml.evaluation.metrics import full_evaluation

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "ml/datasets/diabetes_dataset.csv"
PRED = ROOT / "ml/artifacts/experiments/synthetic_shift_predictions.csv"
OUT = ROOT / "ml/artifacts/experiments"

def safe_metrics(y, p):
    return {"n": int(len(y)), "events": int(np.asarray(y).sum()),
            "prevalence": float(np.asarray(y).mean()), **full_evaluation(y, p)}

