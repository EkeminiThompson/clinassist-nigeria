"""
Prediction API routes.
"""

from fastapi import APIRouter, HTTPException

from backend.app.schemas import FeatureContribution, PredictionRequest, PredictionResponse
from backend.app.services.prediction import predict

router = APIRouter(prefix="/api/v1", tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def predict_endpoint(req: PredictionRequest):
    try:
        features = req.features.model_dump()
        result = predict(
            features=features,
            return_explanation=req.return_explanation,
            return_uncertainty=req.return_uncertainty,
            uncertainty_threshold=req.uncertainty_threshold,
        )
        if result.get("feature_contributions"):
            result["feature_contributions"] = [
                FeatureContribution(**c) for c in result["feature_contributions"]
            ]
        return PredictionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
