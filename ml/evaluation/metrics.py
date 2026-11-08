"""
Evaluation metrics for ClinAssist Nigeria research experiments.
Includes discrimination, calibration, and selective-prediction metrics.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def compute_discrimination_metrics(
    y_true: np.ndarray, y_prob: np.ndarray, threshold: float = 0.5
) -> Dict[str, float]:
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    return {
        "auroc": float(roc_auc_score(y_true, y_prob)),
        "auprc": float(average_precision_score(y_true, y_prob)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "sensitivity": float(sensitivity),
        "specificity": float(specificity),
    }


def expected_calibration_error(
    y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10
) -> float:
    """Expected Calibration Error (ECE)."""
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    for i in range(n_bins):
        mask = (y_prob >= bins[i]) & (y_prob < bins[i + 1])
        if mask.sum() == 0:
            continue
        bin_acc = y_true[mask].mean()
        bin_conf = y_prob[mask].mean()
        ece += mask.mean() * abs(bin_acc - bin_conf)
    return float(ece)


def compute_calibration_metrics(
    y_true: np.ndarray, y_prob: np.ndarray
) -> Dict[str, float]:
    return {
        "brier": float(brier_score_loss(y_true, y_prob)),
        "ece": expected_calibration_error(y_true, y_prob),
    }


def selective_prediction_metrics(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    uncertainty: np.ndarray,
    coverage: float = 0.8,
) -> Dict[str, float]:
    """
    Evaluate selective classification: keep the most confident (lowest uncertainty)
    predictions covering the requested fraction of the test set.
    """
    n = len(y_true)
    keep_n = max(1, int(coverage * n))
    idx = np.argsort(uncertainty)[:keep_n]
    y_t = y_true[idx]
    y_p = y_prob[idx]
    disc = compute_discrimination_metrics(y_t, y_p)
    cal = compute_calibration_metrics(y_t, y_p)
    return {
        "coverage": float(keep_n / n),
        "selective_auroc": disc["auroc"],
        "selective_auprc": disc["auprc"],
        "selective_f1": disc["f1"],
        "selective_brier": cal["brier"],
        "selective_ece": cal["ece"],
    }


def full_evaluation(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    uncertainty: Optional[np.ndarray] = None,
    coverage: float = 0.8,
) -> Dict[str, float]:
    results = {}
    results.update(compute_discrimination_metrics(y_true, y_prob))
    results.update(compute_calibration_metrics(y_true, y_prob))
    if uncertainty is not None:
        results.update(
            selective_prediction_metrics(y_true, y_prob, uncertainty, coverage)
        )
    return results
