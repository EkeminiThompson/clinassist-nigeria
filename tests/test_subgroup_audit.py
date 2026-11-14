import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import average_precision_score
from ml.experiments.run_subgroup_statistical_audit import (
    _average_precision_batch, _metrics, _paired_bootstrap, _subgroups,
)


def test_subgroups_create_age_and_bmi_bands_and_exclude_zero_bmi():
    x = pd.DataFrame({"Age": [20, 35, 60, 40], "BMI": [17.0, 24.9, 30.0, 0.0]})
    out = _subgroups(x)
    assert out["age_group"].tolist() == ["<30", "30-49", "50+", "30-49"]
    assert out["bmi_group"].iloc[0] == "<18.5"
    assert out["bmi_group"].iloc[1] == "18.5-24.9"
    assert out["bmi_group"].iloc[2] == ">=30"
    assert pd.isna(out["bmi_group"].iloc[3])


def test_small_subgroup_keeps_denominator_but_suppresses_unstable_metrics():
    result = _metrics(np.array([0, 1, 0, 1]), np.array([0.1, 0.9, 0.2, 0.8]))
    assert result["n"] == 4 and result["events"] == 2
    assert result["eligible_for_metrics"] is False
    assert np.isnan(result["auroc"])


def test_vectorized_paired_bootstrap_has_valid_replicates_and_ordered_intervals():
    y = np.array([0, 1] * 30)
    p_source = np.where(y == 1, 0.8, 0.2)
    p_coral = np.where(y == 1, 0.85, 0.15)
    result = _paired_bootstrap(y, p_source, p_coral, 1000, np.random.default_rng(4))
    assert result["status"] == "ok"
    assert result["valid_replicates"] >= 900
    for metric in ("auroc", "auprc", "brier"):
        assert result[f"{metric}_ci_lower"] <= result[f"{metric}_ci_upper"]
        assert np.isfinite(result[f"{metric}_delta"])
    assert result["auroc_delta"] >= 0


def test_identical_arms_produce_zero_paired_deltas_and_intervals():
    y = np.array([0, 1] * 20)
    p = np.where(y == 1, 0.7, 0.3)
    result = _paired_bootstrap(y, p, p.copy(), 1000, np.random.default_rng(12))
    assert result["status"] == "ok"
    for metric in ("auroc", "auprc", "brier"):
        assert result[f"{metric}_delta"] == pytest.approx(0.0, abs=1e-12)
        assert result[f"{metric}_ci_lower"] == pytest.approx(0.0, abs=1e-12)
        assert result[f"{metric}_ci_upper"] == pytest.approx(0.0, abs=1e-12)


def test_invalid_probabilities_are_rejected():
    with pytest.raises(ValueError, match="finite and in"):
        _metrics(np.array([0, 1]), np.array([0.2, 1.2]))


def test_vectorized_average_precision_matches_sklearn_with_tied_scores():
    labels = np.array([[0, 1, 1, 0, 1, 0], [1, 0, 1, 0, 0, 1]])
    scores = np.array([[0.5, 0.5, 0.5, 0.2, 0.2, 0.1],
                       [0.3, 0.3, 0.7, 0.7, 0.1, 0.1]])
    actual = _average_precision_batch(labels, scores)
    expected = np.array([
        average_precision_score(y, p) for y, p in zip(labels, scores)
    ])
    np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)

def test_paired_bootstrap_can_return_unaggregated_draws_without_changing_default_api():
    y = np.array([0, 1] * 30)
    p_source = np.where(y == 1, 0.8, 0.2)
    p_coral = np.where(y == 1, 0.85, 0.15)
    result, draws = _paired_bootstrap(
        y, p_source, p_coral, 1000, np.random.default_rng(4),
        return_draws=True,
    )
    assert result["status"] == "ok"
    assert len(draws["auroc"]) == result["valid_replicates"]
    assert len(draws["auprc"]) == result["valid_replicates"]
    assert len(draws["brier"]) == result["valid_replicates"]
