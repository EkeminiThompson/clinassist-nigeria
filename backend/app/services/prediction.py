from __future__ import annotations
import logging,sys
from pathlib import Path
from typing import Any
import joblib,numpy as np,pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
ROOT=Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from ml.preprocessing.pipeline import FEATURE_COLUMNS,build_preprocessing_pipeline,load_pima_benchmark
from ml.uncertainty.selective import entropy_uncertainty
log=logging.getLogger(__name__);DATA=ROOT/'ml/datasets/diabetes_dataset.csv';MODEL_DIR=ROOT/'ml/artifacts/models';MODEL_DIR.mkdir(parents=True,exist_ok=True);MODEL=MODEL_DIR/'baseline_logistic.joblib'
DATA_PATH=DATA
def load_model():
 if MODEL.exists():return joblib.load(MODEL)
 X,y=load_pima_benchmark(str(DATA));m=Pipeline([('preprocess',build_preprocessing_pipeline()),('clf',LogisticRegression(max_iter=1000,class_weight='balanced',random_state=42))]);m.fit(X,y);joblib.dump(m,MODEL);return m
def risk_category(p):return 'low' if p<.3 else 'moderate' if p<.6 else 'high'
def compute_shap_contributions(model,features):
 try:
  import shap
  X,_=load_pima_benchmark(str(DATA));pre=model.named_steps['preprocess'];est=model.named_steps['clf'];bg=np.asarray(pre.transform(X.sample(min(100,len(X)),random_state=42)));row=np.asarray(pre.transform(pd.DataFrame([features])[FEATURE_COLUMNS]))
  if 'tree' in est.__class__.__name__.lower() or est.__class__.__module__.startswith(('xgboost','lightgbm','catboost')): raw=shap.TreeExplainer(est,data=bg,feature_perturbation='interventional').shap_values(row)
  else: raw=shap.Explainer(est,shap.maskers.Independent(bg,max_samples=min(100,len(bg))))(row).values
  vals=np.asarray(raw)
  if vals.ndim==3:vals=vals[...,-1]
  vals=vals.reshape(1,-1) if vals.ndim==1 else vals
  vals=vals[0]
  if len(vals)!=len(FEATURE_COLUMNS):raise ValueError('Unexpected SHAP dimensions')
  method='SHAP'
 except Exception as exc:
  log.exception('SHAP failed; using labelled coefficient fallback: %s',exc);est=model.named_steps['clf']
  if not hasattr(est,'coef_'):raise RuntimeError('No supported explanation fallback') from exc
  x=np.asarray(model.named_steps['preprocess'].transform(pd.DataFrame([features])[FEATURE_COLUMNS])).ravel();vals=est.coef_.ravel()*x;method='coefficient_fallback_not_SHAP'
 return [{'feature':k,'value':float(features[k]),'contribution':float(v),'direction':'increases_risk' if v>0 else 'decreases_risk','method':method} for k,v in sorted(zip(FEATURE_COLUMNS,vals),key=lambda z:abs(z[1]),reverse=True)]
def predict(features:dict[str,float],return_explanation=True,return_uncertainty=True,uncertainty_threshold=.5)->dict[str,Any]:
 m=load_model();p=float(m.predict_proba(pd.DataFrame([features])[FEATURE_COLUMNS])[0,1]);u=float(entropy_uncertainty(np.array([p]))[0]) if return_uncertainty else None;abstain=bool(u is not None and u>uncertainty_threshold)
 return {'model_version':'baseline-lr-0.2.0','data_source_note':'Public Pima Indians Diabetes dataset (methodological benchmark only), not Nigerian hospital data.','probability':p,'risk_category':risk_category(p),'prediction':-1 if abstain else int(p>=.5),'abstain':abstain,'uncertainty':u,'uncertainty_measure':'binary_entropy_nats' if u is not None else None,'confidence_statement':'Abstain: clinician review required.' if abstain else f'Benchmark model probability: {p:.1%}; not a diagnosis.','feature_contributions':compute_shap_contributions(m,features) if return_explanation else None,'limitations':['Pima public benchmark only; no Nigerian external validation.','Entropy is not a calibrated clinical confidence interval.','SHAP is model behaviour, not causality.']}
