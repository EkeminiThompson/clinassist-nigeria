import numpy as np
import pandas as pd
from ml.experiments.run_subgroup_statistical_audit import _subgroups,_metrics,_paired_bootstrap

def test_subgroups_create_age_and_bmi_bands_and_exclude_zero_bmi():
    x=pd.DataFrame({"Age":[20,35,60,40],"BMI":[17.0,24.9,30.0,0.0]})
    out=_subgroups(x)
    assert out["age_group"].tolist()==["<30","30-49","50+","30-49"]
    assert out["bmi_group"].iloc[0]=="<18.5"
    assert out["bmi_group"].iloc[1]=="18.5-24.9"
    assert out["bmi_group"].iloc[2]==">=30"
    assert pd.isna(out["bmi_group"].iloc[3])

def test_small_subgroup_keeps_denominator_but_suppresses_unstable_metrics():
    result=_metrics(np.array([0,1,0,1]),np.array([.1,.9,.2,.8]))
    assert result["n"]==4 and result["events"]==2
    assert result["eligible_for_metrics"] is False
    assert np.isnan(result["auroc"])

def test_paired_bootstrap_reports_intervals_for_eligible_subgroup():
    y=np.array([0,1]*30)
    p=np.where(y==1,.8,.2)
    q=np.where(y==1,.85,.15)
    result=_paired_bootstrap(y,p,q,100,np.random.default_rng(4))
    assert result["status"]=="ok"
    assert result["valid_replicates"]>0
    assert result["auroc_delta"]>=0
    assert result["auroc_ci_lower"]<=result["auroc_ci_upper"]
