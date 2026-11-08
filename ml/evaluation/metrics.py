"""Validated discrimination, calibration and selective-prediction metrics.

All metrics operate on held-out predictions. They do not imply clinical validity.
"""
from __future__ import annotations
import numpy as np
from sklearn.metrics import (average_precision_score,brier_score_loss,confusion_matrix,
    f1_score,precision_score,recall_score,roc_auc_score)

def _inputs(y_true,y_prob):
    y=np.asarray(y_true).reshape(-1); p=np.asarray(y_prob,dtype=float).reshape(-1)
    if y.size==0 or y.size!=p.size: raise ValueError("y_true and y_prob must have equal non-zero length")
    if not np.isin(y,[0,1]).all(): raise ValueError("y_true must contain only binary labels 0 and 1")
    if not np.isfinite(p).all() or ((p<0)|(p>1)).any(): raise ValueError("y_prob must be finite and within [0, 1]")
    return y.astype(int),p

def compute_discrimination_metrics(y_true,y_prob,threshold=0.5):
    y,p=_inputs(y_true,y_prob)
    if not 0<=threshold<=1: raise ValueError("threshold must be within [0, 1]")
    pred=(p>=threshold).astype(int); tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return {"auroc":float(roc_auc_score(y,p)) if np.unique(y).size==2 else float("nan"),
        "auprc":float(average_precision_score(y,p)) if (y==1).any() else float("nan"),
        "precision":float(precision_score(y,pred,zero_division=0)),
        "recall":float(recall_score(y,pred,zero_division=0)),
        "f1":float(f1_score(y,pred,zero_division=0)),
        "sensitivity":float(tp/(tp+fn)) if tp+fn else 0.0,
        "specificity":float(tn/(tn+fp)) if tn+fp else 0.0}

def expected_calibration_error(y_true,y_prob,n_bins=10):
    y,p=_inputs(y_true,y_prob)
    if not isinstance(n_bins,int) or n_bins<1: raise ValueError("n_bins must be a positive integer")
    edges=np.linspace(0,1,n_bins+1); total=0.0
    for i in range(n_bins):
        mask=(p>=edges[i]) & ((p<edges[i+1]) if i<n_bins-1 else (p<=edges[i+1]))
        if mask.any(): total+=float(mask.mean()*abs(y[mask].mean()-p[mask].mean()))
    return float(total)

def compute_calibration_metrics(y_true,y_prob):
    y,p=_inputs(y_true,y_prob)
    return {"brier":float(brier_score_loss(y,p)),"ece":expected_calibration_error(y,p)}

def risk_coverage_curve(y_true,y_prob,uncertainty):
    y,p=_inputs(y_true,y_prob); u=np.asarray(uncertainty,dtype=float).reshape(-1)
    if u.size!=y.size or not np.isfinite(u).all(): raise ValueError("uncertainty must be finite and match y_true")
    order=np.argsort(u,kind="stable"); errors=((p>=0.5).astype(int)!=y).astype(float)[order]
    coverage=np.arange(1,len(y)+1,dtype=float)/len(y); risk=np.cumsum(errors)/np.arange(1,len(y)+1)
    aurc=float(np.sum((risk[1:]+risk[:-1])*0.5*np.diff(coverage))) if len(y)>1 else float(risk[0])
    return {"coverage":coverage.tolist(),"risk":risk.tolist(),"aurc":aurc}

def selective_prediction_metrics(y_true,y_prob,uncertainty,coverage=0.8):
    y,p=_inputs(y_true,y_prob); u=np.asarray(uncertainty,dtype=float).reshape(-1)
    if u.size!=y.size or not np.isfinite(u).all(): raise ValueError("uncertainty must be finite and match y_true")
    if not 0<coverage<=1: raise ValueError("coverage must be in (0, 1]")
    keep=max(1,int(np.ceil(coverage*len(y)))); idx=np.argsort(u,kind="stable")[:keep]
    disc=compute_discrimination_metrics(y[idx],p[idx]); cal=compute_calibration_metrics(y[idx],p[idx])
    return {"coverage":float(keep/len(y)),"selective_auroc":disc["auroc"],
        "selective_auprc":disc["auprc"],"selective_f1":disc["f1"],
        "selective_brier":cal["brier"],"selective_ece":cal["ece"]}

def full_evaluation(y_true,y_prob,uncertainty=None,coverage=0.8):
    result={**compute_discrimination_metrics(y_true,y_prob),**compute_calibration_metrics(y_true,y_prob)}
    if uncertainty is not None:
        result.update(selective_prediction_metrics(y_true,y_prob,uncertainty,coverage))
        result["aurc"]=risk_coverage_curve(y_true,y_prob,uncertainty)["aurc"]
    return result

def bootstrap_metric_intervals(y_true,y_prob,n_bootstrap=1000,random_state=42):
    y,p=_inputs(y_true,y_prob)
    if n_bootstrap<100: raise ValueError("Use at least 100 bootstrap replicates")
    rng=np.random.default_rng(random_state); vals={"auroc":[],"auprc":[],"brier":[]}
    for _ in range(n_bootstrap):
        ix=rng.integers(0,len(y),len(y)); ys,ps=y[ix],p[ix]
        if np.unique(ys).size<2: continue
        vals["auroc"].append(roc_auc_score(ys,ps)); vals["auprc"].append(average_precision_score(ys,ps)); vals["brier"].append(brier_score_loss(ys,ps))
    return {k:{"lower_95":float(np.quantile(v,.025)),"upper_95":float(np.quantile(v,.975)),"valid_replicates":len(v)}
        for k,v in vals.items() if v}
