from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from backend.app.audit import record_event
from backend.app.db import get_db
from backend.app.models import User
from backend.app.security import require_roles
from backend.app.schemas import FeatureContribution,PredictionRequest,PredictionResponse
from backend.app.services.prediction import predict
from backend.app.core.config import settings
router=APIRouter(prefix="/api/v1",tags=["prediction"])
@router.post("/predict",response_model=PredictionResponse)
def endpoint(req:PredictionRequest,db:Session=Depends(get_db),user:User=Depends(require_roles("admin","clinician","researcher"))):
    # Release safety gate: this benchmark has no Nigerian external validation or
    # clinical approval. Do not expose inference in production deployments.
    if settings.environment.lower()=="production":
        raise HTTPException(503,"Clinical prediction is disabled in production: this research benchmark has not completed Nigerian external validation and clinical governance review.")
    try:
        result=predict(req.features.model_dump(),req.return_explanation,req.return_uncertainty,req.uncertainty_threshold,model_name=req.model_name)
        if result.get("feature_contributions"): result["feature_contributions"]=[FeatureContribution(**item) for item in result["feature_contributions"]]
        record_event(db,user,"prediction.completed","prediction",{"model_version":result["model_version"],"model_name":req.model_name,"abstained":result["abstain"]})
        return PredictionResponse(**result)
    except ValueError as exc: raise HTTPException(422,str(exc))
    except Exception: raise HTTPException(500,"Prediction failed; check model availability and server logs.")
