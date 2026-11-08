"""Subgroup and paired-bootstrap audit of held-out synthetic-shift predictions.

These are exploratory strata in the historical Pima benchmark, not Nigerian
fairness evidence. Patient-row resampling is paired across source-only/CORAL
predictions within each seed/model/scenario. Small strata are retained in the
denominator table but not given unstable discrimination estimates.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from ml.preprocessing.pipeline import load_pima_benchmark

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "ml/datasets/diabetes_dataset.csv"
PRED = ROOT / "ml/artifacts/experiments/synthetic_shift_predictions.csv"
OUT = ROOT / "ml/artifacts/experiments"
MIN_N = 20
MIN_CLASS = 5

def _subgroups(features: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame(index=features.index)
    age = pd.to_numeric(features["Age"], errors="coerce")
    out["age_group"] = pd.cut(age, bins=[-np.inf, 29, 49, np.inf],
                              labels=["<30", "30-49", "50+"], right=True).astype("object")
    bmi = pd.to_numeric(features["BMI"], errors="coerce").replace(0, np.nan)
    out["bmi_group"] = pd.cut(bmi, bins=[-np.inf, 18.5, 25, 30, np.inf],
                              labels=["<18.5", "18.5-24.9", "25-29.9", ">=30"],
                              right=False).astype("object")
    out.loc[bmi.isna(), "bmi_group"] = np.nan
    return out

def _metrics(y: np.ndarray, p: np.ndarray) -> dict:
    y=np.asarray(y,dtype=int); p=np.asarray(p,dtype=float)
    result={"n":int(len(y)),"events":int(y.sum()),
            "prevalence":float(y.mean()) if len(y) else float("nan")}
    if len(y)<MIN_N or y.sum()<MIN_CLASS or (len(y)-y.sum())<MIN_CLASS:
        result.update({"eligible_for_metrics":False,"auroc":np.nan,
                       "auprc":np.nan,"brier":np.nan})
        return result
    result.update({"eligible_for_metrics":True,
        "auroc":float(roc_auc_score(y,p)),
        "auprc":float(average_precision_score(y,p)),
        "brier":float(brier_score_loss(y,p))})
    return result

def _paired_bootstrap(y, p_source, p_coral, n_bootstrap, rng):
    y=np.asarray(y,dtype=int); ps=np.asarray(p_source,dtype=float); pc=np.asarray(p_coral,dtype=float)
    if len(y)<MIN_N or y.sum()<MIN_CLASS or (len(y)-y.sum())<MIN_CLASS:
        return {"valid_replicates":0,"auroc_delta":np.nan,"auroc_ci_lower":np.nan,
                "auroc_ci_upper":np.nan,"auprc_delta":np.nan,"auprc_ci_lower":np.nan,
                "auprc_ci_upper":np.nan,"brier_delta":np.nan,"brier_ci_lower":np.nan,
                "brier_ci_upper":np.nan,"status":"insufficient subgroup events"}
    values={"auroc":[],"auprc":[],"brier":[]}
    n=len(y)
    for _ in range(n_bootstrap):
        ix=rng.integers(0,n,n); yy=y[ix]
        if yy.sum()<1 or (len(yy)-yy.sum())<1:
            continue
        a,b=ps[ix],pc[ix]
        values["auroc"].append(roc_auc_score(yy,b)-roc_auc_score(yy,a))
        values["auprc"].append(average_precision_score(yy,b)-average_precision_score(yy,a))
        values["brier"].append(brier_score_loss(yy,b)-brier_score_loss(yy,a))
    result={"valid_replicates":len(values["auroc"]),"status":"ok"}
    for metric,arr in values.items():
        if arr:
            result[f"{metric}_delta"]=float(np.mean(arr))
            result[f"{metric}_ci_lower"]=float(np.quantile(arr,.025))
            result[f"{metric}_ci_upper"]=float(np.quantile(arr,.975))
        else:
            result[f"{metric}_delta"]=result[f"{metric}_ci_lower"]=result[f"{metric}_ci_upper"]=np.nan
    return result

def run_audit(n_bootstrap=1000,seed=2026):
    if n_bootstrap<100: raise ValueError("Use at least 100 bootstrap replicates")
    X,y=load_pima_benchmark(str(DATA))
    subgroup=_subgroups(X.reset_index(drop=True))
    predictions=pd.read_csv(PRED)
    required={"seed","source_row_index","model","shift_scenario","adaptation","y_true","probability"}
    missing=required-set(predictions.columns)
    if missing: raise ValueError(f"Prediction file missing columns: {sorted(missing)}")
    predictions["source_row_index"]=predictions["source_row_index"].astype(int)
    predictions=predictions.merge(subgroup,left_on="source_row_index",right_index=True,how="left",validate="many_to_one")
    predictions["overall_group"]="all"
    group_specs=[("overall_group",["all"]),("age_group",["<30","30-49","50+"]),
                 ("bmi_group",["<18.5","18.5-24.9","25-29.9",">=30"])]
    metric_rows=[]
    rng=np.random.default_rng(seed)
    bootstrap_rows=[]
    for group_col,labels in group_specs:
        for label in labels:
            subset=predictions[predictions[group_col]==label]
            for (split,model,scenario),part in subset.groupby(["seed","model","shift_scenario"],sort=True):
                for adaptation,arm in part.groupby("adaptation",sort=True):
                    m=_metrics(arm["y_true"].to_numpy(),arm["probability"].to_numpy())
                    metric_rows.append({"subgroup_type":group_col,"subgroup":label,"seed":int(split),
                        "model":model,"shift_scenario":scenario,"adaptation":adaptation,**m})
                wide=part.pivot(index="source_row_index",columns="adaptation",values=["y_true","probability"])
                if not {"source_only","coral"}.issubset(set(wide["probability"].columns)):
                    continue
                wide=wide.dropna(subset=[("y_true","source_only"),("y_true","coral"),
                                         ("probability","source_only"),("probability","coral")])
                y_source=wide[("y_true","source_only")].to_numpy(dtype=int)
                y_coral=wide[("y_true","coral")].to_numpy(dtype=int)
                if not np.array_equal(y_source,y_coral):
                    raise ValueError("Paired predictions do not share identical held-out labels")
                result=_paired_bootstrap(y_source,wide[("probability","source_only")].to_numpy(),
                    wide[("probability","coral")].to_numpy(),n_bootstrap,rng)
                bootstrap_rows.append({"subgroup_type":group_col,"subgroup":label,"seed":int(split),
                    "model":model,"shift_scenario":scenario,"n":len(y_source),
                    "events":int(y_source.sum()),**result})
    OUT.mkdir(parents=True,exist_ok=True)
    metrics_path=OUT/"subgroup_metrics.csv"
    bootstrap_path=OUT/"subgroup_paired_bootstrap.csv"
    pd.DataFrame(metric_rows).to_csv(metrics_path,index=False)
    pd.DataFrame(bootstrap_rows).to_csv(bootstrap_path,index=False)
    if not metric_rows or not bootstrap_rows:
        raise RuntimeError("Subgroup audit produced no result rows")
    print({"subgroup_metric_rows":len(metric_rows),"paired_bootstrap_rows":len(bootstrap_rows),
           "bootstrap_requested":n_bootstrap,"metrics_output":str(metrics_path),
           "bootstrap_output":str(bootstrap_path),
           "minimum_stratum_n":MIN_N,"minimum_events_per_class":MIN_CLASS,
           "interpretation":"Exploratory Pima strata only; not Nigerian external validation or fairness certification."})
    return pd.DataFrame(metric_rows),pd.DataFrame(bootstrap_rows)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--bootstrap",type=int,default=1000)
    parser.add_argument("--seed",type=int,default=2026)
    args=parser.parse_args()
    run_audit(args.bootstrap,args.seed)
