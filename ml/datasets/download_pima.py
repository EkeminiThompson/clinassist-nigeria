"""Fetch and validate OpenML dataset 37 (Pima Indians Diabetes) locally.

The raw dataset is not committed to Git. The loader checks its schema, sample
count and class balance before writing the canonical CSV and a SHA-256 manifest.
"""
from __future__ import annotations
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
import pandas as pd
from sklearn.datasets import fetch_openml
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"ml/datasets/diabetes_dataset.csv"
ALIASES={"preg":"Pregnancies","plas":"Glucose","pres":"BloodPressure","skin":"SkinThickness","insu":"Insulin","mass":"BMI","pedi":"DiabetesPedigreeFunction","age":"Age"}
def main():
    dataset=fetch_openml(data_id=37,as_frame=True)
    frame=dataset.frame.copy()
    frame.columns=[str(c).strip().lower() for c in frame.columns]
    target_name=next((c for c in ("class","diabetes","outcome") if c in frame.columns),None)
    if target_name is None: raise ValueError(f"OpenML data_id=37 has unexpected target columns: {frame.columns.tolist()}")
    if not set(ALIASES).issubset(frame.columns): raise ValueError(f"Unexpected feature schema: {frame.columns.tolist()}")
    y=frame.pop(target_name).astype(str).str.lower()
    mapping={"tested_negative":0,"tested_positive":1,"negative":0,"positive":1,"0":0,"1":1}
    if not set(y.unique()).issubset(mapping): raise ValueError(f"Unexpected target labels: {sorted(y.unique())}")
    canonical=frame[list(ALIASES)].rename(columns=ALIASES)
    canonical["Outcome"]=y.map(mapping).astype(int)
    if len(canonical)!=768: raise ValueError(f"Expected 768 rows, received {len(canonical)}")
    counts=canonical["Outcome"].value_counts().to_dict()
    if counts!={0:500,1:268}: raise ValueError(f"Unexpected class distribution: {counts}")
    for col in canonical.columns: canonical[col]=pd.to_numeric(canonical[col],errors="raise")
    OUT.parent.mkdir(parents=True,exist_ok=True);canonical.to_csv(OUT,index=False)
    digest=hashlib.sha256(OUT.read_bytes()).hexdigest()
    manifest={"source":"OpenML dataset id 37 (Pima Indians Diabetes; original source NIDDK/UCI)","openml_data_id":37,"dataset_name":dataset.details.get("name"),"version":dataset.details.get("version"),"retrieved_at":datetime.now(timezone.utc).isoformat(),"n_samples":len(canonical),"class_counts":{str(k):int(v) for k,v in counts.items()},"feature_columns":list(ALIASES.values()),"target_column":"Outcome","csv_sha256":digest,"file":"diabetes_dataset.csv","note":"Historical Pima cohort of adult women; methodological benchmark only, not Nigerian hospital validation."}
    (OUT.parent/"pima_manifest.json").write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest,indent=2))
if __name__=="__main__": main()
