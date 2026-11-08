"""Controlled synthetic-shift study; never interpret as external hospital validation.

Protocol:
* stratified source/held-out split, repeated over fixed seeds;
* target shift changes held-out covariates only, without consulting target labels;
* source-only vs CORAL adaptation; CORAL sees target covariates, never target labels;
* all preprocessing is fitted on source training data only;
* target labels are used only after predictions for evaluation.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier,HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from ml.domain_adaptation.coral import CORALAdapter
from ml.evaluation.metrics import full_evaluation
from ml.preprocessing.pipeline import FEATURE_COLUMNS,build_preprocessing_pipeline,load_pima_benchmark
DATA=ROOT/"ml/datasets/diabetes_dataset.csv"; OUT=ROOT/"ml/artifacts/experiments"

def make_shift(X,seed,missing_rate=0.0):
    """Create deterministic covariate stress test; not synthetic patient data."""
    shifted=X.copy().astype(float); rng=np.random.default_rng(seed)
    shifted[:,1]=shifted[:,1]*1.15+5.0 # Glucose location/scale shift
    shifted[:,5]=shifted[:,5]*1.10+1.5 # BMI location/scale shift
    shifted[:,7]=shifted[:,7]*1.05+2.0 # Age location/scale shift
    if missing_rate:
        mask=rng.random(shifted.shape)<missing_rate
        shifted[mask]=np.nan
    return shifted

def _model(name,seed):
    if name=="logistic_regression": return LogisticRegression(max_iter=1500,class_weight="balanced",random_state=seed)
    if name=="random_forest": return RandomForestClassifier(n_estimators=250,max_depth=6,min_samples_leaf=3,class_weight="balanced",n_jobs=-1,random_state=seed)
    if name=="hist_gradient_boosting": return HistGradientBoostingClassifier(max_iter=150,learning_rate=.06,max_leaf_nodes=15,l2_regularization=1.0,random_state=seed)
    raise ValueError(f"Unknown model: {name}")

def _calibrated(estimator,seed):
    # Calibration folds are source-only; no target labels are accessed.
    return CalibratedClassifierCV(estimator=clone(estimator),method="sigmoid",cv=3)

def _json_safe(value):
    if isinstance(value,dict): return {str(k):_json_safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [_json_safe(v) for v in value]
    if isinstance(value,(np.integer,)): return int(value)
    if isinstance(value,(np.floating,float)):
        return float(value) if np.isfinite(value) else None
    return value

def run_study(repeats=5,models=("logistic_regression","random_forest","hist_gradient_boosting"),missing_rate=0.1):
    X,y=load_pima_benchmark(str(DATA)); X=X[FEATURE_COLUMNS].to_numpy(dtype=float); y=y.to_numpy(dtype=int)
    rows=[]
    for seed in range(42,42+repeats):
        ix=np.arange(len(y)); train_ix,test_ix=train_test_split(ix,test_size=.25,stratify=y,random_state=seed)
        raw_train,raw_test=X[train_ix],X[test_ix]; y_train,y_test=y[train_ix],y[test_ix]
        shifted=make_shift(raw_test,seed,missing_rate=missing_rate)
        for model_name in models:
            preprocess=build_preprocessing_pipeline()
            Xs=preprocess.fit_transform(pd.DataFrame(raw_train,columns=FEATURE_COLUMNS))
            Xt=preprocess.transform(pd.DataFrame(shifted,columns=FEATURE_COLUMNS))
            for scenario in ("source_only","coral"):
                estimator=_calibrated(_model(model_name,seed),seed)
                if scenario=="coral":
                    adapter=CORALAdapter().fit(Xs,Xt)
                    train_features=adapter.transform(Xs)
                else: train_features=Xs
                estimator.fit(train_features,y_train)
                prob=estimator.predict_proba(Xt)[:,1]
                uncertainty=-(np.clip(prob,1e-8,1-1e-8)*np.log(np.clip(prob,1e-8,1-1e-8))+(1-np.clip(prob,1e-8,1-1e-8))*np.log(1-np.clip(prob,1e-8,1-1e-8)))
                metrics=full_evaluation(y_test,prob,uncertainty,coverage=.8)
                rows.append({"seed":seed,"model":model_name,"scenario":scenario,"n_train":len(train_ix),"n_test":len(test_ix),"synthetic_missing_rate":missing_rate,**metrics})
    frame=pd.DataFrame(rows); OUT.mkdir(parents=True,exist_ok=True)
    frame.to_csv(OUT/"synthetic_shift_runs.csv",index=False)
    summary=frame.groupby(["model","scenario"]).agg({c:["mean","std"] for c in ["auroc","auprc","brier","ece","aurc","selective_auroc","selective_brier"]}).round(5)
    summary.to_csv(OUT/"synthetic_shift_summary.csv")
    artifact={"study":"controlled_synthetic_covariate_and_missingness_shift","data_source":"public Pima benchmark only","external_validation":False,"target_labels_used_for_adaptation":False,"target_covariates_used_for_adaptation":"CORAL scenario only","repeats":repeats,"models":list(models),"missing_rate":missing_rate,"seed_range":[42,41+repeats],"results":rows,"summary_csv":"synthetic_shift_summary.csv","raw_runs_csv":"synthetic_shift_runs.csv"}
    (OUT/"synthetic_shift_study.json").write_text(json.dumps(_json_safe(artifact),indent=2,allow_nan=False))
    return artifact

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--repeats",type=int,default=5);parser.add_argument("--missing-rate",type=float,default=.1);args=parser.parse_args()
    if args.repeats<2: parser.error("--repeats must be >=2")
    if not 0<=args.missing_rate<.8: parser.error("--missing-rate must be in [0, .8)")
    result=run_study(args.repeats,missing_rate=args.missing_rate)
    print(json.dumps({"status":"complete","runs":len(result["results"]),"external_validation":False,"output":str(OUT)},indent=2))
