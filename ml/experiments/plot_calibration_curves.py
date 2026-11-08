"""Create descriptive calibration plots from repeated held-out predictions.

Predictions from repeated splits overlap. This script averages each participant's
held-out probabilities across the seeds in which they appear, so each source
row contributes at most once to each model/scenario/adaptation curve. The
result is descriptive and must not be presented as external validation or as
a confidence-interval estimate.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import calibration_curve

MODELS = ("logistic_regression", "random_forest", "hist_gradient_boosting")
SCENARIOS = ("reference", "combined_severe")
ARMS = ("source_only", "coral")


def make_calibration_figures(prediction_path: Path, output_dir: Path, bins: int = 8) -> pd.DataFrame:
    predictions = pd.read_csv(prediction_path)
    required = {
        "source_row_index", "seed", "model", "shift_scenario",
        "adaptation", "y_true", "probability",
    }
    missing = required - set(predictions.columns)
    if missing:
        raise ValueError(f"Prediction file is missing columns: {sorted(missing)}")
    if not predictions["y_true"].isin([0, 1]).all():
        raise ValueError("y_true must contain binary labels")
    if not predictions["probability"].between(0, 1).all():
        raise ValueError("probability must be finite and in [0, 1]")
    if predictions["probability"].isna().any():
        raise ValueError("probability contains missing values")
    output_dir.mkdir(parents=True, exist_ok=True)
    curve_rows = []

    for model in MODELS:
        fig, axis = plt.subplots(figsize=(7.5, 6))
        axis.plot([0, 1], [0, 1], linestyle="--", label="Ideal calibration")
        for scenario in SCENARIOS:
            for arm in ARMS:
                subset = predictions[
                    (predictions["model"] == model)
                    & (predictions["shift_scenario"] == scenario)
                    & (predictions["adaptation"] == arm)
                ]
                if subset.empty:
                    raise ValueError(f"No predictions for {model}/{scenario}/{arm}")
                patient_level = (
                    subset.groupby("source_row_index", as_index=False)
                    .agg(
                        y_true=("y_true", "first"),
                        probability=("probability", "mean"),
                        heldout_seed_count=("seed", "nunique"),
                    )
                )
                fraction_positive, mean_predicted = calibration_curve(
                    patient_level["y_true"],
                    patient_level["probability"],
                    n_bins=bins,
                    strategy="quantile",
                )
                label = f"{scenario.replace('_', ' ')} / {arm}"
                axis.plot(mean_predicted, fraction_positive, marker="o", label=label)
                for index, (mean_p, fraction_p) in enumerate(
                    zip(mean_predicted, fraction_positive), start=1
                ):
                    curve_rows.append({
                        "model": model,
                        "scenario": scenario,
                        "adaptation": arm,
                        "quantile_bin": index,
                        "mean_predicted_probability": float(mean_p),
                        "observed_fraction_positive": float(fraction_p),
                        "n_unique_patients": int(len(patient_level)),
                        "mean_heldout_seed_count": float(
                            patient_level["heldout_seed_count"].mean()
                        ),
                        "aggregation": "mean held-out probability per source row across seeds",
                        "uncertainty": "not estimated",
                    })

        axis.set(
            xlabel="Mean predicted probability",
            ylabel="Observed event fraction",
            title=f"Calibration: {model.replace('_', ' ').title()}",
            xlim=(0, 1),
            ylim=(0, 1),
        )
        axis.legend(fontsize=8, loc="best")
        fig.tight_layout()
        fig.savefig(output_dir / f"calibration_{model}.png", dpi=220, bbox_inches="tight")
        plt.close(fig)

    curves = pd.DataFrame(curve_rows)
    curves.to_csv(output_dir / "calibration_curve_points.csv", index=False)
    return curves


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predictions",
        type=Path,
        default=Path("ml/artifacts/experiments/synthetic_shift_predictions.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("ml/artifacts/figures/calibration"),
    )
    parser.add_argument("--bins", type=int, default=8)
    args = parser.parse_args()
    if args.bins < 2:
        parser.error("--bins must be at least 2")
    result = make_calibration_figures(args.predictions, args.output_dir, args.bins)
    print({
        "curve_points": len(result),
        "models": sorted(result["model"].unique().tolist()),
        "output_dir": str(args.output_dir),
        "note": "Descriptive repeated-split aggregation; no confidence intervals.",
    })
