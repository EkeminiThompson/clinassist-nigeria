"""Fast, paired subgroup bootstrap audit of held-out Pima predictions.

Exploratory age/BMI strata only. This is not Nigerian fairness evidence or
external clinical validation. Bootstrap resampling is paired by patient row
within each seed/model/scenario and preserves the source-only/CORAL pairing.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from ml.preprocessing.pipeline import load_pima_benchmark

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "ml/datasets/diabetes_dataset.csv"
PRED = ROOT / "ml/artifacts/experiments/synthetic_shift_predictions.csv"
OUT = ROOT / "ml/artifacts/experiments"
MIN_N = 20
MIN_CLASS = 5
MIN_VALID_FRACTION = 0.90
BOOTSTRAP_BATCH_SIZE = 128


def _subgroups(features: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=features.index)
    age = pd.to_numeric(features["Age"], errors="coerce")
    out["age_group"] = pd.cut(
        age, bins=[-np.inf, 29, 49, np.inf],
        labels=["<30", "30-49", "50+"], right=True,
    ).astype("object")
    bmi = pd.to_numeric(features["BMI"], errors="coerce").replace(0, np.nan)
    out["bmi_group"] = pd.cut(
        bmi, bins=[-np.inf, 18.5, 25, 30, np.inf],
        labels=["<18.5", "18.5-24.9", "25-29.9", ">=30"], right=False,
    ).astype("object")
    out.loc[bmi.isna(), "bmi_group"] = np.nan
    return out


def _validate_vectors(y, *probabilities) -> np.ndarray:
    y = np.asarray(y, dtype=int)
    if y.ndim != 1 or not np.isin(y, [0, 1]).all():
        raise ValueError("y must be a one-dimensional binary array")
    for p in probabilities:
        p = np.asarray(p, dtype=float)
        if p.shape != y.shape:
            raise ValueError("Each probability vector must match y")
        if not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
            raise ValueError("Probabilities must be finite and in [0, 1]")
    return y


def _metrics(y: np.ndarray, p: np.ndarray) -> dict:
    y = _validate_vectors(y, p)
    p = np.asarray(p, dtype=float)
    result = {
        "n": int(len(y)),
        "events": int(y.sum()),
        "prevalence": float(y.mean()) if len(y) else float("nan"),
    }
    if len(y) < MIN_N or y.sum() < MIN_CLASS or (len(y) - y.sum()) < MIN_CLASS:
        result.update({
            "eligible_for_metrics": False,
            "auroc": np.nan, "auprc": np.nan, "brier": np.nan,
        })
        return result
    result.update({
        "eligible_for_metrics": True,
        "auroc": float(roc_auc_score(y, p)),
        "auprc": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)),
    })
    return result


def _average_precision_batch(labels: np.ndarray, scores: np.ndarray) -> np.ndarray:
    """Exact sklearn-style average precision for rows, including tied scores."""
    order = np.argsort(-scores, axis=1, kind="mergesort")
    sorted_labels = np.take_along_axis(labels, order, axis=1)
    sorted_scores = np.take_along_axis(scores, order, axis=1)
    cumulative_positives = np.cumsum(sorted_labels, axis=1)
    group_ends = np.ones(sorted_labels.shape, dtype=bool)
    group_ends[:, :-1] = sorted_scores[:, :-1] != sorted_scores[:, 1:]
    previous_group_positives = np.concatenate([
        np.zeros((len(labels), 1), dtype=float),
        np.maximum.accumulate(np.where(
            group_ends[:, :-1], cumulative_positives[:, :-1], 0
        ), axis=1),
    ], axis=1)
    group_positives = cumulative_positives - previous_group_positives
    precision_at_group_end = cumulative_positives / np.arange(
        1, labels.shape[1] + 1, dtype=float
    )[None, :]
    return np.sum(
        group_positives * precision_at_group_end * group_ends, axis=1
    ) / labels.sum(axis=1)


def _paired_bootstrap(y, p_source, p_coral, n_bootstrap, rng):
    """Vectorised patient bootstrap; CORAL and source-only share each draw."""
    y = _validate_vectors(y, p_source, p_coral)
    ps = np.asarray(p_source, dtype=float)
    pc = np.asarray(p_coral, dtype=float)
    empty = {
        f"{metric}_{suffix}": np.nan
        for metric in ("auroc", "auprc", "brier")
        for suffix in ("delta", "ci_lower", "ci_upper")
    }
    if len(y) < MIN_N or y.sum() < MIN_CLASS or (len(y) - y.sum()) < MIN_CLASS:
        return {
            "valid_replicates": 0, **empty,
            "status": "insufficient subgroup events",
        }

    n = len(y)
    deltas = {"auroc": [], "auprc": [], "brier": []}
    valid = 0
    remaining = n_bootstrap

    while remaining:
        batch = min(BOOTSTRAP_BATCH_SIZE, remaining)
        indices = rng.integers(0, n, size=(batch, n))
        yy = y[indices]
        positives = yy.sum(axis=1)
        keep = (positives > 0) & (positives < n)
        if keep.any():
            yy = yy[keep]
            a = ps[indices[keep]]
            b = pc[indices[keep]]
            positives = positives[keep].astype(float)
            negatives = n - positives
            valid += len(yy)

            # Rank-based AUROC with average ranks for tied probabilities.
            ranks_a = rankdata(a, axis=1, method="average")
            ranks_b = rankdata(b, axis=1, method="average")
            auc_a = (np.sum(ranks_a * yy, axis=1) - positives * (positives + 1) / 2) / (positives * negatives)
            auc_b = (np.sum(ranks_b * yy, axis=1) - positives * (positives + 1) / 2) / (positives * negatives)
            deltas["auroc"].extend((auc_b - auc_a).tolist())

            # Average precision: mean precision at each positive's rank.
            ap_a = _average_precision_batch(yy, a)
            ap_b = _average_precision_batch(yy, b)
            deltas["auprc"].extend((ap_b - ap_a).tolist())

            # Brier delta is the paired mean squared-error difference.
            brier_a = np.mean((a - yy) ** 2, axis=1)
            brier_b = np.mean((b - yy) ** 2, axis=1)
            deltas["brier"].extend((brier_b - brier_a).tolist())
        remaining -= batch

    result = {"valid_replicates": int(valid)}
    if valid < int(n_bootstrap * MIN_VALID_FRACTION):
        return {
            **result, **empty,
            "status": "too few valid bootstrap replicates",
        }

    for metric, values in deltas.items():
        values = np.asarray(values, dtype=float)
        result[f"{metric}_delta"] = float(values.mean())
        result[f"{metric}_ci_lower"] = float(np.quantile(values, 0.025))
        result[f"{metric}_ci_upper"] = float(np.quantile(values, 0.975))
    result["status"] = "ok"
    return result


def run_audit(n_bootstrap=1000, seed=2026):
    if n_bootstrap < 100:
        raise ValueError("Use at least 100 bootstrap replicates")

    X, y = load_pima_benchmark(str(DATA))
    X = X.reset_index(drop=True)
    y = np.asarray(y, dtype=int)
    subgroup = _subgroups(X)

    predictions = pd.read_csv(PRED)
    required = {
        "seed", "source_row_index", "model", "shift_scenario",
        "adaptation", "y_true", "probability",
    }
    missing = required - set(predictions.columns)
    if missing:
        raise ValueError(f"Prediction file missing columns: {sorted(missing)}")

    predictions["source_row_index"] = pd.to_numeric(
        predictions["source_row_index"], errors="raise"
    ).astype(int)
    if not predictions["source_row_index"].between(0, len(y) - 1).all():
        raise ValueError("Prediction source_row_index is outside benchmark rows")
    predictions["y_true"] = pd.to_numeric(predictions["y_true"], errors="raise").astype(int)
    predictions["probability"] = pd.to_numeric(
        predictions["probability"], errors="raise"
    ).astype(float)
    _validate_vectors(
        predictions["y_true"].to_numpy(),
        predictions["probability"].to_numpy(),
    )
    expected_labels = y[predictions["source_row_index"].to_numpy()]
    if not np.array_equal(expected_labels, predictions["y_true"].to_numpy()):
        raise ValueError("Prediction labels do not match their benchmark source_row_index")

    predictions = predictions.merge(
        subgroup, left_on="source_row_index", right_index=True,
        how="left", validate="many_to_one",
    )
    predictions["overall_group"] = "all"
    group_specs = [
        ("overall_group", ["all"]),
        ("age_group", ["<30", "30-49", "50+"]),
        ("bmi_group", ["<18.5", "18.5-24.9", "25-29.9", ">=30"]),
    ]

    metric_rows = []
    bootstrap_rows = []
    rng = np.random.default_rng(seed)

    for group_col, labels in group_specs:
        for label in labels:
            subset = predictions[predictions[group_col] == label]
            for (split, model, scenario), part in subset.groupby(
                ["seed", "model", "shift_scenario"], sort=True
            ):
                if part.duplicated(["source_row_index", "adaptation"]).any():
                    raise ValueError("Duplicate patient/adaptation prediction rows")
                arms = set(part["adaptation"].unique())
                if arms != {"source_only", "coral"}:
                    raise ValueError(f"Expected paired source_only/coral arms, got {sorted(arms)}")

                for adaptation, arm in part.groupby("adaptation", sort=True):
                    m = _metrics(
                        arm["y_true"].to_numpy(),
                        arm["probability"].to_numpy(),
                    )
                    metric_rows.append({
                        "subgroup_type": group_col, "subgroup": label,
                        "seed": int(split), "model": model,
                        "shift_scenario": scenario, "adaptation": adaptation, **m,
                    })

                wide = part.pivot(
                    index="source_row_index", columns="adaptation",
                    values=["y_true", "probability"],
                ).sort_index()
                if wide.isna().any().any():
                    raise ValueError("Source-only and CORAL arms must contain identical patient rows")
                y_source = wide[("y_true", "source_only")].to_numpy(dtype=int)
                y_coral = wide[("y_true", "coral")].to_numpy(dtype=int)
                if not np.array_equal(y_source, y_coral):
                    raise ValueError("Paired predictions do not share identical held-out labels")
                result = _paired_bootstrap(
                    y_source,
                    wide[("probability", "source_only")].to_numpy(),
                    wide[("probability", "coral")].to_numpy(),
                    n_bootstrap, rng,
                )
                bootstrap_rows.append({
                    "subgroup_type": group_col, "subgroup": label,
                    "seed": int(split), "model": model,
                    "shift_scenario": scenario, "n": len(y_source),
                    "events": int(y_source.sum()), **result,
                })

    if not metric_rows or not bootstrap_rows:
        raise RuntimeError("Subgroup audit produced no result rows")

    metrics = pd.DataFrame(metric_rows)
    bootstrap = pd.DataFrame(bootstrap_rows)
    OUT.mkdir(parents=True, exist_ok=True)
    metrics_path = OUT / "subgroup_metrics.csv"
    bootstrap_path = OUT / "subgroup_paired_bootstrap.csv"
    metrics.to_csv(metrics_path, index=False)
    bootstrap.to_csv(bootstrap_path, index=False)

    if not metrics_path.stat().st_size or not bootstrap_path.stat().st_size:
        raise RuntimeError("Subgroup audit generated an empty output file")
    allowed_statuses = {"ok", "insufficient subgroup events"}
    unexpected = bootstrap[~bootstrap["status"].isin(allowed_statuses)]
    print({
        "subgroup_metric_rows": len(metrics),
        "paired_bootstrap_rows": len(bootstrap),
        "bootstrap_requested_per_comparison": n_bootstrap,
        "bootstrap_minimum_valid": int(n_bootstrap * MIN_VALID_FRACTION),
        "comparisons_with_unexpected_status": len(unexpected),
        "metrics_output": str(metrics_path),
        "bootstrap_output": str(bootstrap_path),
        "minimum_stratum_n": MIN_N,
        "minimum_events_per_class": MIN_CLASS,
        "interpretation": "Exploratory Pima strata only; not Nigerian external validation or fairness certification.",
    })
    if not unexpected.empty:
        raise RuntimeError(
            f"{len(unexpected)} paired-bootstrap comparisons failed validity requirements"
        )
    successful = bootstrap[bootstrap["status"] == "ok"]
    if not successful.empty and (
        (successful["valid_replicates"] < int(n_bootstrap * MIN_VALID_FRACTION)).any()
        or successful[["auroc_ci_lower", "auroc_ci_upper",
                       "auprc_ci_lower", "auprc_ci_upper",
                       "brier_ci_lower", "brier_ci_upper"]].isna().any().any()
    ):
        raise RuntimeError("Successful bootstrap rows contain invalid replicate counts or intervals")
    return metrics, bootstrap


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    run_audit(args.bootstrap, args.seed)
