import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from backend.app.api.predict import router as predict_router
from backend.app.api.auth import router as auth_router
from backend.app.api.sync import router as sync_router
from backend.app.core.config import settings\nfrom backend.app.limiter import limiter\nfrom slowapi import _rate_limit_exceeded_handler\nfrom slowapi.errors import RateLimitExceeded
app=FastAPI(title="ClinAssist Nigeria API",version="0.3.0",docs_url="/api/docs")\napp.state.limiter=limiter\napp.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware,allow_origins=settings.allowed_origins,allow_credentials=True,allow_methods=["GET","POST","PATCH"],allow_headers=["Authorization","Content-Type"])
app.include_router(auth_router);app.include_router(predict_router);app.include_router(sync_router)
@app.get("/health")
def health(): return {"status":"ok","service":"clinassist-nigeria","mode":"research","disclaimer":"Not autonomous diagnosis or treatment."}
@app.get("/api/v1/model/info")
def info(): return {"model_version":"baseline-lr-0.2.0","data_source_note":"Public Pima benchmark only; not Nigerian multi-hospital validation.","supports_uncertainty":True,"supports_explainability":True,"explanation_methods":{"logistic_regression":"SHAP with labelled coefficient fallback","random_forest":"TreeSHAP","xgboost":"TreeSHAP"},"supported_models":["logistic_regression","random_forest","xgboost"],"uncertainty_note":"Binary entropy is not a calibrated confidence interval.","offline_capable":True}
