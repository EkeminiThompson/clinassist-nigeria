"""
Uncertainty quantification and selective prediction utilities.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin, clone


def bootstrap_uncertainty(
    model: BaseEstimator,
    X: np.ndarray,
    y: np.ndarray,
    X_test: np.ndarray,
    n_bootstrap: int = 30,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simple bootstrap ensemble for uncertainty estimation.
    Returns mean probability and standard deviation across bootstrap models.
    Suitable for small tabular datasets.
    """
    rng = np.random.RandomState(random_state)
    n = len(y)
    probs = []

    for i in range(n_bootstrap):
        idx = rng.choice(n, size=n, replace=True)
        m = clone(model)
        m.fit(X[idx], y[idx])
        if hasattr(m, "predict_proba"):
            p = m.predict_proba(X_test)[:, 1]
        else:
            p = m.predict(X_test).astype(float)
        probs.append(p)

    probs = np.stack(probs, axis=0)
    mean_prob = probs.mean(axis=0)
    std_prob = probs.std(axis=0)
    return mean_prob, std_prob


def entropy_uncertainty(prob: np.ndarray) -> np.ndarray:
    """Binary entropy as a simple uncertainty measure."""
    p = np.clip(prob, 1e-8, 1 - 1e-8)
    return -p * np.log(p) - (1 - p) * np.log(1 - p)


class SelectiveClassifier(BaseEstimator, ClassifierMixin):
    """
    Wrapper that abstains when uncertainty exceeds a threshold.
    Abstention is indicated by prediction = -1.
    """

    def __init__(self, base_estimator: BaseEstimator, uncertainty_threshold: float = 0.5):
        self.base_estimator = base_estimator
        self.uncertainty_threshold = uncertainty_threshold

    def fit(self, X, y):
        self.base_estimator_ = clone(self.base_estimator)
        self.base_estimator_.fit(X, y)
        return self

    def predict_proba(self, X):
        return self.base_estimator_.predict_proba(X)

    def predict(self, X, uncertainty: np.ndarray | None = None):
        proba = self.predict_proba(X)[:, 1]
        pred = (proba >= 0.5).astype(int)
        if uncertainty is not None:
            pred = pred.copy()
            pred[uncertainty > self.uncertainty_threshold] = -1  # abstain
        return pred
