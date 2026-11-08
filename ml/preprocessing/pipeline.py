"""
Leakage-safe preprocessing pipeline for ClinAssist Nigeria.
All transforms are fit only on training folds.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]
TARGET_COLUMN = "Outcome"

# Physiologically implausible zeros that should be treated as missing
ZERO_AS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]


class ZeroToMissingTransformer(BaseEstimator, TransformerMixin):
    """Replace physiologically impossible zeros with NaN.
    Accepts both pandas DataFrame and numpy ndarray.
    """

    def __init__(self, columns: List[str]):
        self.columns = columns
        self.feature_names_in_: Optional[List[str]] = None

    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            self.feature_names_in_ = list(X.columns)
        else:
            self.feature_names_in_ = FEATURE_COLUMNS
        return self

    def transform(self, X):
        if isinstance(X, pd.DataFrame):
            X = X.copy()
            for col in self.columns:
                if col in X.columns:
                    X.loc[X[col] == 0, col] = np.nan
            return X
        # ndarray path
        X = np.asarray(X, dtype=float).copy()
        names = self.feature_names_in_ or FEATURE_COLUMNS
        for col in self.columns:
            if col in names:
                idx = names.index(col)
                if idx < X.shape[1]:
                    X[X[:, idx] == 0, idx] = np.nan
        return X


def build_preprocessing_pipeline(
    impute_strategy: str = "median",
    scale: bool = True,
) -> Pipeline:
    """
    Construct a sklearn Pipeline that can be safely nested inside
    cross-validation or used with domain-adaptation folds.
    """
    steps = [
        ("zero_to_missing", ZeroToMissingTransformer(ZERO_AS_MISSING)),
        ("imputer", SimpleImputer(strategy=impute_strategy)),
    ]
    if scale:
        steps.append(("scaler", StandardScaler()))
    return Pipeline(steps)


def load_pima_benchmark(path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """Load the public Pima benchmark. Explicitly documented as non-Nigerian."""
    df = pd.read_csv(path)
    expected = set(FEATURE_COLUMNS + [TARGET_COLUMN])
    if not expected.issubset(df.columns):
        raise ValueError(f"Unexpected columns. Found: {df.columns.tolist()}")
    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].astype(int)
    return X, y


def add_missingness_indicator(
    X: pd.DataFrame, columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """Append binary missingness indicators (useful for missingness-aware models)."""
    columns = columns or ZERO_AS_MISSING
    X = X.copy()
    for col in columns:
        if col in X.columns:
            X[f"{col}_missing"] = X[col].isna().astype(int)
    return X
