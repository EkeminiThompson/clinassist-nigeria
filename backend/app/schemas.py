from typing import List,Optional
from pydantic import BaseModel,Field,field_validator
class PatientFeatures(BaseModel):
 Pregnancies:float=Field(...,ge=0);Glucose:float=Field(...,ge=0);BloodPressure:float=Field(...,ge=0);SkinThickness:float=Field(...,ge=0);Insulin:float=Field(...,ge=0);BMI:float=Field(...,ge=0);DiabetesPedigreeFunction:float=Field(...,ge=0);Age:float=Field(...,ge=21,le=120)
 @field_validator('*',mode='before')
 @classmethod
 def numeric(cls,v):return None if v is None else float(v)
class PredictionRequest(BaseModel):
 features:PatientFeatures;return_explanation:bool=True;return_uncertainty:bool=True;uncertainty_threshold:float=Field(.5,ge=0,le=.6932)
class FeatureContribution(BaseModel):feature:str;value:float;contribution:float;direction:str;method:Optional[str]=None
class PredictionResponse(BaseModel):
 model_version:str;data_source_note:str;probability:float;risk_category:str;prediction:int;abstain:bool=False;uncertainty:Optional[float]=None;uncertainty_measure:Optional[str]=None;confidence_statement:str;feature_contributions:Optional[List[FeatureContribution]]=None;clinical_disclaimer:str='Clinician review only; not diagnosis or treatment.';limitations:List[str]=Field(default_factory=list)
