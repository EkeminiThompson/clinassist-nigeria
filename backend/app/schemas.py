"""
Pydantic schemas for ClinAssist Nigeria API.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class PatientFeatures(BaseModel):
    Pregnancies: float = Field(..., ge=0, description="Number of pregnancies")
    Glucose: float = Field(..., ge=0, description="Plasma glucose concentration")
    BloodPressure: float = Field(..., ge=0, description="Diastolic blood pressure (mm Hg)")
    SkinThickness: float = Field(..., ge=0, description="Triceps skinfold thickness (mm)")
    Insulin: float = Field(..., ge=0, description="2-Hour serum insulin (mu U/ml)")
    BMI: float = Field(..., ge=0, description="Body mass index")
    DiabetesPedigreeFunction: float = Field(..., ge=0, description="Diabetes pedigree function")
    Age: float = Field(..., ge=21, le=120, description="Age in years")

    @field_validator("*", mode="before")
    @classmethod
    def coerce_numeric(cls, v):
        if v is None:
            return v
        return float(v)


class PredictionRequest(BaseModel):
    features: PatientFeatures
    return_explanation: bool = True
    return_uncertainty: bool = True
    uncertainty_threshold: float = Field(0.5, ge=0.0, le=1.0)


class FeatureContribution(BaseModel):
    feature: str
    value: float
    contribution: float
    direction: str


class PredictionResponse(BaseModel):
    model_version: str
    data_source_note: str
    probability: float
    risk_category: str
    prediction: int
    abstain: bool = False
    uncertainty: Optional[float] = None
    uncertainty_measure: Optional[str] = None
    confidence_statement: str
    feature_contributions: Optional[List[FeatureContribution]] = None
    clinical_disclaimer: str = (
        "This output is intended to support qualified healthcare professionals. "
        "It does not constitute a diagnosis or treatment recommendation. "
        "Clinical judgment remains essential."
    )
    limitations: List[str] = Field(default_factory=list)
