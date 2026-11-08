"""Consistent TreeSHAP interface for binary tree classifiers.

Attributions explain model outputs, not causal effects. With probability output,
contributions are expressed on the probability scale.
"""
from __future__ import annotations
import numpy as np

def tree_shap_values(estimator,background,samples,feature_names=None):
    import shap
    bg=np.asarray(background,dtype=float); x=np.asarray(samples,dtype=float)
    if bg.ndim!=2 or x.ndim!=2 or bg.shape[1]!=x.shape[1]: raise ValueError("background and samples must be 2D with matching features")
    if not np.isfinite(bg).all() or not np.isfinite(x).all(): raise ValueError("SHAP inputs must be finite; preprocess missing values first")
    explainer=shap.TreeExplainer(estimator,data=bg,feature_perturbation="interventional",model_output="probability")
    raw=explainer.shap_values(x)
    if isinstance(raw,list):
        if len(raw)<2: raise ValueError("Expected binary classifier SHAP outputs")
        raw=raw[1]
    values=np.asarray(raw,dtype=float)
    if values.ndim==3:
        if values.shape[-1]==2: values=values[...,1]
        elif values.shape[0]==2: values=values[1]
        else: raise ValueError(f"Unsupported SHAP output shape: {values.shape}")
    if values.ndim==1: values=values.reshape(1,-1)
    if values.shape!=(x.shape[0],x.shape[1]): raise ValueError(f"Unexpected SHAP dimensions {values.shape}; expected {(x.shape[0],x.shape[1])}")
    if not np.isfinite(values).all(): raise ValueError("SHAP returned non-finite attributions")
    return values

def ranked_features(shap_values,feature_names):
    values=np.asarray(shap_values,dtype=float)
    if values.ndim!=2 or values.shape[1]!=len(feature_names): raise ValueError("SHAP values and feature names do not align")
    return [list(np.asarray(feature_names)[np.argsort(-np.abs(row),kind="stable")]) for row in values]
