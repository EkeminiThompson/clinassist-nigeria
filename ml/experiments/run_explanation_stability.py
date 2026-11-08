"""Local TreeSHAP explanation stability under controlled feature perturbations."""
from __future__ import annotations
import argparse,sys
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from ml.explainability.tree_shap import tree_shap_values,ranked_features
from ml.explainability.stability import rank_biased_overlap
from ml.preprocessing.pipeline import FEATURE_COLUMNS,build_preprocessing_pipeline,load_pima_benchmark
DATA=ROOT/"ml/datasets/diabetes_dataset.csv";OUT=ROOT/"ml/artifacts/experiments"
def models(seed):
    return {"random_forest":RandomForestClassifier(n_estimators=250,max_depth=6,min_samples_leaf=3,class_weight="balanced",n_jobs=-1,random_state=seed),
            "xgboost":XGBClassifier(n_estimators=180,max_depth=3,learning_rate=.04,subsample=.8,colsample_bytree=.8,reg_lambda=2,random_state=seed,eval_metric="logloss",verbosity=0)}
def run_stability(seed=42,n_explain=100,noise_levels=(.01,.05,.10)):
    X,y=load_pima_benchmark(str(DATA));train_x,test_x,train_y,_=train_test_split(X,y,test_size=.25,stratify=y,random_state=seed)
    prep=build_preprocessing_pipeline();xs=prep.fit_transform(train_x);xt=prep.transform(test_x)
    rng=np.random.default_rng(seed);xt=xt[:min(n_explain,len(xt))]
    background=xs[:min(100,len(xs))];rows=[]
    for name,model in models(seed).items():
        model.fit(xs,train_y)
        base=tree_shap_values(model,background,xt,FEATURE_COLUMNS)
        base_ranks=ranked_features(base,FEATURE_COLUMNS)
        for sigma in noise_levels:
            perturbed=xt+rng.normal(0,sigma,size=xt.shape)
            changed=tree_shap_values(model,background,perturbed,FEATURE_COLUMNS)
            changed_ranks=ranked_features(changed,FEATURE_COLUMNS)
            scores=[rank_biased_overlap(a,b,p=.9) for a,b in zip(base_ranks,changed_ranks)]
            rows.append({"model":name,"noise_sigma_standardized":sigma,"n_explanations":len(scores),"mean_rbo":float(np.mean(scores)),"std_rbo":float(np.std(scores)),"seed":seed})
    frame=pd.DataFrame(rows);OUT.mkdir(parents=True,exist_ok=True);frame.to_csv(OUT/"explanation_stability.csv",index=False)
    return frame
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--seed",type=int,default=42);parser.add_argument("--n-explain",type=int,default=100);args=parser.parse_args()
    if args.n_explain<2:parser.error("--n-explain must be >=2")
    print(run_stability(seed=args.seed,n_explain=args.n_explain).to_string(index=False))
