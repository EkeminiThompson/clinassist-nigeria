import numpy as np
import pytest
from ml.experiments.run_shift_study import make_shift,_json_safe,SCENARIOS

def test_synthetic_shift_is_deterministic_and_preserves_rows():
    x=np.ones((12,8),dtype=float)
    a=make_shift(x,seed=12,missing_rate=.05)
    b=make_shift(x,seed=12,missing_rate=.05)
    assert a.shape==x.shape and np.array_equal(a,b,equal_nan=True)

def test_reference_scenario_does_not_perturb_features():
    x=np.arange(80,dtype=float).reshape(10,8)
    assert np.array_equal(make_shift(x,seed=1,**SCENARIOS["reference"]),x)

def test_mar_like_missingness_targets_insulin_and_skin_thickness():
    x=np.ones((1000,8),dtype=float);x[:,1]=np.linspace(60,190,1000)
    z=make_shift(x,seed=3,missing_rate=.2,severity=0,mechanism="mar")
    assert np.isnan(z[:,3]).any() and np.isnan(z[:,4]).any()
    assert np.isfinite(z[:,0]).all() and np.isfinite(z[:,7]).all()

def test_shift_rejects_invalid_missingness_mechanism():
    with pytest.raises(ValueError):make_shift(np.ones((5,8)),seed=1,missing_rate=.1,mechanism="unknown")

def test_json_safe_replaces_non_finite_metrics():
    assert _json_safe({"score":float("nan")})=={"score":None}
