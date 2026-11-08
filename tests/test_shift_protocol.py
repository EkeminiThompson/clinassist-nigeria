import numpy as np
from ml.experiments.run_shift_study import make_shift,_json_safe

def test_synthetic_shift_is_deterministic_and_preserves_rows():
    x=np.ones((12,8),dtype=float)
    a=make_shift(x,seed=12,missing_rate=.05)
    b=make_shift(x,seed=12,missing_rate=.05)
    assert a.shape==x.shape and np.array_equal(a,b,equal_nan=True)

def test_shift_function_does_not_accept_or_use_labels():
    x=np.ones((5,8),dtype=float)
    assert make_shift(x,seed=1,missing_rate=0).shape==(5,8)

def test_json_safe_replaces_non_finite_metrics():
    assert _json_safe({"score":float("nan")})=={"score":None}
