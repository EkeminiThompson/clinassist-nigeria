import numpy as np
import pytest
from ml.evaluation.metrics import (compute_discrimination_metrics,expected_calibration_error,
    full_evaluation,selective_prediction_metrics,risk_coverage_curve,bootstrap_metric_intervals)

def test_ece_includes_probability_one():
    assert expected_calibration_error([1,0],[1.0,0.0])==0.0

def test_discrimination_handles_single_class_without_crashing():
    assert np.isnan(compute_discrimination_metrics([1,1],[.8,.9])["auroc"])

def test_invalid_probabilities_rejected():
    with pytest.raises(ValueError): compute_discrimination_metrics([0,1],[.2,1.2])

def test_selective_coverage_uses_ceiling_and_validates():
    out=selective_prediction_metrics([0,1,0],[.1,.9,.4],[.1,.2,.3],coverage=.5)
    assert out["coverage"]==pytest.approx(2/3)
    with pytest.raises(ValueError): selective_prediction_metrics([0],[.1],[.2],coverage=0)

def test_risk_coverage_curve_is_monotone_in_coverage():
    out=risk_coverage_curve([0,1,0],[.1,.8,.7],[.1,.2,.3])
    assert out["coverage"]==sorted(out["coverage"])
    assert 0<=out["aurc"]<=1

def test_bootstrap_intervals_reproducible():
    a=bootstrap_metric_intervals([0,1,0,1],[.1,.8,.3,.7],n_bootstrap=100,random_state=9)
    b=bootstrap_metric_intervals([0,1,0,1],[.1,.8,.3,.7],n_bootstrap=100,random_state=9)
    assert a==b
