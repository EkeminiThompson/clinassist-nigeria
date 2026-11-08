import numpy as np
import pytest
from ml.domain_adaptation.coral import CORALAdapter,coral_transform

def test_coral_preserves_dimensions_and_finite_values():
    rng=np.random.default_rng(4);s=rng.normal(size=(80,4));t=rng.normal(1,2,size=(60,4))
    z=coral_transform(s,t)
    assert z.shape==s.shape and np.isfinite(z).all()

def test_adapter_requires_fit():
    with pytest.raises(RuntimeError): CORALAdapter().transform(np.ones((4,2)))

def test_adapter_rejects_feature_mismatch():
    with pytest.raises(ValueError): CORALAdapter().fit(np.ones((10,2)),np.ones((10,3)))

def test_coral_rejects_nan_until_imputed():
    with pytest.raises(ValueError): coral_transform([[1,2],[2,np.nan]],[[1,2],[2,3]])

def test_single_feature_supported():
    s=np.arange(10,dtype=float).reshape(-1,1);t=(s*2)+3
    z=coral_transform(s,t)
    assert z.shape==s.shape and np.isfinite(z).all()
