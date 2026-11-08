from __future__ import annotations
import logging,sys
from pathlib import Path
from typing import Any
import joblib,numpy as np,pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
ROOT=Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from ml.preprocessing.pipeline import FEATURE_COLUMNS,build_preprocessing_pipeline,load_pima_benchmark
from ml.uncertainty.selective import entropy_uncertainty
log=logging.getLogger(__name__)
DATA=ROOT/"ml/datasets/diabetes_dataset.csv"
DATA_PATH=DATA
MODEL_DIR=ROOT/"ml/artifacts/models"
MODEL_DIR.mkdir(parents=True,exist_ok=True)
MODEL_NAMES=("logistic_regression","random_forest","xgboost")
def build_classifier(model_name:str,seed:int=42):
    if model_name=="logistic_regression":
        return LogisticRegression(max_iter=1500,class_weight="balanced",random_state=seed)
    if model_name=="random_forest":
        return RandomForestClassifier(n_estimators=250,max_depth=6,min_samples_leaf=3,class_weight="balanced",n_jobs=-1,random_state=seed)
    if model_name=="xgboost":
        return XGBClassifier(n_estimators=180,max_depth=3,learning_rate=.04,subsample=.8,colsample_bytree=.8,reg_lambda=2,random_state=seed,eval_metric="logloss",verbosity=0)
    raise ValueError(f"Unsupported model_name. Choose one of: {', '.join(MODEL_NAMES)}")
def load_model(model_name:str="logistic_regression"):
    classifier=build_classifier(model_name)
    model_path=MODEL_DIR/f"{model_name}_v0_3_0.joblib"
    if model_path.exists(): return joblib.load(model_path)
    X,y=load_pima_benchmark(str(DATA))
    model=Pipeline([("preprocess",build_preprocessing_pipeline()),("clf",classifier)])
    model.fit(X,y);joblib.dump(model,model_path)
    return model
def risk_category(probability:float)->str:
    # No clinical cut-points have been validated for this non-Nigerian benchmark.
    return "not_clinically_calibrated"
def compute_shap_contributions(model,features):
    X,_=load_pima_benchmark(str(DATA))
    preprocess=model.named_steps["preprocess"];estimator=model.named_steps["clf"]
    background=np.asarray(preprocess.transform(X.sample(min(100,len(X)),random_state=42)))
    row=np.asarray(preprocess.transform(pd.DataFrame([features])[FEATURE_COLUMNS]))
    try:
        if hasattr(estimator,"feature_importances_"):
            from ml.explainability.tree_shap import tree_shap_values
            values=tree_shap_values(estimator,background,row,FEATURE_COLUMNS)[0]
            method="TreeSHAP"
        else:
            import shap
            explanation=shap.Explainer(estimator,shap.maskers.Independent(background,max_samples=min(100,len(background))))(row)
            values=np.asarray(explanation.values)
            if values.ndim==3: values=values[...,-1]
            values=values.reshape(-1)
            method="SHAP"
        if len(values)!=len(FEATURE_COLUMNS): raise ValueError("Unexpected SHAP dimensions")
    except Exception as exc:
        if not hasattr(estimator,"coef_"):
            log.exception("TreeSHAP unavailable for selected model")
            raise RuntimeError("A faithful local SHAP explanation could not be computed for this tree model.") from exc
        log.exception("SHAP failed; using explicitly labelled coefficient fallback: %s",exc)
        transformed=np.asarray(preprocess.transform(pd.DataFrame([features])[FEATURE_COLUMNS])).ravel()
        values=estimator.coef_.ravel()*transformed
        method="coefficient_fallback_not_SHAP"
    return [{"feature":name,"value":float(features[name]),"contribution":float(value),
        "direction":"increases_risk" if value>0 else "decreases_risk","method":method}
        for name,value in sorted(zip(FEATURE_COLUMNS,values),key=lambda pair:abs(pair[1]),reverse=True)]
def predict(features:dict[str,float],return_explanation=True,return_uncertainty=True,uncertainty_threshold=.5,model_name="logistic_regression")->dict[str,Any]:
    model=load_model(model_name)
    probability=float(model.predict_proba(pd.DataFrame([features])[FEATURE_COLUMNS])[0,1])
    uncertainty=float(entropy_uncertainty(np.array([probability]))[0]) if return_uncertainty else None
    abstain=bool(uncertainty is not None and uncertainty>uncertainty_threshold)
    return {"model_version":f"{model_name}-0.3.0","data_source_note":"Public Pima Indians Diabetes dataset (methodological benchmark only), not Nigerian hospital data.",
        "probability":probability,"risk_category":risk_category(probability),"prediction":-1 if abstain else int(probability>=.5),
        "abstain":abstain,"uncertainty":uncertainty,"uncertainty_measure":"binary_entropy_nats" if uncertainty is not None else None,
        "confidence_statement":"Experimental benchmark output only; not calibrated or intended for clinical decisions. Entropy-based abstention is not a clinical safety guarantee.",
        "feature_contributions":compute_shap_contributions(model,features) if return_explanation else None,
        "limitations":["Pima public benchmark only; no Nigerian external validation.","Entropy is not a calibrated clinical confidence interval.","SHAP is model behaviour, not causality."]}
