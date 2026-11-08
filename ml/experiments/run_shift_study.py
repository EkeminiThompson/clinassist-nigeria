"""Factorial controlled synthetic-shift study; not external hospital validation.

Source-only vs CORAL is compared across target covariate, MCAR-like and MAR-like
missingness scenarios. Target covariates may be used by CORAL; target labels are
used only after prediction for evaluation.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier,HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from ml.domain_adaptation.coral import CORALAdapter
from ml.evaluation.metrics import full_evaluation
from ml.preprocessing.pipeline import FEATURE_COLUMNS,build_preprocessing_pipeline,load_pima_benchmark
DATA=ROOT/"ml/datasets/diabetes_dataset.csv"
OUT=ROOT/"ml/artifacts/experiments"
SCENARIOS={
    "reference":{"severity":0.0,"missing_rate":0.0,"mechanism":"none"},
    "covariate_mild":{"severity":0.5,"missing_rate":0.0,"mechanism":"none"},
    "covariate_severe":{"severity":1.5,"missing_rate":0.0,"mechanism":"none"},
    "mcar_10":{"severity":0.0,"missing_rate":0.10,"mechanism":"mcar"},
    "mar_like_10":{"severity":0.0,"missing_rate":0.10,"mechanism":"mar"},
    "combined_mild":{"severity":0.5,"missing_rate":0.10,"mechanism":"mcar"},
    "combined_severe":{"severity":1.5,"missing_rate":0.20,"mechanism":"mar"},
}
def make_shift(X,seed,missing_rate=0.0,severity=1.0,mechanism="mcar"):
    """Perturb covariates only; MCAR masks all cells, MAR-like masks depend on glucose."""
    shifted=np.asarray(X,dtype=float).copy()
    rng=np.random.default_rng(seed)
    if severity:
        shifted[:,1]=shifted[:,1]*(1+.15*severity)+5*severity
        shifted[:,5]=shifted[:,5]*(1+.10*severity)+1.5*severity
        shifted[:,7]=shifted[:,7]*(1+.05*severity)+2*severity
    if missing_rate:
        if not 0<missing_rate<.8:
            raise ValueError("missing_rate must be in [0, .8)")
        if mechanism=="mcar":
            shifted[rng.random(shifted.shape)<missing_rate]=np.nan
        elif mechanism=="mar":
            glucose_z=(shifted[:,1]-np.nanmean(shifted[:,1]))/(np.nanstd(shifted[:,1])+1e-8)
            row_probability=np.clip(2*missing_rate/(1+np.exp(-glucose_z)),0,1)
            mask=np.zeros(shifted.shape,dtype=bool)
            for column in (3,4):
                mask[:,column]=rng.random(len(shifted))<row_probability
            shifted[mask]=np.nan
        else:
            raise ValueError("mechanism must be 'mcar' or 'mar' when missing_rate > 0")
    return shifted
def _model(name,seed):
    if name=="logistic_regression":
        return LogisticRegression(max_iter=1500,class_weight="balanced",random_state=seed)
    if name=="random_forest":
        return RandomForestClassifier(n_estimators=250,max_depth=6,min_samples_leaf=3,class_weight="balanced",n_jobs=-1,random_state=seed)
    if name=="hist_gradient_boosting":
        return HistGradientBoostingClassifier(max_iter=150,learning_rate=.06,max_leaf_nodes=15,l2_regularization=1.0,random_state=seed)
    raise ValueError(f"Unknown model: {name}")
def _calibrated(estimator):
    return CalibratedClassifierCV(estimator=clone(estimator),method="sigmoid",cv=3)
def _json_safe(value):
    if isinstance(value,dict):
        return {str(k):_json_safe(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value,(np.integer,)):
        return int(value)
    if isinstance(value,(np.floating,float)):
        return float(value) if np.isfinite(value) else None
    return value
def run_study(repeats=5,models=("logistic_regression","random_forest","hist_gradient_boosting"),scenarios=None):
    if repeats<2:
        raise ValueError("Use at least two repeated splits")
    scenarios=scenarios or SCENARIOS
    X,y=load_pima_benchmark(str(DATA))
    X=X[FEATURE_COLUMNS].to_numpy(dtype=float)
    y=y.to_numpy(dtype=int)
    rows=[]
    prediction_rows=[]
    for seed in range(42,42+repeats):
        indices=np.arange(len(y))
        train_indices,test_indices=train_test_split(indices,test_size=.25,stratify=y,random_state=seed)
        raw_train,raw_test=X[train_indices],X[test_indices]
        y_train,y_test=y[train_indices],y[test_indices]
        preprocess=build_preprocessing_pipeline()
        source_train=preprocess.fit_transform(pd.DataFrame(raw_train,columns=FEATURE_COLUMNS))
        for scenario_index,(shift_name,config) in enumerate(scenarios.items()):
            shifted=make_shift(raw_test,seed=seed+1000*scenario_index,**config)
            target_test=preprocess.transform(pd.DataFrame(shifted,columns=FEATURE_COLUMNS))
            for model_name in models:
                for adaptation in ("source_only","coral"):
                    estimator=_calibrated(_model(model_name,seed))
                    if adaptation=="coral":
                        adapter=CORALAdapter().fit(source_train,target_test)
                        train_features=adapter.transform(source_train)
                    else:
                        train_features=source_train
                    estimator.fit(train_features,y_train)
                    probability=estimator.predict_proba(target_test)[:,1]
                    clipped=np.clip(probability,1e-8,1-1e-8)
                    uncertainty=-(clipped*np.log(clipped)+(1-clipped)*np.log(1-clipped))
                    metrics=full_evaluation(y_test,probability,uncertainty,coverage=.8)
                    rows.append({"seed":seed,"model":model_name,"shift_scenario":shift_name,
                        "adaptation":adaptation,"n_train":len(train_indices),"n_test":len(test_indices),
                        **config,**metrics})
                    for local_index,source_row_index in enumerate(test_indices):
                        prediction_rows.append({"seed":seed,"source_row_index":int(source_row_index),
                            "model":model_name,"shift_scenario":shift_name,"adaptation":adaptation,
                            "y_true":int(y_test[local_index]),"probability":float(probability[local_index]),
                            "uncertainty":float(uncertainty[local_index])})
    frame=pd.DataFrame(rows)
    OUT.mkdir(parents=True,exist_ok=True)
    frame.to_csv(OUT/"synthetic_shift_runs.csv",index=False)
    pd.DataFrame(prediction_rows).to_csv(OUT/"synthetic_shift_predictions.csv",index=False)
    metric_names=["auroc","auprc","brier","ece","calibration_intercept_in_large","calibration_intercept","calibration_slope","aurc","selective_auroc","selective_brier"]
    summary=frame.groupby(["model","shift_scenario","adaptation"])[metric_names].agg(["mean","std"]).round(5)
    summary.to_csv(OUT/"synthetic_shift_summary.csv")
    paired=frame.pivot_table(index=["seed","model","shift_scenario"],columns="adaptation",values=metric_names)
    deltas=[]
    for metric in metric_names:
        delta=paired[(metric,"coral")]-paired[(metric,"source_only")]
        for (seed,model_name,shift_name),value in delta.items():
            deltas.append({"seed":seed,"model":model_name,"shift_scenario":shift_name,
                "metric":metric,"coral_minus_source_only":float(value)})
    pd.DataFrame(deltas).to_csv(OUT/"synthetic_shift_paired_differences.csv",index=False)
    artifact={"study":"factorial_controlled_synthetic_covariate_and_missingness_shift",
        "data_source":"public Pima benchmark only","external_validation":False,
        "target_labels_used_for_adaptation":False,"target_covariates_used_for_adaptation":"CORAL scenario only",
        "repeats":repeats,"models":list(models),"scenario_definitions":scenarios,
        "seed_range":[42,41+repeats],"results":rows,
        "summary_csv":"synthetic_shift_summary.csv","raw_runs_csv":"synthetic_shift_runs.csv",
        "predictions_csv":"synthetic_shift_predictions.csv",
        "paired_differences_csv":"synthetic_shift_paired_differences.csv",
        "interpretation_note":"Mean and standard deviation across repeated random splits describe split variability, not independent external validation or patient-level confidence intervals."}
    (OUT/"synthetic_shift_study.json").write_text(json.dumps(_json_safe(artifact),indent=2,allow_nan=False))
    return artifact
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--repeats",type=int,default=5)
    args=parser.parse_args()
    if args.repeats<2:
        parser.error("--repeats must be >=2")
    result=run_study(repeats=args.repeats)
    print(json.dumps({"status":"complete","runs":len(result["results"]),
        "scenarios":list(SCENARIOS),"external_validation":False,"output":str(OUT)},indent=2))
