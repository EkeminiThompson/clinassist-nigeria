"""Exact paired sign-flip tests for the frozen five-split CORAL comparison.

Input: ml/artifacts/experiments/synthetic_shift_paired_differences.csv
Output: ml/artifacts/experiments/paired_sign_flip_tests.csv

The unit of pairing is the repeated train/test split (five seeds), not the
individual patient. Two-sided exact sign-flip tests assume exchangeable signs
under the null. With n=5 there are only 32 sign assignments and the minimum
attainable two-sided p-value is 0.0625. These are exploratory tests, not
confirmatory evidence of clinical or population-level effects.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "ml/artifacts/experiments/synthetic_shift_paired_differences.csv"
OUTPUT = ROOT / "ml/artifacts/experiments/paired_sign_flip_tests.csv"
METRICS = ("auroc", "brier", "ece")


def exact_sign_flip(values: np.ndarray) -> tuple[float, float, float, int]:
    values = np.asarray(values, dtype=float)
    observed = float(values.mean())
    signs = np.asarray(list(product((-1.0, 1.0), repeat=len(values))))
    null_means = (signs * values[None, :]).mean(axis=1)
    p_value = float(np.mean(np.abs(null_means) >= abs(observed) - 1e-12))
    return observed, float(values.std(ddof=1)), p_value, len(null_means)


def main() -> None:
    frame = pd.read_csv(INPUT)
    frame = frame[frame["metric"].isin(METRICS)]
    rows = []
    for (metric, scenario, model), group in frame.groupby(
        ["metric", "shift_scenario", "model"], sort=True
    ):
        values = group.sort_values("seed")["coral_minus_source_only"].to_numpy()
        mean, sd, p, permutations = exact_sign_flip(values)
        rows.append({
            "metric": metric, "scenario": scenario, "model": model,
            "n": len(values), "mean_delta": mean, "sd_delta": sd,
            "exact_two_sided_sign_flip_p": p,
            "sign_assignments": permutations,
        })
    result = pd.DataFrame(rows)
    result["holm_adjusted_p"] = np.nan
    for metric in METRICS:
        mask = result["metric"].eq(metric)
        ordered = result.loc[mask].sort_values("exact_two_sided_sign_flip_p")
        m = len(ordered)
        adjusted = []
        running = 0.0
        for rank, p in enumerate(ordered["exact_two_sided_sign_flip_p"], start=1):
            running = max(running, min(1.0, (m - rank + 1) * float(p)))
            adjusted.append(running)
        result.loc[ordered.index, "holm_adjusted_p"] = adjusted
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT, index=False, float_format="%.8f")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
