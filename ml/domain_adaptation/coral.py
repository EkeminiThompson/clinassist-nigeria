"""CORAL: unsupervised second-order alignment of source to target covariates.

Target labels must never be passed to fit(). Fit uses target features only.
"""
from __future__ import annotations
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin

def _matrix(x,name):
    a=np.asarray(x,dtype=float)
    if a.ndim!=2 or a.shape[0]<2 or a.shape[1]<1: raise ValueError(f"{name} must be a 2D matrix with at least two rows and one feature")
    if not np.isfinite(a).all(): raise ValueError(f"{name} must contain finite values; impute missing data first")
    return a

def _sqrt_cov(cov,epsilon,inverse=False):
    values,vectors=np.linalg.eigh(cov)
    values=np.maximum(values,epsilon)
    powers=1.0/np.sqrt(values) if inverse else np.sqrt(values)
    return (vectors*powers)@vectors.T

def coral_transform(source,target,epsilon=1e-5):
    source=_matrix(source,"source"); target=_matrix(target,"target")
    if source.shape[1]!=target.shape[1]: raise ValueError("source and target must have the same feature count")
    if epsilon<=0: raise ValueError("epsilon must be positive")
    cs=np.atleast_2d(np.cov(source,rowvar=False))+epsilon*np.eye(source.shape[1])
    ct=np.atleast_2d(np.cov(target,rowvar=False))+epsilon*np.eye(target.shape[1])
    mapping=_sqrt_cov(cs,epsilon,inverse=True)@_sqrt_cov(ct,epsilon)
    return (source-source.mean(axis=0))@mapping+target.mean(axis=0)

class CORALAdapter(BaseEstimator,TransformerMixin):
    def __init__(self,epsilon=1e-5):
        self.epsilon=epsilon
    def fit(self,source_X,target_X):
        source=_matrix(source_X,"source_X"); target=_matrix(target_X,"target_X")
        if source.shape[1]!=target.shape[1]: raise ValueError("source_X and target_X feature counts differ")
        if self.epsilon<=0: raise ValueError("epsilon must be positive")
        cs=np.atleast_2d(np.cov(source,rowvar=False))+self.epsilon*np.eye(source.shape[1])
        ct=np.atleast_2d(np.cov(target,rowvar=False))+self.epsilon*np.eye(target.shape[1])
        self.source_mean_=source.mean(axis=0); self.target_mean_=target.mean(axis=0)
        self.mapping_=_sqrt_cov(cs,self.epsilon,inverse=True)@_sqrt_cov(ct,self.epsilon)
        self.n_features_in_=source.shape[1]
        return self
    def transform(self,X):
        if not hasattr(self,"mapping_"): raise RuntimeError("CORALAdapter must be fitted before transform")
        a=_matrix(X,"X")
        if a.shape[1]!=self.n_features_in_: raise ValueError("X feature count differs from fitted data")
        return (a-self.source_mean_)@self.mapping_+self.target_mean_
