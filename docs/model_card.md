# Model Card – ClinAssist Nigeria Baseline

**Model ID:** baseline-lr-0.1.0  
**Date:** 2026-11-08  
**Intended use:** Research prototype for diabetes risk assessment support in resource-constrained clinical settings.

## Model Details
- Algorithm: Logistic Regression (balanced class weights)
- Preprocessing: Zero-as-missing for physiological zeros → median imputation → standard scaling
- Features: Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age
- Uncertainty: Binary entropy of predicted probability; optional abstention above threshold
- Explanations: Coefficient × scaled-feature contributions (directionally consistent)

## Training Data
- Public Pima Indians Diabetes dataset (UCI)
- n = 768, binary outcome
- **Explicitly not Nigerian multi-hospital data**
- See `docs/dataset_provenance.md`

## Evaluation (Stratified 5-fold CV on Pima)
| Metric   | Value  |
|----------|--------|
| AUROC    | 0.835  |
| AUPRC    | 0.707  |
| Brier    | 0.157  |
| ECE      | 0.036  |

Full results: `ml/artifacts/experiments/baseline_cv_results.json`

## Domain Adaptation (Controlled Shift)
Simulated shift by median split on Age and BMI. CORAL improves both discrimination and calibration vs source-only.

See `ml/artifacts/experiments/domain_adaptation_results.json`.

## Out-of-Scope Uses
- Autonomous diagnosis or treatment decisions
- Claims of performance on Nigerian teaching-hospital populations (not yet evaluated)
- Causal interpretation of feature contributions

## Limitations
- Small public benchmark dataset
- No real multi-site Nigerian external validation
- Coefficient-based explanations are not full SHAP
- Performance under true hospital distribution shift is unknown until verified data are available

## Ethical Considerations
- System is designed to support, not replace, qualified clinicians
- Every prediction response includes a clinical disclaimer and data-source note
- No identifiable patient data are stored in the repository
