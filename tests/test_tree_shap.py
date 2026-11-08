import numpy as np
import pytest
shap=pytest.importorskip("shap")
from sklearn.ensemble import RandomForestClassifier
from ml.explainability.tree_shap import tree_shap_values,ranked_features

def test_tree_shap_returns_finite_binary_attributions():
    rng=np.random.default_rng(7);x=rng.normal(size=(120,4));y=(x[:,0]+x[:,1]>.1).astype(int)
    model=RandomForestClassifier(n_estimators=30,max_depth=3,random_state=3).fit(x,y)
    values=tree_shap_values(model,x[:40],x[40:45],["a","b","c","d"])
    assert values.shape==(5,4) and np.isfinite(values).all()
    rankings=ranked_features(values,["a","b","c","d"])
    assert len(rankings)==5 and len(rankings[0])==4

def test_tree_shap_rejects_nan_inputs():
    model=RandomForestClassifier(n_estimators=5,random_state=1).fit([[0,1],[1,0],[0,0],[1,1]],[0,1,0,1])
    with pytest.raises(ValueError):tree_shap_values(model,[[0,np.nan]],[[1,0]],["a","b"])
