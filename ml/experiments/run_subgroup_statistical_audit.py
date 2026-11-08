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

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "ml/datasets/diabetes_dataset.csv"
PRED = ROOT / "ml/artifacts/experiments/synthetic_shift_predictions.csv"
OUT = ROOT / "ml/artifacts/experiments"

def safe_metrics(y, p):
    y = np.asarray(y, dtype=int); p = np.asarray(p, dtype=float)
    return {
        "n": int(len(y)),
        "events": int(y.sum()),
        "prevalence": float(y.mean()) if len(y) else None,
        "auroc": float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None,
        "auprc": float(average_precision_score(y, p)) if y.sum() else None,
        "brier": float(brier_score_loss(y, p)) if len(y) else None,
    }

def run_audit(n_bootstrap=1000, seed=2026):
    X, y = load_pima_benchmark(str(DATA))
    predictions = pd.read_csv(PRED)
    demo = X.copy()
    demo["source_row_index"] = np.arange(len(demo))
    demo["y_reference"] = y.to_numpy()
    demo["age_group"] = pd.cut(demo["Age"], [-np.inf, 29, 49, np.inf],
                               labels=["<30", "30-49", "50+"])
    demo["BMI_for_group"] = demo["BMI"].replace(0, np.nan)\n    demo["bmi_group"] = pd.cut(demo["BMI_for_group"], [-np.inf, 18.5, 25, 30, np.inf],
                               right=False,
                               labels=["<18.5", "18.5-24.9", "25-29.9", ">=30"])
    predictions = predictions.merge(demo, on="source_row_index", how="left", validate="many_to_one")
    if predictions["Age"].isna().any():
        raise ValueError("Could not join every prediction to benchmark demographics")
    subgroup_rows = []
    keys = ["seed", "model", "shift_scenario", "adaptation"]
    for key, frame in predictions.groupby(keys, observed=True):
        for variable in ("age_group", "bmi_group"):
            for subgroup, part in frame.groupby(variable, observed=True):
                metrics = safe_metrics(part["y_true"], part["probability"])
                subgroup_rows.append(dict(zip(keys, key), subgroup_variable=variable,
                    subgroup=str(subgroup), **metrics))
    subgroup_frame = pd.DataFrame(subgroup_rows)
    subgroup_frame.to_csv(OUT / "subgroup_metrics.csv", index=False)

    rng = np.random.default_rng(seed)
    paired_rows = []
    pair_keys = ["seed", "model", "shift_scenario"]
    for key, frame in predictions.groupby(pair_keys, observed=True):
        wide = frame.pivot(index="source_row_index", columns="adaptation",
                           values=["y_true", "probability"])
        if not {"source_only", "coral"}.issubset(set(wide["probability"].columns)):
            continue
        y_true = wide[("y_true", "source_only")].to_numpy(dtype=int)
        p_source = wide[("probability", "source_only")].to_numpy(dtype=float)
        p_coral = wide[("probability", "coral")].to_numpy(dtype=float)
        if not np.array_equal(y_true, wide[("y_true", "coral")].to_numpy(dtype=int)):
            raise ValueError("Paired adaptations do not share identical held-out labels")
        point = {
            "auroc": (roc_auc_score(y_true, p_coral) - roc_auc_score(y_true, p_source))
                if len(np.unique(y_true)) == 2 else np.nan,
            "auprc": average_precision_score(y_true, p_coral) - average_precision_score(y_true, p_source),
            "brier": brier_score_loss(y_true, p_coral) - brier_score_loss(y_true, p_source),
        }
        boot = {metric: [] for metric in point}
        n = len(y_true)
        for _ in range(n_bootstrap):
            ix = rng.integers(0, n, n)
            ys = y_true[ix]
            for metric in point:
                if metric == "auroc" and len(np.unique(ys)) < 2:
                    continue
                if metric == "auroc":
                    value = roc_auc_score(ys, p_coral[ix]) - roc_auc_score(ys, p_source[ix])
                elif metric == "auprc":
                    value = average_precision_score(ys, p_coral[ix]) - average_precision_score(ys, p_source[ix])
                else:
                    value = brier_score_loss(ys, p_coral[ix]) - brier_score_loss(ys, p_source[ix])
                boot[metric].append(float(value))
        for metric, estimate in point.items():
            vals = boot[metric]
            lower, upper = (np.quantile(vals, [.025, .975]).tolist() if vals else (np.nan, np.nan))
            paired_rows.append(dict(zip(pair_keys, key), metric=metric,
                coral_minus_source_only=float(estimate), bootstrap_lower_95=float(lower),
                bootstrap_upper_95=float(upper), valid_bootstrap_replicates=len(vals), n_patients=n))
    paired = pd.DataFrame(paired_rows)
    paired.to_csv(OUT / "paired_bootstrap_differences.csv", index=False)
    summary = paired.groupby(["model", "shift_scenario", "metric"], observed=True).agg(
        mean_split_delta=("coral_minus_source_only", "mean"),
        sd_split_delta=("coral_minus_source_only", "std"),
        min_split_ci_lower=("bootstrap_lower_95", "min"),
        max_split_ci_upper=("bootstrap_upper_95", "max"),
        n_splits=("seed", "nunique")).reset_index()
    summary.to_csv(OUT / "paired_bootstrap_summary.csv", index=False)
    print(f"Subgroup rows: {len(subgroup_frame)}; paired bootstrap rows: {len(paired)}")
    print("Outputs: subgroup_metrics.csv, paired_bootstrap_differences.csv, paired_bootstrap_summary.csv")
    print("Interpretation: exploratory Pima benchmark strata; not fairness certification or external validation.")
    return subgroup_frame, paired, summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bootstrap", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=2026)
    args = parser.parse_args()
    if args.bootstrap < 100:
        parser.error("--bootstrap must be >=100")
    run_audit(args.bootstrap, args.seed)
