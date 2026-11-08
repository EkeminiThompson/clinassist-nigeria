"""
CORAL (Correlation Alignment) domain adaptation for tabular clinical data.
Suitable for small-sample regimes.
"""

from __future__ import annotations

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


def coral_transform(
    source: np.ndarray, target: np.ndarray, epsilon: float = 1e-5
) -> np.ndarray:
    """
    Align second-order statistics of source to target.
    Returns the transformed source features.
    """
    source = np.asarray(source, dtype=float)
    target = np.asarray(target, dtype=float)

    cs = np.cov(source, rowvar=False) + epsilon * np.eye(source.shape[1])
    ct = np.cov(target, rowvar=False) + epsilon * np.eye(target.shape[1])

    us, ss, _ = np.linalg.svd(cs)
    ut, st, _ = np.linalg.svd(ct)

    ss = np.maximum(ss, epsilon)
    st = np.maximum(st, epsilon)

    whitening = us @ np.diag(1.0 / np.sqrt(ss)) @ us.T
    colouring = ut @ np.diag(np.sqrt(st)) @ ut.T

    source_centered = source - source.mean(axis=0)
    transformed = source_centered @ whitening @ colouring
    transformed = transformed + target.mean(axis=0)
    return transformed


class CORALAdapter(BaseEstimator, TransformerMixin):
    """
    sklearn-compatible transformer that aligns source features
    to a target distribution using CORAL.
    Fit on (source_X, target_X); transform applies the mapping.
    """

    def __init__(self, epsilon: float = 1e-5):
        self.epsilon = epsilon
        self.source_mean_: np.ndarray | None = None
        self.whitening_: np.ndarray | None = None
        self.colouring_: np.ndarray | None = None
        self.target_mean_: np.ndarray | None = None

    def fit(self, source_X: np.ndarray, target_X: np.ndarray):
        source_X = np.asarray(source_X, dtype=float)
        target_X = np.asarray(target_X, dtype=float)

        self.source_mean_ = source_X.mean(axis=0)
        self.target_mean_ = target_X.mean(axis=0)

        cs = np.cov(source_X, rowvar=False) + self.epsilon * np.eye(source_X.shape[1])
        ct = np.cov(target_X, rowvar=False) + self.epsilon * np.eye(target_X.shape[1])

        us, ss, _ = np.linalg.svd(cs)
        ut, st, _ = np.linalg.svd(ct)
        ss = np.maximum(ss, self.epsilon)
        st = np.maximum(st, self.epsilon)

        self.whitening_ = us @ np.diag(1.0 / np.sqrt(ss)) @ us.T
        self.colouring_ = ut @ np.diag(np.sqrt(st)) @ ut.T
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.whitening_ is None:
            raise RuntimeError("CORALAdapter must be fitted before transform.")
        X = np.asarray(X, dtype=float)
        centered = X - self.source_mean_
        return centered @ self.whitening_ @ self.colouring_ + self.target_mean_
