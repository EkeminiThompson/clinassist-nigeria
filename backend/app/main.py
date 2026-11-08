"""
ClinAssist Nigeria – FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ClinAssist Nigeria API",
    description=(
        "Explainable, uncertainty-aware clinical decision support API "
        "designed for resource-constrained Nigerian teaching hospital environments. "
        "Initial use case: diabetes risk assessment."
    ),
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "clinassist-nigeria",
        "version": "0.1.0",
        "mode": "research",
        "disclaimer": (
            "This system supports qualified healthcare professionals. "
            "It does not provide autonomous diagnosis or treatment recommendations."
        ),
    }


@app.get("/api/v1/model/info")
def model_info():
    return {
        "model_version": "baseline-0.1.0",
        "data_source_note": (
            "Current models are trained on the public Pima Indians Diabetes dataset "
            "used strictly as a methodological benchmark. See docs/dataset_provenance.md."
        ),
        "features": [
            "Pregnancies",
            "Glucose",
            "BloodPressure",
            "SkinThickness",
            "Insulin",
            "BMI",
            "DiabetesPedigreeFunction",
            "Age",
        ],
        "supports_uncertainty": True,
        "supports_explainability": True,
        "offline_capable": True,
    }
